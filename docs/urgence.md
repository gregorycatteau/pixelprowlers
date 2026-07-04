# Tunnel urgence PixelProwlers

## Route frontend

- Page : `/urgence`
- Domaine de référence : `https://pixelprowlers.io/urgence`
- Objectif : permettre à un visiteur de déclarer une urgence web en moins de 90 secondes.
- Aucun upload de fichier dans cette première version.
- Le formulaire rappelle explicitement de ne transmettre aucun mot de passe, token, clé privée, accès administrateur ou information sensible.

## Endpoint

- API : `POST /api/urgency`
- Stockage actuel : Nitro storage `data`, clé `urgency-tickets:<reference>`.
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
- `URGENCY_WEBHOOK_URL` : webhook optionnel ntfy, Discord, Telegram, Slack ou autre passerelle.
- `URGENCY_WEBHOOK_TOKEN` : token bearer optionnel pour le webhook.
- `URGENCY_SMS_WEBHOOK_URL` : passerelle SMS optionnelle pour impacts critiques.
- `URGENCY_SMS_WEBHOOK_TOKEN` : token bearer optionnel pour la passerelle SMS.

Aucun secret ne doit être codé en dur dans le dépôt.

## Flux de notification

1. Le visiteur soumet `/urgence`.
2. `POST /api/urgency` valide et refuse les contenus à risque.
3. Une référence `PXP-URG-YYYYMMDD-XXXX` est générée.
4. La prochaine étape souhaitée est transmise dans le ticket interne.
5. Un email interne prioritaire est envoyé si la configuration SMTP et le destinataire interne sont présents.
6. Un email automatique de confirmation est envoyé au client si SMTP est configuré.
7. Un SMS interne est déclenché uniquement pour `activité bloquée` ou `risque sécurité/données`, si la passerelle est configurée.
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
- Soumettre une URL invalide et vérifier le message d erreur propre.
- Soumettre un champ monoligne avec saut de ligne et vérifier le rejet.
- Soumettre une description contenant `password=` ou une clé privée factice et vérifier le rejet.
- Remplir le honeypot `website` via les devtools et vérifier le rejet.
- Dépasser `URGENCY_RATE_LIMIT_MAX` demandes en 15 minutes et vérifier le HTTP 429.
