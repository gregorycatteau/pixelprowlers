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
