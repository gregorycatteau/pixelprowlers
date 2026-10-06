# Correctif de confinement du backend historique — 6 octobre 2026

## Statut et périmètre

**Préparé et qualifié localement ; non déployé.** Aucun push, workflow, réglage ou volume de production modifié. Aucun dossier client de production consulté. Les tests utilisent exclusivement des fixtures synthétiques et des adresses `example.invalid`, sans email réel.

Branche : `fix/backend-historique-securite-runtime-20261006`, dans le worktree distinct `pixelprowlers-backend-securite-20261006`. Base : `09b2cde900083bf7f0160292fbccc5225118d0ae`. Le commit final et l'image exacte sont identifiés par le manifeste local produit après commit, et par le label `org.opencontainers.image.revision` de l'image.

L'arbre original `feat/pixelprowlers-repositionnement-sasu` au commit `c0d9c13beac1429b4a5353176f89b28eacdf9012`, ses modifications et ses fichiers non suivis sont conservés. La branche initialement créée depuis `c79299c7` reste intacte : elle n'a pas été déplacée. Le choix de `09b2cde` exclut dix fichiers ajoutés ensuite, dont l'application boutique inactive. Aucun code frontend, modèle, migration, requirements ou lockfile n'est modifié.

## Identification de production — observations renouvelées

Les 79 fichiers Python chargés, `requirements.txt` et le Dockerfile correspondent, par SHA-256, à cette base historique. Les empreintes et versions des dépendances sont dans [runtime-fingerprint.json](evidence/runtime-fingerprint.json).

| Élément | Observation actuelle |
|---|---|
| Django | image `sha256:1fd7de0d2b3028177417e877683cced740ac40955ec1ce25aba93027e671d139` ; conteneur `c10e4b6fbd1a307fa12b2c3a318a68da9fff6e62444d9704ba2a10e7e765300a`, sain |
| PostgreSQL | 15.10 ; image `sha256:933581caa3e7f545e12ab058d0063011a517d403a3cb93059ac8d8dde064313e` ; 43 tables, 36 migrations enregistrées |
| Historique SQL | 34 migrations des applications actives et deux migrations de l'ancienne application `api`, désormais non chargée ; ses tables sont conservées |
| Rôle courant | `SUPERUSER`, `CREATEDB`, `CREATEROLE` encore présents ; aucune réduction effectuée en production |
| Notifications | backend console ; destinataires contacts/audits/urgences et clé `AUDIT_SIGNATURE_KEY` absents ; TLS SMTP désactivé ; SMS en dry-run et webhook absent |
| Frontend | métadonnées `1205eeb78e4985930f0a326dcb403052be222482`, livraison frontend seule ; image `sha256:aa65083b2205af7891d57cd4b568c245dd3609e1f4f25d52fdb5fe9525acf709` |

Le nombre de clients et l'existence actuelle d'administrateurs n'ont **pas** été relus. Le constat antérieur d'une base vide ne permet aucune conclusion actuelle. Les données SQL lues dans cette tâche sont uniquement des métadonnées de schéma, le registre des migrations et les attributs du rôle.

Qualification : Python **3.13.13**, contre **3.13.14** en production. Les versions des dépendances applicatives installées sont identiques ; seul `pip` diffère (26.0.1 / 26.1.2). Base de construction locale figée : `sha256:efd98e84bc445b342a64b05cb63e40cae0fa62f7e920676261db4f4c1520fd23`. Aucun téléchargement ou installation de dépendances. Le venv Python 3.14 n'est pas utilisé.

## Vulnérabilités reproduites sur fixtures

Avec le code historique non corrigé, dans le réseau Docker interne de qualification :

- `contacts` permet une lecture anonyme du nom, de l'email et du jeton secret d'un contact synthétique.
- `deleteCrmObject` supprime anonymement ce contact synthétique.
- `_request` tente un appel vers une URL loopback ; l'appel est intercepté par mock **avant tout accès réseau**.

Ces reproductions ne comportent aucune requête privée vers la production ni vers une métadonnée cloud réelle.

## Matrice complète des opérations historiques

Dans la colonne contrôle, « aucun » signifie qu'aucun contrôle d'autorisation objet n'existait dans le resolver historique. Le schéma corrigé est une liste positive ; les projections n'exposent plus les relations de dossier, les logs internes ou les parents de messages.

| Opération(s) | Fonction / données | Public autorisé et authentification | Contrôle historique | Correctif / vérification |
|---|---|---|---|---|
| `citationAleatoire` | Citation publique ; compteur d'affichages | Public | Filtre actif | Conservé, projection limitée ; contrat frontend |
| `motifs`, `raisonsAppel` | Référentiels de réservation | Public | Filtre actif | Conservés ; test historique réservation |
| `creneauxDisponibles`, `calendrierMois` | Disponibilités sans identité | Public | Validation dates / motif | Conservés ; contrat et test réservation |
| `createContact` | Dépôt et premier message | Public, consentement / anti-abus historiques | Validation, délai, honeypot, quota ; pas d'identité requise | Validation complète avant écriture ; groupe contact/message/dossier atomique ; notifications après ; tests et navigateur trois largeurs |
| `contactByToken` | Un contact et ses messages | Possession du jeton secret aléatoire de 256 bits | Recherche par jeton ; projection trop large | Jeton de format attendu, refus générique, projection sans relations internes ; tests mauvais jeton, identifiant, imbrication et séparation A/B |
| `addContactMessage` | Réponse du demandeur | Même jeton secret ; aucun rôle navigateur | Jeton mais nom d'auteur libre | Auteur CUSTOMER et nom issus du contact côté serveur ; quota, écriture atomique ; tests refus sans jeton et navigateur |
| `createDiagnosticTicket` | Diagnostic historique | Public, données validées | Création ouverte légitime | Conservé ; `redirectTo` et lien email signés Django, identifiant court d'affichage conservé ; test historique et écran navigateur |
| `diagnosticTicket` | Résultat et coordonnées d'un diagnostic | Lien signé avec `SECRET_KEY` Django, salt dédié, validité maximale 30 jours | Identifiant court seul | Refus des anciens IDs bruts, altérations, expiration, mauvais salt ; aucune recherche avant preuve valide |
| `createAuditDossier` | Initialisation d'un audit | Public, origine autorisée et session Django | Création ouverte | Accorde une autorisation serveur dans la session existante ; numéro d'affichage inchangé ; tests historiques |
| `submitAuditReponses` | Réponses, scores et signature | Session créatrice, objet et utilisateur éventuel liés côté serveur | Numéro séquentiel seul | Resolver exige l'autorisation objet ; serializer exige le dossier autorisé transmis par serveur ; tests autre navigateur/utilisateur/origine, expiration et appel direct du service |
| `createRefonteAudit` | URL et questionnaire fournis | Public, origine autorisée et session Django | Déclenchement réseau automatique | Dépôt conservé, analyse arrêtée, autorisation de suivi accordée ; test aucun réseau / thread / navigateur |
| `refonteAudit` | Rapports d'un seul dossier | Session créatrice et autorisation objet | Référence seule | Refus autre session ; API et cookie vérifiés au navigateur ; écran résultat frontend non qualifié, voir limites |
| `auditDossier`, `clientDossier` | Identité, réponses et dossiers consolidés | Privé ; aucun accès public maintenu | Numéro ou référence seul | Retirés du schéma public, y compris pour staff ; administration Django existante uniquement |
| `contacts`, `contact`, `unreadContacts` | Lectures CRM / coordonnées / jetons | Privé | Aucun | Retirés ; refus anonyme, utilisateur, staff et superutilisateur ; aucune imbrication alternative |
| `leads`, `lead` | Prospects CRM | Privé | Aucun | Retirés ; administration Django avec permissions de modèle |
| `formations`, `formation` | Administration formation | Privé ; aucune opération consommée par le frontend livré | Aucun | Retirées ; tests de fermeture |
| `formationRegistrations`, `formationRegistration` | Inscrits et coordonnées | Privé | Aucun | Retirées ; tests de fermeture |
| `services`, `service` | Administration du référentiel | Privé ; non consommé par les 16 contrats publiés | Aucun | Retirés ; contenu de vitrine existant conservé |
| `createLead`, `updateLeadStatus` | Création / traitement CRM | Privé | Aucun | Classes de mutation publique supprimées ; modèle et admin conservés |
| `createFormation`, `createFormationRegistration`, `updateFormationRegistrationStatus` | Administration formation | Privé | Aucun | Retirées ; aucun accès d'inscription non autorisé maintenu |
| `upsertService`, `deleteCrmObject` | Modification / suppression | Privé | Aucun | Retirées ; tests sans effet de bord, validation avant exécution |
| `sessionInit`, `recordPageView`, `recordQuestionInteraction`, `recordTrackingEvent` | Tracking et liens vers dossiers | Aucun usage par le frontend publié qualifié | UUID navigateur et relations trop larges | Mixins retirés du schéma public ; stockage interne conservé ; tests des quatre noms réels |
| `createRdvReservation` | Réservation publique | Public | Validations / disponibilités | Conservée ; réponse limitée au RDV/créneaux/motif, sans identité imbriquée ; test historique |
| `createUrgencyRequest` | Dépôt d'urgence | Public, consentements et validation | Validation / quota | Conservée ; projection ticket référence/statut seule ; test réel de création GraphQL |

Les comptes clients authentifiés récents ne sont pas introduits. Les modèles historiques n'ont pas de propriétaire utilisateur pour une séparation par compte client : on ne prétend donc pas déduire une propriété à partir d'un email ou d'un ID. L'API CRM est fermée entièrement. Les opérateurs Django staff n'accèdent au CRM qu'après attribution explicite des permissions de modèle ; ces permissions leur donnent une portée métier sur le modèle, **pas** une segmentation par intervenant. Un utilisateur non-staff n'est pas un opérateur CRM.

Pour les audits/refontes, les autorisations serveur sont limitées à 20 objets, datées et liées à l'utilisateur Django éventuel. La référence seule ne suffit pas. Le navigateur publié envoie déjà `credentials: same-origin`. Un changement de navigateur, la perte du cookie ou le passage à un autre compte ferme le suivi. Les anciens liens non autorisés restent fermés ; une récupération exige un opérateur et une vérification réelle du demandeur, à définir au lot d'exploitation.

La validation GraphQL complète est rétablie en production, en plus de l'interdiction d'introspection. Alias, fragments et tableaux HTTP ne contournent pas la fermeture ; une sélection invalide empêche aussi l'exécution de la mutation publique présente dans la même opération. Les réponses API portent `Cache-Control: no-store` et `Referrer-Policy: no-referrer`.

## SSRF : arrêt complet

`refonte_analysis.py` ne contient plus de client HTTP, DNS, Playwright, parser de sous-ressources ou thread. Les entrées initiale et différée écrivent seulement un statut local `non_analysable` avec :

> Analyse automatique désactivée. Votre demande est enregistrée pour une prise en charge manuelle.

Les helpers historiques réseau retournent une indisponibilité ou lèvent `AutomaticAnalysisDisabled`. L'URL fournie est stockée, sans prétendre que sa validation syntaxique la rend sûre à charger. Aucun réglage n'autorise la réactivation de l'ancien moteur. Un futur moteur nécessitera une qualification séparée de la connexion effective, des redirections et de toutes les sous-ressources.

## Vérifications exécutées

| Vérification | Résultat / portée |
|---|---|
| Tests Django sur PostgreSQL 15 dédié, Python 3.13 | **26 tests réussis** ; [sortie conservée](evidence/tests-postgresql.txt) |
| Historique | Import citations, audit/scores/signature/notification échouée, refonte, réservation, contact/suivi/réponse, diagnostic, URLs et CORS conservés/adaptés. Trois tests validant les anciennes opérations publiques dangereuses remplacés par les tests de fermeture ; contrôle du dossier lié maintenu côté ORM lorsque nécessaire |
| Sécurité ciblée | Refus privés pour quatre profils ; objet A/B ; mauvaise preuve/expiration/scope ; erreurs sans email du dossier ; service sans autorisation refusé ; admin sans permission refusé puis permissions view/change vérifiées |
| Notifications | Demande et premier message conservés malgré erreur ; console/dummy/file/locmem jamais présentés comme SMTP ; SMTP simulé `count=1` = acceptation du relais uniquement, `count=0` = échec ; aucun email réel |
| SSRF | Création et entrées indirectes avec sockets, DNS, thread et processus interdits ; URLs IPv4, IPv6, adresse de métadonnée et redirection simulées sans requête |
| Contrats frontend | **16/16** sélections compilent sur le schéma corrigé ; fixtures depuis le frontend `1205eeb` |
| Navigateur publié, backend isolé | Estimation → contact → ticket → réponse, clavier Enter, **390 / 768 / 1440 px**, deux messages visibles, sans erreur JS ni débordement du ticket. [390](evidence/contact-ticket-reply-390.png), [768](evidence/contact-ticket-reply-768.png), [1440](evidence/contact-ticket-reply-1440.png) |
| Diagnostic | Nouveau lien signé chargé dans la page publiée ; ID court affiché, [capture](evidence/signed-diagnostic-390.png) |
| Refonte | API manuelle et isolation des cookies vérifiées depuis le navigateur ; affichage du résultat non qualifié, voir ci-dessous |
| Migrations | `makemigrations --check --dry-run` : **No changes detected** ; aucun modèle/migration modifié ; aucune migration prévue en livraison |
| Droits SQL réduits | Contact/suivi/réponse/traitement et audit/session/signature réussis ; CREATE DATABASE, CREATE ROLE, ALTER TABLE, DROP TABLE et CREATE TABLE refusés ; attributs superuser/createdb/createrole faux |
| Scripts | Syntaxe Bash vérifiée ; sauvegarde et restauration réellement exécutées sur fixtures |

Le registre de qualification contient les **34 migrations actives et 38 tables** ; la production contient aussi cinq tables héritées de `api` et ses deux anciennes migrations. Elles ne sont ni recréées ni supprimées par ce lot. La sauvegarde complète prévue les inclut.

## Sauvegarde et restauration effectivement qualifiées

`backup.sh` réalise un `pg_dump -Fc --no-owner --no-acl`, export MVCC cohérent, avec identité explicite du conteneur et de la base, répertoire 700 et fichiers 600. Il vérifie la taille, la lisibilité du catalogue et SHA-256. Il ne copie ni fichier d'environnement ni secret d'exploitation.

Dump synthétique conservé hors Git : `/tmp/pixelprowlers-backend-fix-20261006/backup/20261006T121835Z-backend-security/database.dump`. Une autre instance PostgreSQL 15 dédiée, initialement sans tables, a été restaurée avec `--single-transaction --exit-on-error`, sans `--clean`.

Contrôles réellement effectués : égalité des colonnes et du registre des migrations ; égalité exacte des lignes synthétiques d'origine contact/messages/audit/réponse ; chargement du ticket restauré ; nouveau contact/réponse et nouvelle soumission d'audit après restauration, sous le rôle applicatif réduit. Le dump et les données de qualification ne sont pas une sauvegarde de production ; **aucune restauration de production n'a été testée**.

Rétention proposée : conserver toute sauvegarde préalable à une livraison jusqu'à son acceptation, puis 7 quotidiennes / 4 hebdomadaires / 6 mensuelles ; copie chiffrée hors serveur et contrôle périodique de restauration. Aucun nettoyage automatique installé. La politique de suppression doit être revue avant activation.

Django actuellement sans montage média, applications historiques sans catalogue de photos à livrer : aucun volume média touché. Réinspecter les montages avant livraison ; tout média devenu pertinent nécessite un export séparé protégé, coordonné avec l'export DB. Conserver également les images applicatives, l'identité du volume PostgreSQL, les fichiers Caddy/Compose et les références de secrets dans le coffre existant, sans les intégrer à Git.

Secrets/configurations indispensables à une restauration : identifiants PostgreSQL, `DJANGO_SECRET_KEY` stable (sessions et liens signés), éventuelle `AUDIT_SIGNATURE_KEY` stable pour les signatures, SMTP et ses destinataires validés, paramètres domaine/TLS/proxy/CORS, accès SSH/coffre. Aucun secret à valeur de secours publique n'est créé pour l'exploitation. Les valeurs de qualification sont explicitement synthétiques et ne doivent jamais être utilisées en production.

## Réduction des privilèges : préparée, non appliquée

`runtime-role.sql` prépare `pixelprowlers_app` initialement NOLOGIN, sans SUPERUSER/CREATEDB/CREATEROLE/REPLICATION/BYPASSRLS. Il autorise DML sur les seules tables des applications historiques actives, sessions/auth/admin, lecture du registre et des content types, usage des séquences associées. Les anciennes tables `api_*` sont exclues. Pas de CREATE sur le schéma, transfert de propriétaire ou attribution globale aux tables futures.

La maintenance/migration reste distincte, avec le propriétaire des objets existants : compte réservé à la maintenance, jamais utilisé par Gunicorn. Une éventuelle réduction de ce compte et les transferts de propriétaire seront un lot séparé. Les nouvelles tables futures nécessitent une revue explicite des GRANT ; aucun déploiement ne doit lancer implicitement `migrate`.

Avant activation réelle : examiner les grants PUBLIC existants et les droits effectifs ; provisionner un mot de passe unique depuis le coffre ; contrôler une copie de restauration ; modifier seulement l'environnement Django après approbation, sans changer POSTGRES_USER du service PostgreSQL ni réinitialiser son volume.

Retour arrière des droits : rétablir la référence d'identifiants applicatifs précédente, recréer uniquement Django, vérifier les opérations ; laisser le rôle réduit en place et retirer son LOGIN ensuite si nécessaire. Aucun DROP ROLE / DROP OWNED / changement de propriétaire ni restauration de base active. Cette séparation a été testée sur instances dédiées.

## Lot SMTP et administration suivant

| Sujet | Paramètres / travaux nécessaires | Qualification requise |
|---|---|---|
| Administration | Compte nominatif existant Django, `is_staff`, groupe de permissions minimales ; mot de passe unique, procédure de récupération, accès admin protégé ; aucun compte client parallèle | Connexion personnelle, view/change explicitement accordés, refus sans permission et pour non-staff ; contrôle de session et traçabilité d'une réponse |
| SMTP | `EMAIL_BACKEND` SMTP, `SMTP_HOST/PORT/USER/PASS`, `SMTP_USE_TLS`, expéditeur vérifié ; ajouter timeout explicite et SSL seulement si le fournisseur l'exige | Boîte contrôlée, TLS et authentification, erreurs/timeout, acceptation SMTP puis réception réellement observée ; console ne suffit jamais |
| Destinataires | `CONTACT_TO`, `AUDIT_INTERNAL_EMAIL`, `URGENCY_INTERNAL_EMAIL` validés par l'exploitant ; le Compose actuel ne transmet pas nécessairement ces variables, adapter explicitement après revue | Nouvelle demande à chaque canal dans une boîte contrôlée, absence d'adresse devinée ou de fallback silencieux |
| Audits | Clé `AUDIT_SIGNATURE_KEY` générée dans le coffre, injectée sans valeur publique ; conserver les clés de signature précédentes si une rotation est décidée | Soumission, stabilité/vérification des signatures après restauration ; refus sans clé avant émission de notification |
| Réponse aux tickets | Action opérateur Django autorisée, auteur professionnel imposé côté serveur ; notification du client avec lien secret existant | Réponse enregistrée, autre dossier inaccessible, réception dans boîte contrôlée ; l'interface actuelle n'envoie pas de notification de réponse automatiquement |
| Reprise d'envoi | Ajouter une outbox persistante et identifiant unique `(dossier, événement, destinataire)` ; états pending / relay_accepted / failed ; verrouillage, backoff, journal sans corps/jetons et outil de reprise | Échec, reprise ciblée, répétition sans double émission applicative ; un crash après acceptation SMTP peut être ambigu, ne pas promettre un exactly-once sans mécanisme du fournisseur |
| Sauvegardes | Planifier le script avec paramètres validés, alerte d'échec, copie chiffrée externe, rétention et exercice de restauration | Export complet, contrôle SHA, restauration dédiée, redémarrage applicatif et cohérence des dossiers/media |
| Fallback `.fr` | `app/pages/rendez-vous.vue:287` du frontend livré utilise `mailto:contact@pixelprowlers.fr` ; ne pas remplacer par une adresse `.io` supposée | Confirmer une boîte réellement reçue et modifier frontend dans un lot explicite ; un mailto ne crée pas de demande en DB |

Les statuts restent compatibles avec le frontend : `sent` signifie uniquement **accepté par le relais SMTP** ; `not_configured` couvre console/simulation ; `failed` signifie échec de tentative. La demande enregistrée est une réalité distincte. L'attente persistante, les reprises et la réception constatée ne sont pas implémentées dans ce correctif ; elles ne peuvent pas être déduites d'un HTTP 200 ou d'un état `sent`.

SMS et rappels automatiques restent désactivés/non qualifiés. Aucun destinataire réel n'a été utilisé. L'anti-abus historique reste un quota LocMem par processus et l'attribution IP repose sur X-Forwarded-For : avant activation SMTP, qualifier les proxies de confiance et un compteur partagé/atomique. Ce lot ne prétend pas fermer cette limite d'exploitation.

## Limites et décisions avant livraison

- Réception et traitement **non qualifiés de bout en bout** : administration réelle, SMTP, réception et réponse client restent à mettre en place.
- La signature des audits n'est pas configurée en production : la soumission n'y est pas qualifiée malgré le test local avec clé synthétique. La livraison urgente protège le formulaire de contact actuellement utilisé ; elle n'active pas les anciens questionnaires.
- La route publiée `/audit-refonte/resultat` affiche la page d'introduction du parent `audit-refonte.vue`, plutôt que le composant résultat. L'API protégée fonctionne, mais cet écran et les métriques factices affichables par le vieux template ne sont pas qualifiés. Aucun code frontend n'est modifié par ce lot ; ne pas promouvoir ce parcours comme analyse automatique.
- Les anciens liens diagnostic basés sur un identifiant et les audits/refontes sans autorisation de session sont volontairement fermés. Préparer une reprise manuelle avec opérateur et vérification du demandeur, jamais une réouverture par ID.
- Les jetons de contact restent des liens secrets partageables, sans expiration ni rotation existantes ; protéger les journaux HTTP et les captures. Les headers API ne remplacent pas une politique de logs/referrer de la page frontend.
- PostgreSQL en production reste surprivilégié. La réduction est un changement de configuration distinct, à approuver après restauration sur copie dédiée.
- Python 3.13.13 qualifié et production 3.13.14 diffèrent : les deux empreintes sont déclarées, aucune égalité de runtime complète n'est revendiquée.
- Le retour à l'ancienne image **réintroduit les vulnérabilités** : préférer un confinement temporaire et un correctif complémentaire ; si rollback nécessaire, bloquer `/graphql/` pendant sa durée après approbation.

La procédure concrète de construction, export, sauvegarde, livraison limitée et rollback se trouve dans [le runbook](../../ops/backend-security/README.md). La production demeure inchangée à l'issue de cette préparation.
