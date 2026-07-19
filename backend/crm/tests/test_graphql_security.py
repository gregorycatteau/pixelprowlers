import json
import time

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase, override_settings

from crm.contact_services import verify_contact_hmac
from crm.models import Contact, DiagnosticTicket
from audits.serializers import create_refonte_reference
from pixelprowlers.schema import schema


TEST_SETTINGS = {
    "CONTACT_HMAC_SECRET": "test-contact-hmac-secret-at-least-32-characters",
    "EMAIL_BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    "DEFAULT_FROM_EMAIL": "test-sender-do-not-use@pixelprowlers.io",
    "CONTACT_TO": "contact@example.invalid",
    "TRUSTED_PROXY_IPS": set(),
}


@override_settings(**TEST_SETTINGS)
class PublicGraphQLSecurityBoundaryTests(TestCase):
    forbidden_queries = (
        "contacts",
        "contact",
        "unreadContacts",
        "leads",
        "lead",
        "formations",
        "formation",
        "formationRegistrations",
        "formationRegistration",
        "services",
        "service",
        "auditDossier",
        "clientDossier",
    )
    forbidden_mutations = (
        "createLead",
        "updateLeadStatus",
        "createFormation",
        "createFormationRegistration",
        "updateFormationRegistrationStatus",
        "upsertService",
        "deleteCrmObject",
    )

    def setUp(self):
        cache.clear()
        self.client = Client(HTTP_HOST="localhost", REMOTE_ADDR="127.0.0.1")

    def graphql(self, query, variables=None):
        return self.client.post(
            "/graphql/",
            data=json.dumps({"query": query, "variables": variables or {}}),
            content_type="application/json",
        )

    def assert_field_is_not_in_schema(self, operation, field):
        query = f"{operation} {{ {field} {{ __typename }} }}"
        response = self.graphql(query)
        payload = response.json()
        self.assertIsNotNone(payload.get("errors"), payload)
        self.assertFalse(payload.get("data"), payload)
        rendered = json.dumps(payload).lower()
        self.assertNotIn("example.com", rendered)
        self.assertNotIn("secret_token", rendered)

    def test_anonymous_private_queries_are_absent(self):
        for field in self.forbidden_queries:
            with self.subTest(field=field):
                self.assert_field_is_not_in_schema("query", field)

    def test_anonymous_administrative_mutations_are_absent(self):
        for field in self.forbidden_mutations:
            with self.subTest(field=field):
                self.assert_field_is_not_in_schema("mutation", field)

    def test_authenticated_non_staff_and_staff_do_not_gain_a_hidden_backoffice(self):
        user_model = get_user_model()
        for is_staff in (False, True):
            with self.subTest(is_staff=is_staff):
                user = user_model.objects.create_user(
                    username=f"boundary-{is_staff}",
                    password="test-only-password",
                    is_active=True,
                    is_staff=is_staff,
                )
                self.client.force_login(user)
                self.assert_field_is_not_in_schema("query", "contacts")
                self.assert_field_is_not_in_schema("mutation", "deleteCrmObject")
                self.client.logout()

    def test_removed_operations_are_absent_from_schema_introspection(self):
        query_fields = set(schema.graphql_schema.query_type.fields)
        mutation_fields = set(schema.graphql_schema.mutation_type.fields)
        self.assertTrue(set(self.forbidden_queries).isdisjoint(query_fields))
        self.assertTrue(set(self.forbidden_mutations).isdisjoint(mutation_fields))

    def test_capability_scoped_types_use_explicit_public_fields(self):
        graphql_schema = schema.graphql_schema
        self.assertEqual(
            set(graphql_schema.get_type("ContactType").fields),
            {
                "id",
                "ticketId",
                "secretToken",
                "numeroDossier",
                "nom",
                "prenom",
                "name",
                "email",
                "company",
                "phone",
                "serviceType",
                "demandType",
                "objet",
                "methodeContact",
                "status",
                "message",
                "createdAt",
                "updatedAt",
                "demandLabel",
                "messages",
            },
        )
        self.assertEqual(
            set(graphql_schema.get_type("DiagnosticTicketType").fields),
            {
                "id",
                "ticketId",
                "organization",
                "email",
                "phone",
                "message",
                "answers",
                "diagnosticResult",
                "emailConfirmation",
            },
        )

    def test_unlisted_sensitive_fields_cannot_be_queried(self):
        for field, query in (
            ("signatureHmac", "query($token: String!) { contactByToken(token: $token) { signatureHmac } }"),
            ("clientDossier", "query($ticketId: String!) { diagnosticTicket(ticketId: $ticketId) { clientDossier { id } } }"),
        ):
            with self.subTest(field=field):
                response = self.graphql(query, {"token": "invalid", "ticketId": "invalid"})
                self.assertIsNotNone(response.json().get("errors"))
                self.assertFalse(response.json().get("data"))

    def test_create_contact_remains_public_minimal_and_signed(self):
        response = self.graphql(
            """
            mutation CreateContact($startedAt: Float!) {
              createContact(
                nom: "Martin"
                prenom: "Alice"
                email: "boundary@example.invalid"
                company: "Association Exemple"
                telephone: "0612345678"
                objet: "Qualification matérielle"
                methodeContact: "email"
                serviceType: "materiel"
                demandType: "partnership"
                message: "Nous souhaitons qualifier un besoin matériel avant toute intervention."
                privacyConsent: true
                startedAt: $startedAt
              ) {
                success
                numeroDossier
                message
              }
            }
            """,
            {"startedAt": int((time.time() - 5) * 1000)},
        )
        payload = response.json()
        self.assertIsNone(payload.get("errors"), payload)
        result = payload["data"]["createContact"]
        self.assertEqual(set(result), {"success", "numeroDossier", "message"})
        self.assertTrue(result["success"])
        contact = Contact.objects.get()
        self.assertEqual(contact.service_type, "materiel")
        self.assertTrue(verify_contact_hmac(contact))

    def test_malformed_and_enumeration_attempts_reveal_no_private_data(self):
        for query in (
            "query { contact(id: 999999) { email } }",
            "query { lead(id: 999999) { email } }",
            "mutation { updateLeadStatus(id: 999999, status: \"closed\") { __typename } }",
            "mutation { deleteCrmObject(model: \"contact\", id: 999999) { ok } }",
        ):
            with self.subTest(query=query):
                payload = self.graphql(query).json()
                self.assertIsNotNone(payload.get("errors"), payload)
                self.assertFalse(payload.get("data"), payload)
                self.assertNotIn("example.invalid", json.dumps(payload))

    def test_capability_identifiers_have_sufficient_entropy_for_new_records(self):
        ticket = DiagnosticTicket.objects.create(
            organization="Security Probe",
            email="probe@example.invalid",
            message="Synthetic security test",
        )
        self.assertGreaterEqual(len(ticket.ticket_id.removeprefix("PP-")), 24)
        self.assertGreaterEqual(len(create_refonte_reference().removeprefix("PXP-")), 20)

    def test_capability_lookups_are_rate_limited_with_generic_errors(self):
        query = "query($ticketId: String!) { diagnosticTicket(ticketId: $ticketId) { ticketId } }"
        for index in range(31):
            response = self.graphql(query, {"ticketId": f"missing-{index}"})
        payload = response.json()
        self.assertEqual(payload["errors"][0]["message"], "Ressource indisponible.")
        self.assertIsNone(payload["data"]["diagnosticTicket"])
