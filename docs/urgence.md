# Tunnel urgence PixelProwlers

## Route frontend

- Page : `/urgence`
- Domaine de référence : `https://pixelprowlers.io/urgence`
- Objectif : permettre à un visiteur de déclarer une urgence web en moins de 90 secondes.
- Aucun upload de fichier dans cette première version.
- Le formulaire rappelle explicitement de ne transmettre aucun mot de passe, token, clé privée, accès administrateur ou information sensible.

## Endpoint

- API GraphQL : mutation `createUrgencyRequest`
- Stockage actuel : table Django `urgencies_urgencyrequest` via PostgreSQL.
- Référence générée : `PXP-URG-YYYYMMDD-XXXX`.
- Champ de qualification humaine : `expected_next_step`.
- Le backend valide les champs, l URL, l email, le téléphone, les consentements, le honeypot, les longueurs et les caractères CRLF dans les champs monolignes.
- Les secrets évidents sont refusés par heuristique simple.

## Variables d environnement

- `SMTP_HOST` : serveur SMTP.
- `SMTP_PORT` : port SMTP, `587` par défaut.
- `SMTP_USER` : utilisateur SMTP.
- `SMTP_PASS` : mot de passe SMTP.
- `SMTP_SECURE` : `true` pour TLS direct.
- `CONTACT_FROM` : adresse expéditeur.
- `URGENCY_INTERNAL_EMAIL` : destinataire interne prioritaire. Repli sur `CONTACT_TO` si absent.
- `URGENCY_RATE_LIMIT_MAX` : nombre de demandes autorisées par IP sur 15 minutes, `5` par défaut.

- `SMS_DRY_RUN` : `true` par défaut, journalise le SMS au lieu d'appeler Twilio.
- `INTERNAL_SMS_TO` : destinataire SMS interne optionnel.
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER` : configuration Twilio pour l'envoi réel.
- `WEBHOOK_URL` ou `URGENCY_WEBHOOK_URL` : webhook optionnel.
- `WEBHOOK_TOKEN` ou `URGENCY_WEBHOOK_TOKEN` : token bearer optionnel pour le webhook.

Aucun secret ne doit être codé en dur dans le dépôt.

## Flux de notification

1. Le visiteur soumet `/urgence`.
2. La mutation `createUrgencyRequest` valide et refuse les contenus à risque.
3. Une référence `PXP-URG-YYYYMMDD-XXXX` est générée.
4. La prochaine étape souhaitée est transmise dans le ticket interne.
5. Un email interne prioritaire est envoyé si la configuration SMTP et le destinataire interne sont présents.
6. Un email automatique de confirmation est envoyé au client si SMTP est configuré.
7. Un SMS interne est déclenché pour `activité bloquée` ou `risque sécurité/données`. Par défaut il reste en dry-run.
8. Un webhook optionnel reçoit un payload sans description libre ni coordonnées client.

## Limites anti-abus

- Rate limiting par IP : fenêtre de 15 minutes.
- Honeypot `website` côté frontend et backend.
- Refus des CRLF dans les champs monolignes pour limiter l injection header/email.
- Longueurs maximales strictes.
- URL limitée à `http` et `https`.
- Pas d upload de fichier.
- Les logs ne contiennent pas la description client ni les coordonnées complètes.

## Tests manuels

- Ouvrir `https://pixelprowlers.io/urgence` ou `http://localhost:3000/urgence`.
- Soumettre une demande valide et vérifier l affichage de la référence.
- Vérifier la persistance du ticket côté storage.
- Vérifier l email interne et l email client avec une configuration SMTP de test.
- Vérifier `notification_status.internal_sms` : `dry_run` en local, `sent` si Twilio réel est configuré.
- Vérifier `notification_status.webhook` : `not_configured` sans URL, `sent` si le webhook répond correctement.
- Soumettre une URL invalide et vérifier le message d erreur propre.
- Soumettre un champ monoligne avec saut de ligne et vérifier le rejet.
- Soumettre une description contenant `password=` ou une clé privée factice et vérifier le rejet.
- Remplir le honeypot `website` via les devtools et vérifier le rejet.
- Dépasser `URGENCY_RATE_LIMIT_MAX` demandes en 15 minutes et vérifier le HTTP 429.
