# Réception des demandes : constat et test de bout en bout préparé

## Observation du runtime — 5 octobre 2026

Inspection limitée aux settings effectifs non secrets du conteneur Django, sans lecture des demandes clients ni des logs de production :

| Élément | Observation |
| --- | --- |
| EMAIL_BACKEND | django.core.mail.backends.console.EmailBackend |
| Serveur déclaré | smtp.example.com (valeur d’exemple, non utilisée par ce backend) |
| Port déclaré | 587 |
| TLS / SSL | désactivés |
| Identifiants | présence constatée seulement ; aucune valeur affichée |
| Expéditeur | noreply@pixelprowlers.io |
| Destinataire interne CONTACT_TO | vide |
| Destinataire de l’accusé | contact.email, fourni lors de la soumission |

**Blocage confirmé : aucun transport SMTP n’est exécuté par ce backend console et aucune notification interne n’est configurée.** Le retour sent de safe_send_mail décrit le succès du backend sélectionné, pas une acceptation SMTP ni une livraison dans une boîte. Le backend console peut écrire le contenu de l’accusé et son URL de suivi dans sa sortie ; ne pas provoquer une soumission de production pour tester cette configuration. Aucun log client n’a été consulté.

Cette cause relève d’un lot d’infrastructure/backend distinct. Rien n’est changé dans Django, PostgreSQL, Compose ou les secrets pour cette livraison frontend.

## Chemin réellement exécuté

ContactForm → useContactForm → POST /graphql/ createContact → validations/anti-abus existants → Contact → ContactMessage → attach_client_dossier → _notify_contact et _notify_contact_client → safe_send_mail → backend Django sélectionné. Le suivi existant utilise un jeton secret ; les preuves ne doivent jamais contenir son URL.

Destinataires possibles de createContact : exactement la liste interne [CONTACT_TO] si configurée, puis l’adresse contact.email pour l’accusé. Pas de SMS, webhook ou envoi de réponse de ticket déclenché par cette mutation. Vérifier à nouveau ce graphe et les settings juste avant tout test ; ne pas présumer que la configuration reste celle du relevé.

Les références locales récentes docs/contact-service.md de la branche principale décrivent un autre contrat (success/numeroDossier/message, HMAC, callbacks, Brevo, CONTACT_NOTIFICATION_RECIPIENT, confirmation et sessionStorage). Ces évolutions ne sont pas dans le backend exécuté ni dans la branche de livraison. Ne pas transférer ce contrat ou ces variables à l’aveugle. Dans le runtime inspecté, les settings SMTP lisent SMTP_HOST/PORT/USER/PASS/USE_TLS, pas toutes les variables EMAIL_* du futur contrat. La politique Brevo décrite dans ce document local doit être respectée et rapprochée du runtime dans un lot séparé avant activation.

## Correctif proposé dans un lot séparé

Conserver le contrat legacy tant que le backend n’est pas remplacé et qualifier une modification de configuration dédiée : EMAIL_BACKEND vers le backend SMTP natif Django, SMTP_HOST vers le relais Brevo approuvé, SMTP_PORT et SMTP_USE_TLS cohérents avec ce relais, SMTP_USER/SMTP_PASS injectés par le gestionnaire de secrets, DEFAULT_FROM_EMAIL autorisé sur pixelprowlers.io, CONTACT_TO vers la boîte interne désignée et autorisée. Ne pas copier les secrets ni les valeurs d’exemple. Le TLS doit être effectivement activé et le domaine d’expédition authentifié ; les paramètres définitifs viennent du compte validé du propriétaire.

Le futur contrat de la branche principale demande des validations supplémentaires et un autre destinataire interne nommé CONTACT_NOTIFICATION_RECIPIENT : il nécessite son propre lot backend, ses tests et sa qualification des migrations. Aucun de ces changements ne doit être entraîné par un push master pour livrer ce bloc frontend.

## Préconditions du test réel — actuellement bloquées

1. Le propriétaire désigne une adresse ou un alias de test unique qu’il maîtrise et valide l’accès à sa boîte. Préférer un alias distinct des échanges clients existants.
2. Lister les destinataires internes réellement configurés et les éventuelles redirections/alias de toutes les boîtes concernées. Obtenir l’autorisation pour chacun avant toute soumission. L’expéditeur n’est pas un destinataire supplémentaire.
3. Faire qualifier dans le lot séparé le transport SMTP approuvé, l’expéditeur autorisé, TLS, le destinataire interne et l’absence d’impression des messages/jetons dans les logs. Ne pas tester avec console, un hôte d’exemple ou un transport non chiffré.
4. Vérifier par une simple existence, sans lire de dossier client, qu’aucun dossier non archivé ne porte l’adresse de test. Le rattachement par email peut réutiliser un dossier existant : si collision, demander un autre alias.
5. Fixer la fenêtre, une seule soumission et une seule vérification de réception ; aucun retry automatique, test de charge ou campagne d’abus.

## Demande synthétique préparée

Le jour du test, générer localement un marqueur unique `PP-E2E-CONTACT-<horodatage UTC>-<UUID>` ; conserver ce marqueur et l’heure dans une preuve privée. Il n’ouvre pas un ticket. Nom : Test synthétique Pixelprowlers. Besoin : reparation, donc serviceType materiel / demandType diagnostic. Téléphone, modèle et société réels : absents ; aucune pièce jointe, aucun secret.

Message de moins de 500 caractères : « TEST SYNTHÉTIQUE — <marqueur>. Validation autorisée de l’enregistrement et des notifications. Aucun appareil réel, aucune donnée client, aucune demande d’intervention. » L’adresse email est exclusivement celle désignée par le propriétaire. Utiliser le formulaire public normal pour exercer ses validations et protections ; ne pas contourner le délai minimal ni le rate limit.

Ne pas imprimer la réponse GraphQL, les jetons ou l’URL du suivi. Si une réponse doit être conservée temporairement, utiliser un fichier privé permissions 0600, puis produire uniquement un bilan expurgé. Pas de capture du ticket complet ni des emails avec le lien personnel.

## Quatre preuves distinctes

| Étape | Preuve attendue | État actuel |
| --- | --- | --- |
| 1. Enregistrement API | Formulaire confirme et ouvre le suivi après réponse valide | Vérifié en environnement isolé ; aucun test de production effectué |
| 2. Persistance | Une seule ligne Contact et son ContactMessage portent le message exact et le marqueur | Vérifié en SQLite dédiée ; aucun dossier client de production consulté |
| 3. Transport | SMTP approuvé accepte chaque message, statuts interprétés selon le backend effectif | Non exécuté : backend console et CONTACT_TO vide |
| 4. Réception | Propriétaire confirme arrivée en réception/indésirables sur chaque boîte autorisée, heure et marqueur | Non exécuté : adresse, autorisations et accès non fournis |

Après autorisation, vérifier la persistance par filtrage sur le message synthétique exact, l’adresse autorisée et la fenêtre prévue ; exiger exactement une ligne et son message. Ne retourner que des booléens/comptages et statuts, jamais nom/email/token/message d’autres demandes. Pour la réception, conserver un bilan heure/marqueur/réception-indésirables et, si disponible, résultats SPF/DKIM/DMARC expurgés. Une acceptation SMTP seule ne valide pas la délivrabilité.

## Traitement des seules données de test

Aucune commande de nettoyage sélectif des contacts n’est fournie dans cette base. La procédure de purge des diagnostics présente sur la branche principale concerne un autre modèle et n’est pas applicable aux contacts de ce runtime. Ne pas lancer de purge globale et ne pas inventer de durée de conservation.

Par défaut, conserver le test identifié jusqu’à décision du propriétaire. Préparer un relevé restreint des seules lignes du marqueur (Contact, ContactMessage et éventuel dossier créé pour ce test) et de leurs dépendances. Toute suppression doit faire l’objet d’une autorisation distincte et ciblée, après dry-run ; ne jamais supprimer un dossier partagé ou un compteur/séquence. Ce lot ne supprime aucune donnée et ne change aucune politique de rétention.
