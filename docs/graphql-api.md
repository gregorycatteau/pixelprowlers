# API GraphQL PixelProwlers

Endpoint : `POST /graphql/`

Le frontend Nuxt lit `NUXT_PUBLIC_GRAPHQL_API_URL` et retombe sur `/graphql/`. Le backend Django lit son schéma depuis `pixelprowlers.schema.schema`.

## Queries principales

```graphql
query {
  citationAleatoire {
    id
    texte
    auteur
    source
  }
}
```

```graphql
query {
  clientDossier(dossierId: "2607001-0") {
    dossierId
    phase
    email
    logs {
      oldPhase
      newPhase
      timestamp
    }
  }
}
```

```graphql
query {
  refonteAudit(reference: "REF-...") {
    reference
    analysisStatus
    clientDossier {
      dossierId
      phase
    }
  }
}
```

```graphql
query {
  auditDossier(numeroDossier: "AUD-2026-000001") {
    numeroDossier
    statut
    clientDossier {
      dossierId
      phase
    }
  }
}
```

## Mutations audit

```graphql
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
```

```graphql
mutation Submit($numeroDossier: String!, $reponses: JSONString!) {
  submitAuditReponses(numeroDossier: $numeroDossier, reponses: $reponses) {
    numeroDossier
    statut
    scoreGlobal
    notificationStatus
  }
}
```

`reponses` doit contenir toutes les réponses attendues sous forme de JSON string, avec des valeurs entières de `0` à `10`.
La soumission complète fait passer le dossier client de la phase `0` à `1`.

## Mutation urgence

```graphql
mutation {
  createUrgencyRequest(
    problemType: "site_down"
    impactLevel: "blocked"
    affectedUrl: "https://example.com"
    shortDescription: "Site inaccessible"
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
```

Le backend envoie les emails si `DEFAULT_FROM_EMAIL`/`CONTACT_FROM` et `URGENCY_INTERNAL_EMAIL` ou `CONTACT_TO` sont configurés. Pour les impacts `blocked` et `security_data_risk`, `notificationStatus.internal_sms` passe par le service SMS. Par défaut `SMS_DRY_RUN=true`, donc aucun crédit SMS n'est consommé. Le webhook utilise `WEBHOOK_URL` ou `URGENCY_WEBHOOK_URL` si configuré ; sinon le statut vaut `not_configured`.

## Mutation refonte

```graphql
mutation CreateRefonte($reponses: JSONString!) {
  createRefonteAudit(
    prenom: "Alice"
    nom: "Martin"
    email: "alice@example.com"
    telephone: "0612345678"
    typePersonne: "individu"
    siteUrl: "https://example.com"
    reponses: $reponses
    consentementRgpd: true
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
```

## Mutation rendez-vous

```graphql
mutation {
  createRdvReservation(
    motifId: 1
    date: "2026-07-08"
    heureDebut: "09:00"
    heureFin: "10:00"
    prenom: "Alice"
    nom: "Martin"
    email: "alice@example.com"
    telephone: "0612345678"
    raisonIds: [1]
    urgence: false
  ) {
    rdv {
      id
      statut
      clientDossier {
        dossierId
        phase
      }
    }
  }
}
```

## Tracking

Mutations disponibles : `sessionInit`, `recordPageView`, `recordQuestionInteraction`, `recordTrackingEvent`.

`sessionInit` crée un dossier client anonyme rattaché à la session. Les pageviews et events restent rattachés à la session pour éviter de créer un dossier par événement.

```graphql
mutation {
  sessionInit(sessionId: "44444444-4444-4444-4444-444444444444") {
    sessionId
    session {
      clientDossier {
        dossierId
        phase
      }
    }
  }
}
```

## Notifications

Champs de statut typiques dans `notificationStatus` :

```json
{
  "internal_email": "sent|failed|not_configured",
  "client_email": "sent|failed|not_configured",
  "internal_sms": "dry_run|sent|failed|skipped|not_configured",
  "webhook": "sent|failed|not_configured"
}
```

Variables SMS/webhook backend :

- `SMS_DRY_RUN=true` par défaut.
- `INTERNAL_SMS_TO` destinataire interne optionnel ; sinon l'urgence utilise le téléphone client pour le dry-run.
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER` pour l'envoi réel.
- `WEBHOOK_URL` ou `URGENCY_WEBHOOK_URL`, avec `WEBHOOK_TOKEN` ou `URGENCY_WEBHOOK_TOKEN` si besoin.

## CRM GraphQL

Les anciennes routes REST/DRF `contacts/`, `leads/`, `formations/`, `registrations` et `services`, ainsi que les anciens handlers Nitro `/api/contact` et `/api/diagnostic`, sont remplacés par les queries/mutations GraphQL ci-dessous.

### Contacts

```graphql
query {
  contacts(serviceType: "audit_site", read: false) {
    id
    ticketId
    secretToken
    name
    email
    status
    demandType
    demandLabel
    serviceType
    read
    messages {
      author
      authorName
      message
      createdAt
    }
    clientDossier {
      dossierId
    }
  }
}
```

```graphql
query {
  contact(id: 1) {
    id
    ticketId
    email
    status
    clientDossier {
      dossierId
    }
  }
}
```

```graphql
query {
  unreadContacts {
    id
    name
    email
    serviceType
  }
}
```

```graphql
mutation CreateContact($startedAt: Float!) {
  createContact(
    name: "Alice Martin"
    email: "alice@example.com"
    company: "ACME"
    phone: "0612345678"
    serviceType: "audit_site"
    demandType: "audit"
    message: "Nous voulons faire auditer notre site avant une refonte."
    structureType: "TPE"
    urgency: "Projet à cadrer"
    contactPreference: "Email"
    backups: "Oui, mais jamais testée"
    access: "Accès partiels"
    privacyConsent: true
    startedAt: $startedAt
  ) {
    detail
    contact {
      id
      ticketId
      secretToken
      status
      demandLabel
      emailConfirmation
      notificationStatus
      messages {
        author
        message
      }
      clientDossier {
        dossierId
      }
    }
  }
}
```

`websiteCompany` est le honeypot. `startedAt` est un timestamp navigateur en millisecondes ; les soumissions trop rapides sont ignorées avec un message neutre.

Lecture et réponse d'un ticket contact :

```graphql
query ContactByToken($token: String!) {
  contactByToken(token: $token) {
    ticketId
    secretToken
    email
    status
    messages {
      author
      authorName
      message
      createdAt
    }
  }
}
```

```graphql
mutation AddContactMessage($token: String!) {
  addContactMessage(
    token: $token
    message: "Voici une précision côté client."
    authorName: "ACME"
  ) {
    contact {
      ticketId
      status
      messages {
        message
      }
    }
  }
}
```

### Diagnostic

Le diagnostic public est persistant côté Django, rattaché à un `ClientDossier` en phase `Diagnostic`, et n'utilise plus de stockage Nitro.

```graphql
mutation CreateDiagnosticTicket($answers: JSONString!) {
  createDiagnosticTicket(
    organization: "ACME"
    email: "contact@example.com"
    phone: "0612345678"
    message: "Nous voulons comprendre les priorités."
    answers: $answers
  ) {
    redirectTo
    ticket {
      id
      ticketId
      organization
      diagnosticResult
      emailConfirmation
      clientDossier {
        dossierId
        phase
      }
    }
  }
}
```

```json
{
  "answers": "{\"stress\":\"site-slow\",\"siteState\":\"fragile\",\"dependency\":\"one\"}"
}
```

```graphql
query DiagnosticTicket($ticketId: String!) {
  diagnosticTicket(ticketId: $ticketId) {
    id
    organization
    answers
    diagnosticResult
  }
}
```

### Leads

```graphql
query {
  leads(leadType: "developpement", status: "new") {
    id
    name
    email
    leadType
    status
    clientDossier {
      dossierId
    }
  }
}
```

```graphql
mutation {
  createLead(
    name: "Alice Martin"
    email: "alice@example.com"
    budget: "1500"
    projectDescription: "Créer une application métier maintenable."
    timeline: "Q3"
    leadType: "developpement"
  ) {
    lead {
      id
      status
      clientDossier {
        dossierId
      }
    }
  }
}
```

```graphql
mutation {
  updateLeadStatus(id: 1, status: "qualified") {
    lead {
      id
      status
    }
  }
}
```

### Formations

```graphql
query {
  formations(formatType: "presentiel", active: true) {
    id
    title
    formatType
    price
  }
}
```

```graphql
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
    formation {
      id
      title
    }
  }
}
```

### Inscriptions formation

```graphql
query {
  formationRegistrations(formationId: 1, status: "pending") {
    id
    name
    email
    status
    formation {
      title
    }
    clientDossier {
      dossierId
    }
  }
}
```

```graphql
mutation {
  createFormationRegistration(
    formationId: 1
    name: "Alice Martin"
    email: "alice@example.com"
    phone: "0612345678"
    numberOfParticipants: 2
  ) {
    registration {
      id
      status
      clientDossier {
        dossierId
      }
    }
  }
}
```

```graphql
mutation {
  updateFormationRegistrationStatus(id: 1, status: "confirmed") {
    registration {
      id
      status
    }
  }
}
```

### Services

```graphql
query {
  services(serviceCategory: "developpement") {
    id
    name
    slug
    serviceCategory
    order
  }
}
```

```graphql
mutation {
  upsertService(
    slug: "audit-site"
    name: "Audit site"
    description: "Audit de présence web"
    serviceCategory: "developpement"
    order: 1
  ) {
    service {
      id
      slug
    }
  }
}
```

### Suppression admin

```graphql
mutation {
  deleteCrmObject(model: "lead", id: 1) {
    ok
  }
}
```

`model` accepte `contact`, `lead`, `formation`, `registration` ou `service`.
