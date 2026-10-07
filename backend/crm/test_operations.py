import socket
import json
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management import call_command, CommandError
from django.core.exceptions import PermissionDenied
from django.db import close_old_connections, IntegrityError, transaction
from django.test import TestCase, TransactionTestCase, Client, override_settings
from django.utils import timezone

from audits.models import AuditDossier, AuditReponse, CreneauCalendrier, Motif, Rdv, RdvRappel, Citation, RaisonAppel
from audits.rdv_services import reserve_rdv, send_due_reminders
from crm.models import Contact, ContactMessage, Notification
from crm.operator_services import reply_to_contact
from crm.outbox import enqueue, process_one, claim, retry

SMTP = dict(NOTIFICATION_DELIVERY_ENABLED=True, EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend",
            EMAIL_USE_TLS=True, EMAIL_USE_SSL=False, EMAIL_HOST_USER="fixture", EMAIL_HOST_PASSWORD="fixture-only", EMAIL_TIMEOUT=10)


class OperationsTests(TestCase):
    def setUp(self):
        directory = self.enterContext(tempfile.TemporaryDirectory())
        self.enterContext(override_settings(RATE_LIMIT_DATABASE=directory + "/quota.sqlite3"))

    def enqueue(self):
        return enqueue(event_key="synthetic:created", subject="Synthetic", message="Private fixture payload",
                       from_email="fixture@example.invalid", recipient_list=["controlled@example.invalid"])

    @override_settings(**SMTP)
    def test_identity_acceptance_and_no_second_submission(self):
        self.assertEqual(self.enqueue(), "pending")
        self.enqueue()
        self.assertEqual(Notification.objects.count(), 1)
        with patch("crm.outbox.EmailMessage.send", return_value=1) as send:
            self.assertTrue(process_one())
            self.assertFalse(process_one())
            self.assertEqual(send.call_count, 1)
        item = Notification.objects.get()
        self.assertEqual(item.state, "relay_accepted")
        self.assertIsNotNone(item.accepted_at)

    @override_settings(**SMTP)
    def test_known_failure_backoff_then_acceptance(self):
        self.enqueue()
        with patch("crm.outbox.EmailMessage.send", side_effect=ConnectionRefusedError):
            process_one()
        item = Notification.objects.get()
        self.assertEqual(item.state, "transient_failed")
        self.assertEqual(item.attempts, 1)
        self.assertFalse(process_one())
        retry(item.pk)
        with patch("crm.outbox.EmailMessage.send", return_value=1):
            process_one()
        item.refresh_from_db()
        self.assertEqual(item.state, "relay_accepted")
        self.assertEqual(item.attempts, 2)

    @override_settings(**SMTP)
    def test_timeout_and_worker_interruption_are_uncertain_no_auto_replay(self):
        self.enqueue()
        with patch("crm.outbox.EmailMessage.send", side_effect=socket.timeout):
            process_one()
        item = Notification.objects.get()
        self.assertEqual(item.state, "uncertain")
        self.assertFalse(process_one())
        with self.assertRaises(ValueError):
            retry(item.pk)
        retry(item.pk, acknowledge_uncertain=True)
        claimed = claim()
        Notification.objects.filter(pk=claimed.pk).update(lease_until=timezone.now()-timedelta(seconds=1))
        self.assertIsNone(claim())
        item.refresh_from_db()
        self.assertEqual(item.state, "uncertain")

    def test_disabled_delivery_has_no_console_payload_or_attempt(self):
        self.enqueue()
        with override_settings(NOTIFICATION_DELIVERY_ENABLED=False), patch("crm.outbox.EmailMessage.send") as send:
            self.assertFalse(process_one())
            send.assert_not_called()
        self.assertEqual(Notification.objects.get().attempts, 0)

    def test_controlled_recipe_refuses_recipient_substitution(self):
        self.enqueue()
        item = Notification.objects.get()
        with self.assertRaises(CommandError):
            call_command('process_notifications', id=item.pk, test_recipient='other@example.invalid')
        with override_settings(**dict(SMTP, NOTIFICATION_DELIVERY_ENABLED=False)), patch('crm.outbox.EmailMessage.send', return_value=1):
            call_command('process_notifications', id=item.pk, test_recipient='controlled@example.invalid')
        item.refresh_from_db()
        self.assertEqual(item.state, 'relay_accepted')

    def test_reference_operations_and_contact_categories_execute(self):
        Citation.objects.create(numero=99999, texte="Citation synthétique", auteur="Qualification", source="Fixtures")
        motif = Motif.objects.create(nom="Consultation synthétique", duree_minutes=60)
        RaisonAppel.objects.create(nom="Besoin synthétique")
        client = Client(HTTP_HOST="localhost", HTTP_ORIGIN="http://localhost")
        def gql(query, variables=None):
            result = client.post('/graphql/', json.dumps({'query': query, 'variables': variables or {}}), content_type='application/json').json()
            self.assertFalse(result.get('errors'), result)
            return result['data']
        data = gql('query($m:Int!){citationAleatoire{texte} motifs{id nom} raisonsAppel{id nom} calendrierMois(annee:2044,mois:4){date statut} creneauxDisponibles(motifId:$m,dateDebut:"2044-04-04",dateFin:"2044-04-05"){date heureDebut heureFin}}', {'m': motif.pk})
        for field in ['citationAleatoire', 'motifs', 'raisonsAppel', 'calendrierMois', 'creneauxDisponibles']:
            self.assertTrue(data[field])
        for need, service in [('reparation','materiel'), ('reemploi','materiel'), ('formation','formation')]:
            gql('mutation($n:String!,$v:String!,$s:Float!){createContact(name:"Synthetic category",email:"fixture@example.invalid",serviceType:$v,need:$n,budget:"100–150 €",message:"Contexte synthétique conservé avec la demande.",privacyConsent:true,startedAt:$s){contact{ticketId}}}', {'n':need, 'v':service, 's':(time.time()-5)*1000})
            contact=Contact.objects.latest('pk')
            self.assertEqual(contact.request_context['need'], need)
            self.assertEqual(contact.request_context['budget'], '100–150 €')
            self.assertEqual(contact.messages.count(), 1)

    def test_operator_reply_is_private_authoritative_and_durable(self):
        contact = Contact.objects.create(name="Synthetic", email="controlled@example.invalid", service_type="materiel", message="Synthetic repair request", request_context={"budget": "100–150 €"})
        user = get_user_model().objects.create_user("synthetic-operator", is_staff=True)
        with self.assertRaises(PermissionDenied):
            reply_to_contact(contact=contact, message="Réponse synthétique", operator=user)
        user.user_permissions.add(*Permission.objects.filter(content_type__app_label="crm", codename__in=["change_contact", "add_contactmessage", "view_contact", "view_contactmessage"]))
        user = get_user_model().objects.get(pk=user.pk)
        reply = reply_to_contact(contact=contact, message="Réponse synthétique", operator=user)
        self.assertEqual(reply.author, "support")
        self.assertEqual(reply.author_name, "synthetic-operator")
        self.assertEqual(Notification.objects.get().state, "pending")
        client = Client()
        client.force_login(user)
        response = client.get(f"/admin/crm/contact/{contact.pk}/change/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Réponse synthétique")
        self.assertContains(response, "budget")
        self.assertContains(response, 'name="reply"')
        self.assertNotContains(response, contact.secret_token)

    def test_audit_updates_resign_and_missing_key_does_not_persist(self):
        dossier = AuditDossier.objects.create(numero_dossier="SYNTH-AUDIT", prenom="Test", nom="Synthétique", email="fixture@example.invalid", telephone="0612345678", type_personne="individu", consentement_rgpd=True)
        item = AuditReponse.objects.create(dossier=dossier, reponses={"fixture": 5}, scores_series={}, score_global=5, pilier_faible="Test")
        first = item.signature_hash
        self.assertTrue(item.signature_is_valid())
        item.refresh_from_db()
        self.assertTrue(item.signature_is_valid())
        item.reponses = {"fixture": 8}
        self.assertFalse(item.signature_is_valid())
        item.save()
        self.assertNotEqual(item.signature_hash, first)
        self.assertTrue(item.signature_is_valid())
        with override_settings(AUDIT_SIGNATURE_KEY=""), self.assertRaises(RuntimeError):
            item.reponses = {"fixture": 9}
            item.save()
        item.refresh_from_db()
        self.assertEqual(item.reponses, {"fixture": 8})

    def test_admin_login_throttled_without_forwarded_spoof(self):
        client = Client()
        for _ in range(10):
            self.assertEqual(client.post("/admin/login/", {"username": "synthetic", "password": "invalid"}, HTTP_X_FORWARDED_FOR="198.51.100.1").status_code, 200)
        self.assertEqual(client.post("/admin/login/", {}, HTTP_X_FORWARDED_FOR="198.51.100.2").status_code, 429)

    def test_personal_operator_has_no_password_or_account_management_permission(self):
        call_command("provision_operator", username="synthetic-gregory", email="fixture@example.invalid")
        user = get_user_model().objects.get(username="synthetic-gregory")
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.has_usable_password())
        self.assertTrue(user.has_perm("crm.change_contact"))
        self.assertTrue(user.has_perm("crm.add_contactmessage"))
        self.assertFalse(user.has_perm("auth.change_user"))
        self.assertFalse(user.has_perm("audits.change_auditreponse"))
        self.assertFalse(user.has_perm("crm.delete_contact"))


class ConcurrentOperationsTests(TransactionTestCase):
    def test_same_slot_concurrently_has_exactly_one_booking_and_db_guard(self):
        motif = Motif.objects.create(nom="Synthetic concurrent booking", duree_minutes=60)
        barrier = Barrier(2)
        slot = {"date": "2043-04-06", "heure_debut": "09:00", "heure_fin": "10:00"}
        def book(i):
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                reserve_rdv(motif=motif, slot=slot, contact_data={"prenom": "Synthetic", "nom": "Concurrent", "email": f"thread-{i}@example.invalid", "telephone": "0612345678"}, raison_ids=[], urgence=False)
                return "reserved"
            except ValueError:
                return "refused"
            finally:
                close_old_connections()
        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertCountEqual(list(pool.map(book, [1, 2])), ["reserved", "refused"])
        self.assertEqual(Rdv.objects.count(), 1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            CreneauCalendrier.objects.create(date="2043-04-06", heure_debut="09:30", heure_fin="10:30", statut="bloque")
        reminder = RdvRappel.objects.first()
        reminder.scheduled_at = timezone.now() - timedelta(seconds=10)
        reminder.save(update_fields=["scheduled_at"])
        before = Notification.objects.count()
        self.assertEqual(send_due_reminders(), 1)
        self.assertEqual(send_due_reminders(), 0)
        self.assertEqual(Notification.objects.count(), before + 1)

    def test_outbox_two_workers_cannot_claim_same_event(self):
        enqueue(event_key="synthetic:concurrent", subject="Synthetic", message="Fixture", from_email="fixture@example.invalid", recipient_list=["fixture@example.invalid"])
        barrier = Barrier(2)
        def worker(_):
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                item = claim()
                return item.pk if item else None
            finally:
                close_old_connections()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(worker, [1, 2]))
        self.assertEqual(sum(r is not None for r in results), 1)
