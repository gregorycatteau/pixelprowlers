# Service de contact PixelProwlers

## Autorité métier

Le formulaire Nuxt appelle la mutation GraphQL `createContact` du backend
Django. Django est l'unique autorité pour la validation, la normalisation, le
numéro de dossier, le HMAC, PostgreSQL et les notifications. Le frontend ne
génère aucune donnée de sécurité.

Le service Go `pixelprowlers-contact`, situé dans le dépôt séparé
`mnemoshade`, est un prototype technique à archiver. Il a servi à valider le
verrouillage concurrent, la séquence commit puis SMTP et les délais SMTP. Il
ne doit recevoir aucune route Caddy, aucun trafic de production et aucune
configuration métier PixelProwlers. Sa suppression éventuelle fera l'objet
d'une opération séparée.

## Numéro et intégrité

`crm.ContactDailyCounter` possède une ligne unique par date métier. La création
insère la ligne de manière idempotente puis la verrouille avec
`select_for_update()` dans la même transaction que le dossier. Le format est
`DDMMYYYYNNN` en `Europe/Paris`; `NNN` va de `001` à `999`. La limite produit
une erreur explicite et la contrainte unique PostgreSQL reste la dernière
défense.

Le HMAC-SHA-256 couvre une sérialisation JSON UTF-8 canonique de :

- `numero_dossier`;
- `date_creation`, convertie en UTC au format ISO 8601 avec microsecondes et
  suffixe `Z`;
- `nom`, `prenom`, `email`, `telephone`, `objet`, `methode_contact`, `message`.

Les chaînes sont normalisées en Unicode NFC, les clés JSON sont triées et les
séparateurs JSON sont fixes. La clé vient uniquement de
`CONTACT_HMAC_SECRET`. Le HMAC garantit l'intégrité, pas la confidentialité des
données personnelles.

## Transaction et email

L'ordre est : validation, transaction, compteur verrouillé, numéro, HMAC,
insertion du contact et du premier message, rattachement CRM, commit, callback
`transaction.on_commit()`, email Django, mise à jour séparée du statut de
notification.

Une erreur email conserve le dossier et son numéro, place
`statut_notification` à `echec`, et renvoie un message public qui ne prétend
pas qu'un email a été envoyé. Les logs contiennent le numéro de dossier et le
type technique de l'erreur, jamais le formulaire, le destinataire ou un
secret.

Il n'existe aucun retry automatique. Un appel répété sur un dossier déjà
marqué `envoyee` est ignoré et journalisé sans donnée personnelle. La courte
fenêtre entre l'acceptation SMTP et l'enregistrement du statut ne peut pas être
rendue atomique avec SMTP : un renvoi manuel d'un dossier `en_attente` ou
`echec` doit donc rester une opération explicitement autorisée et contrôlée.

## Relais transactionnel Brevo

Brevo est l'unique fournisseur transactionnel autorisé. Django utilise son
backend SMTP natif; aucune API Brevo, SDK fournisseur ou seconde pile SMTP
n'est ajoutée. En production, les settings refusent :

- un backend autre que le backend SMTP Django ;
- un relais différent du relais SMTP Brevo approuvé ;
- des identifiants SMTP absents ;
- TLS et SSL simultanément activés ou simultanément désactivés ;
- un expéditeur `DEFAULT_FROM_EMAIL` ou `SERVER_EMAIL` hors du domaine
  authentifié `pixelprowlers.io` ;
- une adresse d'expédition vide, invalide ou contenant CR/LF.

L'adresse exacte d'expédition n'est pas fixée dans le dépôt : elle doit être
une identité déjà autorisée dans le compte Brevo et être injectée par
l'environnement. L'adresse utilisateur n'est jamais utilisée comme `From` ou
comme en-tête contrôlant le sujet.

Les variables canoniques sont `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`,
`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `EMAIL_USE_SSL`,
`EMAIL_TIMEOUT`, `DEFAULT_FROM_EMAIL` et `SERVER_EMAIL`. Les anciens alias
`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_USE_TLS` et
`SMTP_SECURE` restent lus uniquement pour compatibilité. Une variable
canonique non vide gagne toujours; une contradiction est journalisée par les
noms de variables seulement, sans aucune valeur.

Le login SMTP Brevo n'est pas nécessairement l'adresse visible d'expédition.
`EMAIL_HOST_PASSWORD` doit contenir une clé SMTP dédiée à Django, et non une
clé API ni le mot de passe du compte Brevo. Les secrets viennent uniquement
de l'environnement. Authelia et Django n'ont pas à partager la même clé SMTP.

`CONTACT_NOTIFICATION_RECIPIENT` est uniquement le destinataire facultatif de
la notification interne PixelProwlers. Il ne remplace jamais l'adresse
utilisateur comme destinataire de l'accusé de réception.

## Contrat public et confirmation

La mutation de création expose uniquement `success`, `numeroDossier` et
`message`. Elle ne retourne ni HMAC, ni statut SMTP, ni token de suivi, ni
identifiant interne. Le frontend conserve temporairement ces trois données de
confirmation dans `sessionStorage` et navigue vers `/contact/confirmation`
sans placer de donnée de dossier dans l'URL. Le rendu Vue utilise
l'interpolation de texte et aucun `v-html`.

### Procédure de test manuel contrôlé

Cette procédure ne doit être lancée qu'avec une autorisation explicite :

1. injecter les variables Brevo depuis le gestionnaire de secrets, sans les
   afficher dans le terminal ou les logs ;
2. choisir une unique adresse de test autorisée et tracer l'heure du test ;
3. soumettre une demande identifiable via le formulaire normal afin de créer
   exactement un dossier ;
4. vérifier dans PostgreSQL le numéro et le passage de `en_attente` à
   `envoyee`, sans afficher le HMAC ou les données inutiles ;
5. confirmer la réception des versions texte et HTML et l'adresse `From` ;
6. inspecter les en-têtes reçus pour SPF, DKIM et DMARC ;
7. retrouver l'envoi dans les journaux transactionnels Brevo ;
8. vérifier que les logs Django ne contiennent ni identifiant Brevo, ni
   destinataire complet, ni contenu de message ;
9. en cas d'échec, confirmer que le dossier reste présent avec le statut
   `echec`.

Aucun envoi Brevo réel n'est effectué par la suite automatisée : elle utilise
le backend mémoire Django et des exceptions simulées.

## Frontière HTTP et anti-abus

Django limite le corps à `DJANGO_MAX_REQUEST_BODY_BYTES` (1 Mio par défaut).
GraphQL rejette les arguments inconnus et la mutation applique les longueurs,
choix, emails, champs obligatoires, espaces et CRLF. Le honeypot et le délai
minimal existants sont conservés.

Caddy doit ajouter une limite de corps au moins aussi stricte et un rate limit
par adresse source avec une rafale courte. Django ne considère
`X-Forwarded-For` que si le pair TCP direct figure dans `TRUSTED_PROXY_IPS`.
Dans une chaîne transmise par ce proxy, l'adresse la plus proche du proxy est
utilisée afin qu'une valeur préfixée par le client ne contourne pas la limite.
Configurer `127.0.0.1` uniquement pour un Caddy local; en réseau Docker,
relever et utiliser l'adresse réelle du proxy au lieu de supposer un
sous-réseau. Ajouter Turnstile uniquement si les limites, le honeypot et le
délai minimal ne suffisent plus.

Le frontend et `/graphql/` doivent de préférence rester sous la même origine
`https://pixelprowlers.io`; aucun CORS générique n'est nécessaire et les
credentials ne doivent pas être combinés avec une origine `*`.

## Champs obligatoires

Ouvrir un ticket exige toujours les neuf champs métier du formulaire : type
de demande, prénom, nom, organisation, adresse email, numéro de téléphone,
méthode de contact préférée, objet et message. La méthode `email`,
`telephone` ou `les_deux` indique seulement le canal préféré; elle ne rend
jamais le téléphone facultatif.

Le frontend applique le même schéma avec Zod et VeeValidate pour guider
l'utilisateur. Son widget conserve une liste fixe de neuf champs, retire une
coche dès qu'une valeur redevient invalide et maintient le bouton désactivé
tant que le formulaire n'est pas modifié et entièrement valide. Django reste
l'autorité : GraphQL exige `company`, `telephone` et `demandType`, puis le
service revalide le téléphone même lorsqu'il est appelé sans passer par la
mutation.

### Téléphone mobile français

Le contact accepte exclusivement les quatre présentations suivantes, pour les
préfixes `06` et `07` : `0612345678`, `06 12 34 56 78`, `+33612345678` et
`+33 6 12 34 56 78`. Les indicatifs étrangers, `0033`, les numéros fixes,
les lettres et toute autre ponctuation sont refusés.

Zod et Django normalisent indépendamment la saisie vers `0[67]XXXXXXXX`. Le
frontend n'envoie que cette forme canonique à GraphQL. Django la recalcule
avant de construire le modèle; PostgreSQL, le CRM et le HMAC utilisent donc
exclusivement les dix chiffres canoniques. Au blur, le champ peut afficher la
forme espacée pour la lecture sans changer cette valeur métier.

Le champ porte le libellé `Organisation ou statut`, l'aide exacte `Indique le
nom de ton organisation ou « Particulier » si tu ne fais pas partie d’une
organisation.` et le placeholder `Nom de l’organisation ou Particulier`.
`Particulier` n'est jamais prérempli. La valeur est saisie volontairement,
normalisée en NFC, trimée et contrôlée comme champ monoligne de 2 à 180
caractères.

La migration `0004` ne remplit pas les champs historiques vides : elle retire
la règle conditionnelle antérieure et conserve les valeurs ainsi que leur
HMAC existant. Le modèle, GraphQL et le service imposent la nouvelle politique
à toute création future, y compris via l'administration Django.
