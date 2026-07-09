# Dossiers client

## Identifiant

Chaque interaction client peut être rattachée à un `ClientDossier`.

Format public :

```text
YYMMNNN-P
```

Exemple :

```text
2607001-0
```

- `YY` : année sur deux chiffres.
- `MM` : mois.
- `NNN` : séquence mensuelle, réinitialisée chaque mois.
- `P` : phase courante.

La contrainte `(sequence_month, sequence_number)` garantit l'unicité de la séquence mensuelle. `dossier_id` est aussi unique.

## Phases

| Phase | Nom |
|-------|-----|
| 0 | Contact |
| 1 | Diagnostic |
| 2 | Proposition |
| 3 | Contrat |
| 4 | En cours |
| 5 | Tests / recette |
| 6 | Livraison |
| 7 | Suivi |
| 8 | Archivé |

`ClientDossier.increment_phase()` met à jour `dossier_id` et crée un `DossierLog` avec `old_phase`, `new_phase`, `timestamp`, `changed_by` nullable et `reason`.

## Rattachements actuels

- `createAuditDossier` crée ou rattache un dossier client en phase `0`.
- `submitAuditReponses` passe le dossier en phase `1`.
- `createRefonteAudit` crée ou rattache un dossier client en phase `1`.
- `createRdvReservation` crée ou rattache un dossier client en phase `2`.
- `createUrgencyRequest` crée ou rattache un dossier client en phase `0`.
- `sessionInit` crée un dossier client anonyme en phase `0`.

Le rattachement par email réutilise le dernier dossier non archivé. Sans email, un nouveau dossier est créé.

## Notifications

Les emails ne bloquent pas les mutations : une erreur SMTP est loguée et stockée dans `notification_status`.

Les SMS sont prêts pour Twilio mais restent en dry-run par défaut avec `SMS_DRY_RUN=true`. Les webhooks sont non bloquants et retournent `not_configured` si aucune URL n'est définie.
