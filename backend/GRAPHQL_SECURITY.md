# Frontière de sécurité GraphQL

`/graphql/` est un endpoint public, anonyme et sans état. Il n'utilise pas la
session Django comme mécanisme d'autorisation. Django Admin est l'unique
interface de gestion et aucune opération de back-office n'est publiée dans le
schéma GraphQL.

## Inventaire public

| Opération | Classe / resolver | App | Classification | Limitation | Consommateur prouvé |
|---|---|---|---|---|---|
| `citationAleatoire` | `Query.resolve_citation_aleatoire` | audits | `PUBLIC_ANONYMOUS_REQUIRED` | aucune | `CitationScreen.vue` |
| `motifs` | `Query.resolve_motifs` | audits | `PUBLIC_ANONYMOUS_REQUIRED` | aucune | `rendez-vous.vue` |
| `raisonsAppel` | `Query.resolve_raisons_appel` | audits | `PUBLIC_ANONYMOUS_REQUIRED` | aucune | `rendez-vous.vue` |
| `refonteAudit` | `Query.resolve_refonte_audit` | audits | `PUBLIC_ANONYMOUS_REQUIRED` par référence-capacité | 30 / 15 min / IP | résultat de l'audit refonte |
| `creneauxDisponibles` | `Query.resolve_creneaux_disponibles` | audits | `PUBLIC_ANONYMOUS_REQUIRED` | aucune | `rendez-vous.vue` |
| `calendrierMois` | `Query.resolve_calendrier_mois` | audits | `PUBLIC_ANONYMOUS_REQUIRED` | aucune | `rendez-vous.vue` |
| `availableMachines` | `Query.resolve_available_machines` | catalogue | `PUBLIC_ANONYMOUS_REQUIRED` | curseur opaque, 20 par défaut, maximum 50 | futur catalogue public |
| `refurbishedMachine` | `Query.resolve_refurbished_machine` | catalogue | `PUBLIC_ANONYMOUS_REQUIRED` | uniquement les publications actuelles non archivées | future fiche machine |
| `contactByToken` | `Query.resolve_contact_by_token` | crm | `PUBLIC_ANONYMOUS_REQUIRED` par jeton-capacité | 30 / 15 min / IP | suivi de ticket |
| `diagnosticTicket` | `Query.resolve_diagnostic_ticket` | crm | `PUBLIC_ANONYMOUS_REQUIRED` par identifiant-capacité | 30 / 15 min / IP | résultat du diagnostic |
| `createContact` | `CreateContact` | crm | `PUBLIC_ANONYMOUS_REQUIRED` | 5 / 10 min / IP | formulaire de contact |
| `addContactMessage` | `AddContactMessage` | crm | `PUBLIC_ANONYMOUS_REQUIRED` par jeton-capacité | 30 / 15 min / IP | suivi de ticket |
| `createDiagnosticTicket` | `CreateDiagnosticTicket` | crm | `PUBLIC_ANONYMOUS_REQUIRED` | aucune | pré-diagnostic |
| `createUrgencyRequest` | `CreateUrgencyRequest` | urgencies | `PUBLIC_ANONYMOUS_REQUIRED` | 5 / 15 min / IP | formulaire urgence |
| `createAuditDossier` | `CreateAuditDossier` | audits | `PUBLIC_ANONYMOUS_REQUIRED` | 8 / 15 min / IP | audit public |
| `submitAuditReponses` | `SubmitAuditReponses` | audits | `PUBLIC_ANONYMOUS_REQUIRED` par numéro | 12 / 15 min / IP | audit public |
| `createRefonteAudit` | `CreateRefonteAudit` | audits | `PUBLIC_ANONYMOUS_REQUIRED` | 6 / 15 min / IP | audit refonte |
| `createRdvReservation` | `CreateRdvReservation` | audits | `PUBLIC_ANONYMOUS_REQUIRED` | validation de créneau | rendez-vous |
| `sessionInit` | `SessionInit` | tracking | `PUBLIC_ANONYMOUS_REQUIRED` | plafond partagé 60 / min / IP | intégration de suivi |
| `recordPageView` | `RecordPageView` | tracking | `PUBLIC_ANONYMOUS_REQUIRED` | plafond partagé 60 / min / IP | intégration de suivi |
| `recordQuestionInteraction` | `RecordQuestionInteraction` | tracking | `PUBLIC_ANONYMOUS_REQUIRED` | plafond partagé 60 / min / IP | intégration de suivi |
| `recordTrackingEvent` | `RecordTrackingEvent` | tracking | `PUBLIC_ANONYMOUS_REQUIRED` | plafond partagé 60 / min / IP | intégration de suivi |

Les résultats des mutations de suivi ne retournent que leurs identifiants et
compteurs publics. Les relations de dossier, adresses IP, user-agents et
métadonnées stockées ne sont pas exposés.

Les nouveaux tickets diagnostic et références de refonte utilisent au moins
120 bits aléatoires avant encodage. Les identifiants historiques restent
acceptés pour ne pas invalider les liens déjà remis aux visiteurs ; leur
énumération est freinée par la limitation centralisée et des erreurs génériques.

## Opérations retirées

Les opérations suivantes étaient `DANGEROUS`, `STAFF_ONLY` ou
`UNUSED_OR_UNPROVEN`. Elles ne sont plus des champs du schéma :

- lectures `contacts`, `contact`, `unreadContacts`, `leads`, `lead`,
  `formations`, `formation`, `formationRegistrations`,
  `formationRegistration`, `services`, `service`, `auditDossier` et
  `clientDossier` ;
- mutations `createLead`, `updateLeadStatus`, `createFormation`,
  `createFormationRegistration`, `updateFormationRegistrationStatus`,
  `upsertService` et `deleteCrmObject`.

Leur présence antérieure dans la documentation ou dans un test ne constituait
pas la preuve d'un consommateur produit. Les opérations de gestion passent par
Django Admin.

## CSRF, CORS et sessions

L'exemption CSRF est conservée parce que les formulaires publics envoient du
JSON sans authentification par cookie. CORS n'est pas un contrôle
d'autorisation : un client non navigateur peut appeler l'endpoint et les
requêtes même origine ne dépendent pas de CORS.

La sécurité repose donc sur une liste fermée d'opérations anonymes, des
validations serveur et des réponses minimales. Il est interdit d'ajouter à cet
endpoint une opération staff authentifiée par cookie. Si un consommateur staff
GraphQL est un jour démontré, il devra utiliser un endpoint distinct, protégé
par CSRF et par une autorisation Django centralisée et testée. D'ici là,
Django Admin reste le back-office officiel.
