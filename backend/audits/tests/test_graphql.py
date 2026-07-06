import json
from datetime import timedelta

from django.test import Client, TestCase, override_settings
from django.core.cache import cache
from django.utils import timezone

from audits.models import AuditDossier, AuditReponse, Motif, RaisonAppel
from audits.questions import QUESTION_IDS
from audits.refonte_questions import REFONTE_QUESTION_IDS
from tracking.models import TrackingEvent, VisitorSession
from urgencies.models import UrgencyRequest


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="test@example.com",
    CONTACT_TO="test@example.com",
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
                }
              }
            }
            """,
        )
        self.assertEqual(create.status_code, 200)
        self.assertIsNone(create.json().get("errors"))
        numero_dossier = create.json()["data"]["createAuditDossier"]["dossier"]["numeroDossier"]

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
                }
              }
            }
            """,
            variables={"reponses": json.dumps({question_id: "ok" for question_id in REFONTE_QUESTION_IDS})},
        )
        self.assertEqual(refonte.status_code, 200)
        self.assertIsNone(refonte.json().get("errors"))
        reference = refonte.json()["data"]["createRefonteAudit"]["audit"]["reference"]

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
                }}
              }}
            }}
            """
        )
        self.assertEqual(rdv.status_code, 200)
        self.assertIsNone(rdv.json().get("errors"))

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
              }
            }
            """,
        )
        self.assertEqual(session.status_code, 200)
        self.assertIsNone(session.json().get("errors"))

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
              }
            }
            """,
        )
        self.assertEqual(urgency.status_code, 200)
        self.assertIsNone(urgency.json().get("errors"))
        self.assertEqual(urgency.json()["data"]["createUrgencyRequest"]["status"], "open")

        self.assertTrue(VisitorSession.objects.filter(session_id="44444444-4444-4444-4444-444444444444").exists())
        self.assertTrue(TrackingEvent.objects.filter(event_type="cta_click").exists())
        self.assertTrue(UrgencyRequest.objects.filter(status="open").exists())

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
