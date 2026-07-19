import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from types import SimpleNamespace
from unittest import mock
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core import mail
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import DatabaseError, close_old_connections, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.test import Client, TransactionTestCase, override_settings

from crm.contact_services import (
    ContactData,
    DailyContactLimitReached,
    _next_dossier_number,
    canonical_contact_payload,
    compute_contact_hmac,
    create_contact_dossier,
    normalize_french_mobile,
    verify_contact_hmac,
)
from crm.models import Contact, ContactDailyCounter, ContactMessage


TEST_SETTINGS = {
    "CONTACT_HMAC_SECRET": "test-contact-hmac-secret-at-least-32-characters",
    "EMAIL_BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    "DEFAULT_FROM_EMAIL": "test-sender-do-not-use@pixelprowlers.io",
    "CONTACT_TO": "contact@example.invalid",
    "TRUSTED_PROXY_IPS": set(),
}
PARIS = ZoneInfo("Europe/Paris")


def contact_data(index=1, **changes):
    values = {
        "nom": "Martin",
        "prenom": f"Alice{index}",
        "email": f"alice{index}@example.com",
        "telephone": "0612345678",
        "objet": "Audit du site",
        "message": "Nous souhaitons faire auditer notre site avant une refonte.",
        "methode_contact": "email",
        "company": "Association Exemple",
        "service_type": "audit_site",
        "demand_type": "audit",
    }
    values.update(changes)
    return ContactData(**values)


@override_settings(**TEST_SETTINGS)
class ContactGraphQLTests(TransactionTestCase):
    def setUp(self):
        cache.clear()
        self.client = Client(HTTP_HOST="localhost", REMOTE_ADDR="127.0.0.1")

    def submit(self, **changes):
        variables = {
            "nom": "Martin",
            "prenom": "Alice",
            "company": "Association Exemple",
            "email": "alice@example.com",
            "telephone": "0612345678",
            "objet": "Audit du site",
            "methodeContact": "email",
            "serviceType": "audit_site",
            "demandType": "audit",
            "message": "Nous souhaitons faire auditer notre site avant une refonte.",
            "startedAt": int((time.time() - 5) * 1000),
        }
        variables.update(changes)
        query = """
            mutation Contact(
              $nom: String!, $prenom: String!, $company: String!, $email: String!, $telephone: String!,
              $objet: String!, $methodeContact: String!, $serviceType: String!,
              $demandType: String, $message: String!, $startedAt: Float!
            ) {
              createContact(
                nom: $nom, prenom: $prenom, company: $company, email: $email, telephone: $telephone,
                objet: $objet, methodeContact: $methodeContact, serviceType: $serviceType,
                demandType: $demandType, message: $message, privacyConsent: true,
                startedAt: $startedAt
              ) {
                success
                numeroDossier
                message
              }
            }
        """
        return self.client.post(
            "/graphql/",
            data=json.dumps({"query": query, "variables": variables}),
            content_type="application/json",
        )

    def assert_rejected(self, **changes):
        cache.clear()
        response = self.submit(**changes)
        self.assertIn(response.status_code, {200, 400})
        self.assertIsNotNone(response.json().get("errors"), response.content)
        self.assertEqual(Contact.objects.count(), 0)

    def test_valid_request_persists_and_returns_public_contract(self):
        response = self.submit()
        body = response.json()
        self.assertIsNone(body.get("errors"))
        result = body["data"]["createContact"]
        self.assertTrue(result["success"])
        self.assertRegex(result["numeroDossier"], r"^\d{8}001$")
        self.assertEqual(set(result), {"success", "numeroDossier", "message"})
        self.assertNotIn("hmac", response.content.decode().lower())
        contact = Contact.objects.get()
        self.assertEqual(contact.demand_type, "audit")
        self.assertEqual(contact.prenom, "Alice")
        self.assertEqual(contact.nom, "Martin")
        self.assertEqual(contact.company, "Association Exemple")
        self.assertEqual(contact.email, "alice@example.com")
        self.assertEqual(contact.phone, "0612345678")
        self.assertEqual(contact.methode_contact, "email")
        self.assertEqual(contact.objet, "Audit du site")
        self.assertEqual(contact.message, "Nous souhaitons faire auditer notre site avant une refonte.")
        self.assertIsNotNone(contact.client_dossier_id)
        first_message = ContactMessage.objects.get(contact=contact)
        self.assertEqual(first_message.author, ContactMessage.Author.CUSTOMER)
        self.assertEqual(first_message.message, contact.message)
        self.assertEqual(len(contact.signature_hmac), 64)
        self.assertTrue(verify_contact_hmac(contact))

    def test_materiel_belongs_to_the_declared_choices(self):
        self.assertIn("materiel", {choice.value for choice in Contact.DemandType})
        self.assertIn("materiel", {choice.value for choice in Contact.ServiceType})

    def test_materiel_demand_type_is_accepted_and_persists_service_type(self):
        response = self.submit(
            serviceType="materiel",
            demandType="materiel",
            objet="Ordinateur portable qui ne démarre plus",
        )
        body = response.json()
        self.assertIsNone(body.get("errors"), body)
        result = body["data"]["createContact"]
        self.assertTrue(result["success"])

        # Une seule ligne créée, avec les deux valeurs attendues persistées.
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.get()
        self.assertEqual(contact.demand_type, "materiel")
        self.assertEqual(contact.service_type, "materiel")
        self.assertEqual(
            contact.get_demand_type_display(),
            "Matériel : réparation, reconditionnement, migration Linux",
        )

        # Numéro de dossier conforme et retourné publiquement.
        self.assertRegex(result["numeroDossier"], r"^\d{8}001$")
        self.assertEqual(contact.numero_dossier, result["numeroDossier"])

        # Le HMAC de la ligne créée reste valide.
        self.assertEqual(len(contact.signature_hmac), 64)
        self.assertTrue(verify_contact_hmac(contact))

        # L'e-mail est simulé par le backend mémoire, jamais un SMTP réel.
        self.assertEqual(settings.EMAIL_BACKEND, "django.core.mail.backends.locmem.EmailBackend")
        sent_to_client = [item for item in mail.outbox if item.to == [contact.email]]
        self.assertEqual(len(sent_to_client), 1)
        self.assertEqual(contact.statut_notification, Contact.NotificationStatus.SENT)

    def test_other_demand_types_still_work_after_adding_materiel(self):
        for demand_type, service_type in (
            ("diagnostic", "audit_site"),
            ("urgency", "urgence"),
            ("audit", "audit_site"),
            ("refonte", "site_maintenable"),
            ("transmission", "maintenance_documentation"),
            ("partnership", "autre"),
        ):
            with self.subTest(demand_type=demand_type):
                cache.clear()
                response = self.submit(demandType=demand_type, serviceType=service_type)
                body = response.json()
                self.assertIsNone(body.get("errors"), body)
                self.assertTrue(body["data"]["createContact"]["success"])

    def test_unknown_demand_type_is_still_rejected(self):
        self.assert_rejected(demandType="materiel-urgent")
        self.assert_rejected(demandType="unknown")

    def test_validation_rejections(self):
        cases = [
            {"email": "invalid"},
            {"email": "alice@example.com\r\nBcc: victim@example.com"},
            {"email": "alice@example.com\x00"},
            {"methodeContact": "email", "telephone": ""},
            {"methodeContact": "telephone", "telephone": ""},
            {"methodeContact": "les_deux", "telephone": ""},
            {"telephone": "123"},
            {"methodeContact": "fax"},
            {"nom": "   "},
            {"nom": None},
            {"nom": "A" * 101},
            {"prenom": "Alice\r\nBcc: victim@example.com"},
            {"prenom": "Alice\x00Martin"},
            {"objet": "   "},
            {"objet": "Audit\r\nBcc: victim@example.com"},
            {"company": "   "},
            {"company": "Exemple\r\nInjection"},
            {"company": "Exemple\x00"},
            {"message": "Message assez long mais avec un caractère\x00interdit."},
        ]
        for changes in cases:
            with self.subTest(changes=changes):
                self.assert_rejected(**changes)

    def test_phone_is_required_for_email(self):
        self.assert_rejected(telephone="", methodeContact="email")

    def test_graphql_rejects_foreign_phone(self):
        self.assert_rejected(telephone="+32470123456", methodeContact="telephone")

    def test_graphql_stores_and_signs_only_the_canonical_phone(self):
        response = self.submit(telephone="+33 6 12 34 56 78", methodeContact="email")
        self.assertIsNone(response.json().get("errors"))
        contact = Contact.objects.get()
        self.assertEqual(contact.phone, "0612345678")
        payload = canonical_contact_payload(contact)
        self.assertIn(b'"telephone":"0612345678"', payload)
        self.assertNotIn(b"+33 6 12 34 56 78", payload)
        self.assertTrue(verify_contact_hmac(contact))

    def test_graphql_normalizes_organization_and_accepts_particulier(self):
        response = self.submit(company="  Particulier  ")
        self.assertIsNone(response.json().get("errors"))
        self.assertEqual(Contact.objects.get().company, "Particulier")

    def test_graphql_rejects_a_request_without_telephone_argument(self):
        query = """
            mutation {
              createContact(
                nom: "Martin", prenom: "Alice", email: "alice@example.com",
                company: "Association Exemple", objet: "Audit du site",
                methodeContact: "email", serviceType: "audit_site", demandType: "audit",
                message: "Nous souhaitons faire auditer notre site avant une refonte.",
                privacyConsent: true, startedAt: 1
              ) { success }
            }
        """
        response = self.client.post(
            "/graphql/",
            data=json.dumps({"query": query}),
            content_type="application/json",
        )
        self.assertIsNotNone(response.json().get("errors"))
        self.assertFalse(Contact.objects.exists())

    def test_service_rejects_missing_phone_for_every_contact_method(self):
        for method in ("email", "telephone", "les_deux"):
            with self.subTest(method=method):
                with self.assertRaisesRegex(ValueError, "telephone"):
                    create_contact_dossier(contact_data(telephone="", methode_contact=method))

    def test_invalid_json_is_rejected(self):
        response = self.client.post("/graphql/", data=b"{", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    @override_settings(DATA_UPLOAD_MAX_MEMORY_SIZE=128)
    def test_oversized_body_is_rejected(self):
        response = self.client.post("/graphql/", data=b"x" * 256, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_spoofed_forwarded_ip_is_not_trusted(self):
        from crm.schema import _client_ip

        request = SimpleNamespace(META={"REMOTE_ADDR": "203.0.113.10", "HTTP_X_FORWARDED_FOR": "198.51.100.20"})
        info = SimpleNamespace(context=request)
        self.assertEqual(_client_ip(info), "203.0.113.10")

    @override_settings(TRUSTED_PROXY_IPS={"127.0.0.1"})
    def test_trusted_proxy_uses_nearest_forwarded_address(self):
        from crm.schema import _client_ip

        request = SimpleNamespace(
            META={"REMOTE_ADDR": "127.0.0.1", "HTTP_X_FORWARDED_FOR": "198.51.100.99, 203.0.113.20"}
        )
        self.assertEqual(_client_ip(SimpleNamespace(context=request)), "203.0.113.20")

    def test_smtp_failure_returns_honest_public_message(self):
        with mock.patch("crm.contact_services.EmailMultiAlternatives.send", side_effect=RuntimeError("smtp down")):
            response = self.submit()
        result = response.json()["data"]["createContact"]
        self.assertTrue(result["message"].endswith("Conservez votre numéro de dossier."))
        contact = Contact.objects.get()
        self.assertEqual(contact.statut_notification, Contact.NotificationStatus.FAILED)
        self.assertNotIn("smtp", response.content.decode().lower())

    def test_one_mutation_schedules_one_customer_acknowledgement(self):
        with mock.patch(
            "crm.schema.send_contact_acknowledgement",
            return_value=Contact.NotificationStatus.SENT,
        ) as acknowledgement:
            response = self.submit()

        self.assertIsNone(response.json().get("errors"))
        acknowledgement.assert_called_once()
        self.assertEqual(Contact.objects.count(), 1)


@override_settings(**TEST_SETTINGS)
class ContactServiceTests(TransactionTestCase):
    reset_sequences = True

    def test_french_mobile_normalization(self):
        accepted = {
            "0612345678": "0612345678",
            "06 12 34 56 78": "0612345678",
            "+33612345678": "0612345678",
            "+33 6 12 34 56 78": "0612345678",
            "0712345678": "0712345678",
            "07 12 34 56 78": "0712345678",
            "+33712345678": "0712345678",
            "+33 7 12 34 56 78": "0712345678",
        }
        for raw, canonical in accepted.items():
            with self.subTest(raw=raw):
                self.assertEqual(normalize_french_mobile(raw), canonical)

    def test_french_mobile_rejects_foreign_fixed_and_ambiguous_values(self):
        rejected = [
            "+32470123456", "+41791234567", "+34612345678", "0012345678",
            "33612345678", "06AB345678", "+33", "061234567", "06123456789",
            "0123456789", "", "   ", "0612345678\x00", "0612345678\r\n",
        ]
        for raw in rejected:
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(ValueError, "French mobile"):
                    normalize_french_mobile(raw)

    def test_service_accepts_materiel_demand_type(self):
        contact = create_contact_dossier(
            contact_data(service_type="materiel", demand_type="materiel")
        )
        self.assertEqual(contact.demand_type, "materiel")
        self.assertEqual(contact.service_type, "materiel")

    def test_service_stores_canonical_phone_before_hmac(self):
        contact = create_contact_dossier(contact_data(telephone="+33612345678"))
        self.assertEqual(contact.phone, "0612345678")
        self.assertIn(b'"telephone":"0612345678"', canonical_contact_payload(contact))
        self.assertTrue(verify_contact_hmac(contact))

    def test_model_rejects_noncanonical_phone_on_manual_creation(self):
        contact = Contact(
            numero_dossier="14072026999",
            nom="Martin",
            prenom="Alice",
            name="Alice Martin",
            email="alice@example.com",
            company="Particulier",
            phone="+33612345678",
            service_type="audit_site",
            demand_type="audit",
            objet="Audit",
            methode_contact="email",
            message="Description suffisamment longue pour la demande.",
            signature_hmac="a" * 64,
        )
        with self.assertRaises(ValidationError):
            contact.save(force_insert=True)

    def test_number_format_sequence_and_calendar_boundaries(self):
        moments = [
            datetime(2026, 7, 14, 23, 59, 59, tzinfo=PARIS),
            datetime(2026, 7, 15, 0, 0, 0, tzinfo=PARIS),
            datetime(2026, 8, 1, 0, 0, 0, tzinfo=PARIS),
            datetime(2027, 1, 1, 0, 0, 0, tzinfo=PARIS),
        ]
        with transaction.atomic():
            first = _next_dossier_number(moments[0])
            second = _next_dossier_number(moments[0])
            next_day = _next_dossier_number(moments[1])
            next_month = _next_dossier_number(moments[2])
            next_year = _next_dossier_number(moments[3])
        self.assertEqual(first, "14072026001")
        self.assertEqual(second, "14072026002")
        self.assertEqual(next_day, "15072026001")
        self.assertEqual(next_month, "01082026001")
        self.assertEqual(next_year, "01012027001")

    def test_utc_time_uses_paris_business_day(self):
        utc = ZoneInfo("UTC")
        with transaction.atomic():
            number = _next_dossier_number(datetime(2026, 7, 14, 22, 0, 0, tzinfo=utc))
        self.assertEqual(number, "15072026001")

    def test_daily_limit_is_explicit(self):
        ContactDailyCounter.objects.create(date=datetime(2026, 7, 14).date(), value=999)
        with self.assertRaises(DailyContactLimitReached), transaction.atomic():
            _next_dossier_number(datetime(2026, 7, 14, 12, 0, tzinfo=PARIS))

    def test_hmac_is_canonical_and_detects_changes(self):
        contact = Contact(
            numero_dossier="14072026001",
            nom="Martin",
            prenom="Élodie",
            email="elodie@example.com",
            phone="",
            objet="Audit",
            methode_contact="email",
            message="Description",
            date_creation=datetime(2026, 7, 14, 10, 0, tzinfo=ZoneInfo("UTC")),
        )
        first = compute_contact_hmac(contact)
        second = compute_contact_hmac(contact)
        self.assertRegex(first, r"^[0-9a-f]{64}$")
        self.assertEqual(first, second)
        self.assertIn(b'"numero_dossier":"14072026001"', canonical_contact_payload(contact))
        contact.objet = "Objet modifié"
        self.assertNotEqual(first, compute_contact_hmac(contact))

    def test_hmac_covers_every_required_field_and_normalizes_unicode(self):
        base = Contact(
            numero_dossier="14072026001",
            nom="Martin",
            prenom="Élodie",
            email="elodie@example.com",
            phone="0612345678",
            objet="Audit",
            methode_contact="telephone",
            message="Description",
            date_creation=datetime(2026, 7, 14, 10, 0, tzinfo=ZoneInfo("UTC")),
        )
        signature = compute_contact_hmac(base)
        changes = {
            "numero_dossier": "14072026002",
            "date_creation": datetime(2026, 7, 14, 10, 0, 1, tzinfo=ZoneInfo("UTC")),
            "nom": "Durand",
            "prenom": "Alice",
            "email": "alice@example.com",
            "phone": "0699999999",
            "objet": "Refonte",
            "message": "Autre description",
            "methode_contact": "les_deux",
        }
        for field, value in changes.items():
            with self.subTest(field=field):
                original = getattr(base, field)
                setattr(base, field, value)
                self.assertNotEqual(signature, compute_contact_hmac(base))
                setattr(base, field, original)

        base.prenom = "E\u0301lodie"
        decomposed = compute_contact_hmac(base)
        base.prenom = "Élodie"
        self.assertEqual(decomposed, compute_contact_hmac(base))

    @override_settings(CONTACT_HMAC_SECRET="")
    def test_missing_hmac_secret_fails_explicitly(self):
        with self.assertRaisesMessage(Exception, "CONTACT_HMAC_SECRET"):
            create_contact_dossier(contact_data())

    def test_failure_before_commit_rolls_back_contact_and_counter(self):
        with mock.patch("crm.contact_services.ContactMessage.objects.create", side_effect=RuntimeError("insert failed")):
            with self.assertRaises(RuntimeError):
                create_contact_dossier(contact_data())
        self.assertFalse(Contact.objects.exists())
        self.assertFalse(ContactDailyCounter.objects.exists())

    def test_email_is_attempted_after_contact_is_persisted(self):
        from crm.contact_services import send_contact_acknowledgement

        contact = create_contact_dossier(contact_data())

        def assert_persisted(*_args, **_kwargs):
            self.assertTrue(Contact.objects.filter(pk=contact.pk).exists())
            return 1

        with mock.patch("crm.contact_services.EmailMultiAlternatives.send", side_effect=assert_persisted):
            status = send_contact_acknowledgement(contact)
        self.assertEqual(status, Contact.NotificationStatus.SENT)
        contact.refresh_from_db()
        self.assertEqual(contact.statut_notification, Contact.NotificationStatus.SENT)

    def test_on_commit_email_is_not_sent_when_outer_transaction_rolls_back(self):
        from crm.contact_services import send_contact_acknowledgement

        with mock.patch("crm.contact_services.EmailMultiAlternatives.send") as smtp_send:
            with self.assertRaises(RuntimeError):
                with transaction.atomic():
                    contact = create_contact_dossier(contact_data())
                    transaction.on_commit(lambda: send_contact_acknowledgement(contact))
                    raise RuntimeError("rollback before commit")
        smtp_send.assert_not_called()
        self.assertFalse(Contact.objects.exists())

    def test_smtp_failure_keeps_contact_and_sets_failed_status(self):
        from crm.contact_services import send_contact_acknowledgement

        contact = create_contact_dossier(contact_data())
        with mock.patch("crm.contact_services.EmailMultiAlternatives.send", side_effect=RuntimeError("smtp down")):
            status = send_contact_acknowledgement(contact)
        self.assertEqual(status, Contact.NotificationStatus.FAILED)
        contact.refresh_from_db()
        self.assertEqual(contact.statut_notification, Contact.NotificationStatus.FAILED)
        self.assertIsNone(contact.date_notification)
        self.assertTrue(Contact.objects.filter(pk=contact.pk).exists())

    def test_already_sent_contact_is_not_sent_twice(self):
        from crm.contact_services import send_contact_acknowledgement

        contact = create_contact_dossier(contact_data())
        contact.statut_notification = Contact.NotificationStatus.SENT
        contact.date_notification = datetime.now(tz=ZoneInfo("UTC"))
        contact.save(update_fields=["statut_notification", "date_notification", "updated_at"])

        with self.assertLogs("crm.contact_services", level="INFO") as captured:
            with mock.patch("crm.contact_services.EmailMultiAlternatives.send") as smtp_send:
                status = send_contact_acknowledgement(contact)

        smtp_send.assert_not_called()
        self.assertEqual(status, Contact.NotificationStatus.SENT)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertIn("action=skipped", "\n".join(captured.output))

    def test_success_sets_notification_date(self):
        from crm.contact_services import send_contact_acknowledgement

        contact = create_contact_dossier(contact_data())
        status = send_contact_acknowledgement(contact)
        contact.refresh_from_db()
        self.assertEqual(status, Contact.NotificationStatus.SENT)
        self.assertEqual(contact.statut_notification, Contact.NotificationStatus.SENT)
        self.assertIsNotNone(contact.date_notification)

    def test_status_update_failure_does_not_hide_successful_delivery(self):
        from crm.contact_services import send_contact_acknowledgement

        contact = create_contact_dossier(contact_data())
        with mock.patch("crm.contact_services.Contact.objects.filter") as filtered:
            filtered.return_value.update.side_effect = DatabaseError("database unavailable")
            status = send_contact_acknowledgement(contact)
        self.assertEqual(status, Contact.NotificationStatus.SENT)
        self.assertTrue(Contact.objects.filter(pk=contact.pk).exists())

    def test_email_contains_dossier_and_plain_and_html_parts(self):
        from crm.contact_services import send_contact_acknowledgement

        contact = create_contact_dossier(contact_data())
        send_contact_acknowledgement(contact)
        message = next(item for item in mail.outbox if item.to == [contact.email])
        self.assertEqual(message.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertTrue(message.from_email.endswith("@pixelprowlers.io"))
        self.assertEqual(message.to, [contact.email])
        self.assertFalse(message.reply_to)
        self.assertTrue(message.subject.startswith("PixelProwlers — réception de votre demande n°"))
        self.assertIn(contact.numero_dossier, message.subject)
        self.assertIn(contact.numero_dossier, message.body)
        self.assertEqual(message.alternatives[0].mimetype, "text/html")
        complete_content = message.body + message.alternatives[0].content
        self.assertIn(f"Bonjour {contact.prenom},", complete_content)
        self.assertIn(
            "Nous avons bien reçu votre message et ne manquerons pas de revenir vers vous rapidement.",
            complete_content,
        )
        self.assertIn("Cordialement,", complete_content)
        self.assertIn("L’équipe PixelProwlers.", complete_content)
        self.assertNotIn(contact.signature_hmac, complete_content)
        self.assertNotIn(contact.phone, complete_content)
        self.assertNotIn(contact.email, complete_content)
        self.assertNotIn(contact.message, complete_content)
        self.assertNotIn("SMTP", complete_content)
        self.assertNotIn("Brevo", complete_content)
        self.assertNotIn("CONTACT_HMAC_SECRET", complete_content)

    def test_email_html_escapes_customer_name(self):
        from crm.contact_services import send_contact_acknowledgement

        contact = create_contact_dossier(contact_data(prenom="Alice & Bob"))
        send_contact_acknowledgement(contact)
        message = next(item for item in mail.outbox if item.to == [contact.email])
        html = message.alternatives[0].content
        self.assertIn("Bonjour Alice &amp; Bob,", html)
        self.assertNotIn("Bonjour Alice & Bob,", html)

    def test_email_failure_log_does_not_include_secret_or_recipient(self):
        from crm.contact_services import send_contact_acknowledgement

        contact = create_contact_dossier(contact_data())
        leaked_value = "credential-that-must-not-appear"
        with self.assertLogs("crm.contact_services", level="ERROR") as captured:
            with mock.patch(
                "crm.contact_services.EmailMultiAlternatives.send",
                side_effect=RuntimeError(leaked_value),
            ):
                send_contact_acknowledgement(contact)
        rendered_logs = "\n".join(captured.output)
        self.assertNotIn(leaked_value, rendered_logs)
        self.assertNotIn(contact.email, rendered_logs)
        self.assertIn(contact.numero_dossier, rendered_logs)

    def test_fifty_concurrent_postgresql_creations_are_unique(self):
        if connection.vendor != "postgresql":
            self.skipTest("PostgreSQL concurrency semantics required")
        fixed_now = datetime(2026, 9, 20, 12, 0, tzinfo=PARIS)

        def create(index):
            close_old_connections()
            try:
                return create_contact_dossier(contact_data(index), now=fixed_now).numero_dossier
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=10) as pool:
            numbers = list(pool.map(create, range(1, 51)))
        self.assertEqual(len(numbers), 50)
        self.assertEqual(len(set(numbers)), 50)
        self.assertEqual(sorted(numbers), [f"20092026{index:03d}" for index in range(1, 51)])
        self.assertEqual(Contact.objects.filter(numero_dossier__startswith="20092026").count(), 50)


class RequiredContactFieldsMigrationTests(TransactionTestCase):
    migrate_from = [("crm", "0003_contact_dossier_authority")]
    migrate_to = [("crm", "0004_remove_contact_crm_contact_phone_required_and_more")]

    def test_incomplete_historical_contact_is_preserved_without_fake_phone(self):
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps
        OldContact = old_apps.get_model("crm", "Contact")
        OldContact.objects.create(
            ticket_id="15072026001",
            secret_token="historical-contact-token",
            numero_dossier="15072026001",
            nom="Historique",
            prenom="Contact",
            name="Contact Historique",
            email="historique@example.com",
            company="",
            phone="",
            service_type="audit_site",
            demand_type="",
            objet="Ancienne demande",
            methode_contact="email",
            message="Demande créée avant la politique téléphonique stricte.",
            signature_hmac="a" * 64,
        )

        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_to)
        new_apps = executor.loader.project_state(self.migrate_to).apps
        migrated = new_apps.get_model("crm", "Contact").objects.get(numero_dossier="15072026001")
        self.assertEqual(migrated.phone, "")
        self.assertEqual(migrated.company, "")
        self.assertEqual(migrated.demand_type, "")
        self.assertEqual(migrated.signature_hmac, "a" * 64)
