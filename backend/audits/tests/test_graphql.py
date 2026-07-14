import json
import time
from datetime import timedelta
from unittest import mock

from django.test import Client, TestCase, override_settings
from django.core.cache import cache
from django.urls import get_resolver
from django.utils import timezone

from audits.models import AuditDossier, AuditReponse, ClientDossier, DossierLog, Motif, RaisonAppel
from audits.questions import QUESTION_IDS
from audits.refonte_questions import REFONTE_QUESTION_IDS
from crm.models import Contact, ContactMessage, DiagnosticTicket, Formation, FormationRegistration, Lead, Service
from tracking.models import TrackingEvent, VisitorSession
from urgencies.models import UrgencyRequest


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="test@example.com",
    CONTACT_TO="test@example.com",
    CONTACT_HMAC_SECRET="test-contact-hmac-secret-at-least-32-characters",
    CORS_ALLOWED_ORIGINS=["http://localhost:3000"],
    AUDIT_INTERNAL_EMAIL="test@example.com",
    URGENCY_INTERNAL_EMAIL="test@example.com",
)
class GraphQLSmokeTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client(HTTP_HOST="localhost")

    def graphql(self, query, variables=None, **headers):
        payload = {"query": query}
        if variables is not None:
            payload["variables"] = variables
        response = self.client.post(
            "/graphql/",
            data=json.dumps(payload),
            content_type="application/json",
            **headers,
        )
        return response

    def test_create_audit_dossier_and_submit_reponses(self):
        create = self.graphql(
            """
            mutation {
              createAuditDossier(
                prenom: "Alice"
                nom: "Martin"
                email: "alice@example.com"
                telephone: "0612345678"
                typePersonne: "individu"
                consentementRgpd: true
              ) {
                dossier {
                  numeroDossier
                  statut
                  clientDossier {
                    dossierId
                    phase
                  }
                }
              }
            }
            """,
        )
        self.assertEqual(create.status_code, 200)
        self.assertIsNone(create.json().get("errors"))
        numero_dossier = create.json()["data"]["createAuditDossier"]["dossier"]["numeroDossier"]
        client_dossier_id = create.json()["data"]["createAuditDossier"]["dossier"]["clientDossier"]["dossierId"]
        self.assertRegex(client_dossier_id, r"^\d{7}-0$")

        submit = self.graphql(
            """
            mutation Submit($numeroDossier: String!, $reponses: JSONString!) {
              submitAuditReponses(numeroDossier: $numeroDossier, reponses: $reponses) {
                numeroDossier
                statut
                scoreGlobal
              }
            }
            """,
            variables={
                "numeroDossier": numero_dossier,
                "reponses": json.dumps({question_id: 5 for question_id in QUESTION_IDS}),
            },
            HTTP_USER_AGENT="TestAgent/1.0",
            REMOTE_ADDR="127.0.0.42",
        )
        self.assertEqual(submit.status_code, 200)
        self.assertIsNone(submit.json().get("errors"))
        self.assertEqual(submit.json()["data"]["submitAuditReponses"]["statut"], "questionnaire_complété")

        dossier = AuditDossier.objects.get(numero_dossier=numero_dossier)
        reponse = AuditReponse.objects.get(dossier=dossier)
        self.assertEqual(reponse.ip_address, "127.0.0.42")
        self.assertEqual(reponse.user_agent, "TestAgent/1.0")
        dossier.client_dossier.refresh_from_db()
        self.assertEqual(dossier.client_dossier.phase, ClientDossier.Phase.DIAGNOSTIC)
        self.assertRegex(dossier.client_dossier.dossier_id, r"^\d{7}-1$")
        self.assertTrue(DossierLog.objects.filter(dossier=dossier.client_dossier, old_phase=0, new_phase=1).exists())

    def test_audit_create_rate_limit_is_enforced_on_mutation(self):
        last_response = None
        for index in range(9):
            last_response = self.graphql(
                """
                mutation {
                  createAuditDossier(
                    prenom: "Alice"
                    nom: "Martin"
                    email: "alice@example.com"
                    telephone: "0612345678"
                    typePersonne: "individu"
                    consentementRgpd: true
                  ) {
                    dossier {
                      numeroDossier
                    }
                  }
                }
                """,
                HTTP_X_FORWARDED_FOR="198.51.100.10",
            )

        self.assertEqual(last_response.status_code, 200)
        self.assertIsNotNone(last_response.json().get("errors"))
        self.assertIn("Trop de demandes en peu de temps", last_response.json()["errors"][0]["message"])

    def test_create_refonte_and_reservation_queries(self):
        motif = Motif.objects.create(nom="Consultation GraphQL", duree_minutes=60, creneau_type="horaire_precis", actif=True, ordre=999)
        raison = RaisonAppel.objects.create(nom="Besoin GraphQL", actif=True, ordre=999)

        refonte = self.graphql(
            """
            mutation CreateRefonte($reponses: JSONString!) {
              createRefonteAudit(
                prenom: "Alice"
                nom: "Martin"
                email: "alice@example.com"
                telephone: "0612345678"
                typePersonne: "individu"
                siteUrl: "https://example.com"
                consentementRgpd: true
                reponses: $reponses
              ) {
                audit {
                  reference
                  analysisStatus
                  clientDossier {
                    dossierId
                    phase
                  }
                }
              }
            }
            """,
            variables={"reponses": json.dumps({question_id: "ok" for question_id in REFONTE_QUESTION_IDS})},
        )
        self.assertEqual(refonte.status_code, 200)
        self.assertIsNone(refonte.json().get("errors"))
        reference = refonte.json()["data"]["createRefonteAudit"]["audit"]["reference"]
        self.assertRegex(refonte.json()["data"]["createRefonteAudit"]["audit"]["clientDossier"]["dossierId"], r"^\d{7}-1$")

        query = self.graphql(
            """
            query($reference: String!) {
              refonteAudit(reference: $reference) {
                reference
                analysisStatus
              }
            }
            """,
            variables={"reference": reference},
        )
        self.assertEqual(query.status_code, 200)
        self.assertIsNone(query.json().get("errors"))
        self.assertEqual(query.json()["data"]["refonteAudit"]["reference"], reference)

        tomorrow = (timezone.localdate() + timedelta(days=1)).isoformat()
        rdv = self.graphql(
            f"""
            mutation {{
              createRdvReservation(
                motifId: {motif.id}
                date: "{tomorrow}"
                heureDebut: "09:00"
                heureFin: "10:00"
                urgence: false
                prenom: "Alice"
                nom: "Martin"
                email: "alice@example.com"
                telephone: "0612345678"
                raisonIds: [{raison.id}]
                message: ""
              ) {{
                rdv {{
                  id
                  statut
                  clientDossier {{
                    dossierId
                    phase
                  }}
                }}
              }}
            }}
            """
        )
        self.assertEqual(rdv.status_code, 200)
        self.assertIsNone(rdv.json().get("errors"))
        self.assertRegex(rdv.json()["data"]["createRdvReservation"]["rdv"]["clientDossier"]["dossierId"], r"^\d{7}-2$")

    def test_tracking_and_urgency_mutations(self):
        session = self.graphql(
            """
            mutation {
              sessionInit(
                sessionId: "44444444-4444-4444-4444-444444444444"
                referrer: "https://example.com"
                language: "fr"
              ) {
                sessionId
                session {
                  clientDossier {
                    dossierId
                    phase
                  }
                }
              }
            }
            """,
        )
        self.assertEqual(session.status_code, 200)
        self.assertIsNone(session.json().get("errors"))
        self.assertRegex(session.json()["data"]["sessionInit"]["session"]["clientDossier"]["dossierId"], r"^\d{7}-0$")

        pageview = self.graphql(
            """
            mutation {
              recordPageView(
                sessionId: "44444444-4444-4444-4444-444444444444"
                url: "https://example.com"
                title: "Home"
              ) {
                pageviewId
              }
            }
            """,
        )
        self.assertEqual(pageview.status_code, 200)
        self.assertIsNone(pageview.json().get("errors"))

        interaction = self.graphql(
            """
            mutation {
              recordQuestionInteraction(
                sessionId: "44444444-4444-4444-4444-444444444444"
                questionId: "q1"
                serie: "s1"
                timeSpentSeconds: 12.5
                revisitCount: 0
                orderIndex: 1
              ) {
                interactionId
                revisitCount
              }
            }
            """,
        )
        self.assertEqual(interaction.status_code, 200)
        self.assertIsNone(interaction.json().get("errors"))

        event = self.graphql(
            """
            mutation {
              recordTrackingEvent(
                sessionId: "44444444-4444-4444-4444-444444444444"
                eventType: "cta_click"
                pageUrl: "https://example.com"
                metadata: "{}"
              ) {
                eventId
              }
            }
            """,
        )
        self.assertEqual(event.status_code, 200)
        self.assertIsNone(event.json().get("errors"))

        urgency = self.graphql(
            """
            mutation {
              createUrgencyRequest(
                problemType: "site_down"
                impactLevel: "blocked"
                affectedUrl: "https://example.com"
                shortDescription: "Site down"
                sinceWhen: "now"
                name: "Alice"
                organization: "ACME"
                email: "alice@example.com"
                phone: "0612345678"
                contactPreference: "email"
                callbackSlot: "asap"
                expectedNextStep: "quick_callback"
                consentToContact: true
                noSecretsConfirmed: true
              ) {
                reference
                status
                clientEmailStatus
                ticket {
                  notificationStatus
                  clientDossier {
                    dossierId
                    phase
                  }
                }
              }
            }
            """,
        )
        self.assertEqual(urgency.status_code, 200)
        self.assertIsNone(urgency.json().get("errors"))
        self.assertEqual(urgency.json()["data"]["createUrgencyRequest"]["status"], "open")
        notification_status = json.loads(urgency.json()["data"]["createUrgencyRequest"]["ticket"]["notificationStatus"])
        self.assertEqual(notification_status["internal_sms"], "dry_run")
        self.assertEqual(notification_status["webhook"], "not_configured")
        self.assertRegex(urgency.json()["data"]["createUrgencyRequest"]["ticket"]["clientDossier"]["dossierId"], r"^\d{7}-0$")

        self.assertTrue(VisitorSession.objects.filter(session_id="44444444-4444-4444-4444-444444444444").exists())
        self.assertTrue(TrackingEvent.objects.filter(event_type="cta_click").exists())
        self.assertTrue(UrgencyRequest.objects.filter(status="open").exists())

    def test_email_failure_does_not_fail_audit_submission(self):
        create = self.graphql(
            """
            mutation {
              createAuditDossier(
                prenom: "Alice"
                nom: "Martin"
                email: "email-fail@example.com"
                telephone: "0612345678"
                typePersonne: "individu"
                consentementRgpd: true
              ) {
                dossier {
                  numeroDossier
                }
              }
            }
            """,
        )
        self.assertEqual(create.status_code, 200)
        self.assertIsNone(create.json().get("errors"))
        numero_dossier = create.json()["data"]["createAuditDossier"]["dossier"]["numeroDossier"]

        with mock.patch("pixelprowlers.notifications.send_mail", side_effect=RuntimeError("smtp down")):
            submit = self.graphql(
                """
                mutation Submit($numeroDossier: String!, $reponses: JSONString!) {
                  submitAuditReponses(numeroDossier: $numeroDossier, reponses: $reponses) {
                    numeroDossier
                    notificationStatus
                  }
                }
                """,
                variables={
                    "numeroDossier": numero_dossier,
                    "reponses": json.dumps({question_id: 5 for question_id in QUESTION_IDS}),
                },
            )

        self.assertEqual(submit.status_code, 200)
        self.assertIsNone(submit.json().get("errors"))
        status = json.loads(submit.json()["data"]["submitAuditReponses"]["notificationStatus"])
        self.assertEqual(status["internal_email"], "failed")
        self.assertEqual(status["client_email"], "failed")

    def test_tracking_rejects_suspicious_payload(self):
        response = self.graphql(
            """
            mutation {
              sessionInit(
                sessionId: "55555555-5555-5555-5555-555555555555"
                referrer: "<script>"
              ) {
                sessionId
              }
            }
            """,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json().get("errors"))

    def test_crm_graphql_replaces_legacy_rest_domains(self):
        started_at = int((time.time() - 5) * 1000)
        contact = self.graphql(
            """
            mutation CreateContact($startedAt: Float!) {
              createContact(
                nom: "Martin"
                prenom: "Alice"
                email: "crm-contact@example.com"
                company: "ACME"
                telephone: "0612345678"
                objet: "Audit avant refonte"
                methodeContact: "email"
                serviceType: "audit_site"
                message: "Nous voulons faire auditer notre site avant une refonte."
                structureType: "TPE"
                urgency: "Projet à cadrer"
                contactPreference: "Email"
                backups: "Oui, mais jamais testée"
                access: "Accès partiels"
                privacyConsent: true
                startedAt: $startedAt
              ) {
                success
                numeroDossier
                message
              }
            }
            """,
            variables={"startedAt": started_at},
        )
        self.assertEqual(contact.status_code, 200)
        self.assertIsNone(contact.json().get("errors"))
        self.assertEqual(Contact.objects.count(), 1)
        created_contact = Contact.objects.get()
        self.assertRegex(created_contact.client_dossier.dossier_id, r"^\d{7}-0$")

        lead = self.graphql(
            """
            mutation {
              createLead(
                name: "Bob"
                email: "lead@example.com"
                phone: "0612345678"
                budget: "1500"
                projectDescription: "Créer une application métier maintenable."
                timeline: "Q3"
                leadType: "developpement"
              ) {
                lead { id leadType status clientDossier { dossierId } }
              }
            }
            """,
        )
        self.assertEqual(lead.status_code, 200)
        self.assertIsNone(lead.json().get("errors"))
        lead_id = lead.json()["data"]["createLead"]["lead"]["id"]
        self.assertTrue(Lead.objects.filter(pk=lead_id).exists())

        formation = self.graphql(
            """
            mutation {
              createFormation(
                title: "Hygiène numérique"
                description: "Formation d'équipe"
                formatType: "presentiel"
                durationHours: 7
                price: "490.00"
                maxParticipants: 8
                scheduledDates: "[]"
              ) {
                formation { id title formatType }
              }
            }
            """,
        )
        self.assertEqual(formation.status_code, 200)
        self.assertIsNone(formation.json().get("errors"))
        formation_id = formation.json()["data"]["createFormation"]["formation"]["id"]

        registration = self.graphql(
            """
            mutation Register($formationId: ID!) {
              createFormationRegistration(
                formationId: $formationId
                name: "Claire"
                email: "formation@example.com"
                phone: "0612345678"
                numberOfParticipants: 2
              ) {
                registration { id status clientDossier { dossierId } }
              }
            }
            """,
            variables={"formationId": formation_id},
        )
        self.assertEqual(registration.status_code, 200)
        self.assertIsNone(registration.json().get("errors"))
        self.assertEqual(FormationRegistration.objects.count(), 1)

        service = self.graphql(
            """
            mutation {
              upsertService(
                slug: "audit-site"
                name: "Audit site"
                description: "Audit de présence web"
                serviceCategory: "developpement"
                order: 1
              ) {
                service { slug serviceCategory }
              }
            }
            """,
        )
        self.assertEqual(service.status_code, 200)
        self.assertIsNone(service.json().get("errors"))
        self.assertTrue(Service.objects.filter(slug="audit-site").exists())

        query = self.graphql(
            """
            query {
              contacts(serviceType: "audit_site") { id }
              leads(leadType: "developpement") { id }
              formations(formatType: "presentiel") { id }
              formationRegistrations(formationId: 1) { id }
              services(serviceCategory: "developpement") { slug }
            }
            """,
        )
        self.assertEqual(query.status_code, 200)
        self.assertIsNone(query.json().get("errors"))
        self.assertEqual(len(query.json()["data"]["contacts"]), 1)

    def test_contact_ticket_flow_is_graphql_only(self):
        started_at = int((time.time() - 5) * 1000)
        created = self.graphql(
            """
            mutation CreateContact($startedAt: Float!) {
              createContact(
                nom: "Client"
                prenom: "Ticket"
                email: "ticket@example.com"
                company: "Ticket Org"
                telephone: "0612345678"
                objet: "Demande audit"
                methodeContact: "email"
                serviceType: "audit_site"
                demandType: "audit"
                message: "Nous avons besoin d'un suivi clair pour notre demande d'audit."
                privacyConsent: true
                startedAt: $startedAt
              ) {
                success
                numeroDossier
                message
              }
            }
            """,
            variables={"startedAt": started_at},
        )
        self.assertEqual(created.status_code, 200)
        self.assertIsNone(created.json().get("errors"))
        contact_data = created.json()["data"]["createContact"]
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertTrue(contact_data["success"])
        tracking_token = Contact.objects.get().secret_token
        self.assertEqual(ContactMessage.objects.get().author, ContactMessage.Author.CUSTOMER)

        loaded = self.graphql(
            """
            query ContactByToken($token: String!) {
              contactByToken(token: $token) {
                ticketId
                email
                messages { message }
              }
            }
            """,
            variables={"token": tracking_token},
        )
        self.assertEqual(loaded.status_code, 200)
        self.assertIsNone(loaded.json().get("errors"))
        self.assertEqual(loaded.json()["data"]["contactByToken"]["ticketId"], contact_data["numeroDossier"])

        replied = self.graphql(
            """
            mutation AddContactMessage($token: String!) {
              addContactMessage(
                token: $token
                message: "Voici une précision côté client."
                authorName: "Ticket Org"
              ) {
                contact {
                  status
                  messages { message }
                }
              }
            }
            """,
            variables={"token": tracking_token},
        )
        self.assertEqual(replied.status_code, 200)
        self.assertIsNone(replied.json().get("errors"))
        self.assertEqual(ContactMessage.objects.count(), 2)
        self.assertEqual(replied.json()["data"]["addContactMessage"]["contact"]["status"], "WAITING_CUSTOMER")

    def test_diagnostic_ticket_flow_is_graphql_only(self):
        created = self.graphql(
            """
            mutation CreateDiagnosticTicket($answers: JSONString!) {
              createDiagnosticTicket(
                organization: "Diagnostic Org"
                email: "diagnostic@example.com"
                phone: "0612345678"
                message: "Nous voulons comprendre les priorités."
                answers: $answers
              ) {
                redirectTo
                ticket {
                  id
                  ticketId
                  diagnosticResult
                  emailConfirmation
                  clientDossier { dossierId phase }
                }
              }
            }
            """,
            variables={"answers": json.dumps({"stress": "site-slow", "siteState": "fragile", "dependency": "one"})},
        )
        self.assertEqual(created.status_code, 200)
        self.assertIsNone(created.json().get("errors"))
        ticket_data = created.json()["data"]["createDiagnosticTicket"]["ticket"]
        self.assertTrue(created.json()["data"]["createDiagnosticTicket"]["redirectTo"].endswith(ticket_data["ticketId"]))
        self.assertEqual(DiagnosticTicket.objects.count(), 1)
        self.assertRegex(ticket_data["clientDossier"]["dossierId"], r"^\d{7}-1$")
        self.assertEqual(DiagnosticTicket.objects.get().client_dossier.phase, ClientDossier.Phase.DIAGNOSTIC)

        loaded = self.graphql(
            """
            query DiagnosticTicket($ticketId: String!) {
              diagnosticTicket(ticketId: $ticketId) {
                id
                organization
                answers
                diagnosticResult
              }
            }
            """,
            variables={"ticketId": ticket_data["ticketId"]},
        )
        self.assertEqual(loaded.status_code, 200)
        self.assertIsNone(loaded.json().get("errors"))
        self.assertEqual(loaded.json()["data"]["diagnosticTicket"]["id"], ticket_data["ticketId"])

    def test_top_level_urls_are_admin_health_graphql_only(self):
        patterns = {str(pattern.pattern) for pattern in get_resolver().url_patterns}
        self.assertEqual(patterns, {"admin/", "health/", "graphql/"})
        self.assertEqual(self.client.get("/health/").json(), {"status": "ok"})

    def test_graphql_preflight_allows_configured_origin(self):
        response = self.client.options(
            "/graphql/",
            HTTP_ORIGIN="http://localhost:3000",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "http://localhost:3000")
        self.assertIn("POST", response.headers.get("Access-Control-Allow-Methods", ""))
        self.assertEqual(response.headers.get("Access-Control-Allow-Credentials"), None)

    def test_graphql_preflight_rejects_untrusted_origin(self):
        response = self.client.options(
            "/graphql/",
            HTTP_ORIGIN="http://evil.example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.headers.get("Access-Control-Allow-Origin"))
