# Livraison commerciale et Contact — 6 octobre 2026

## Base et périmètre

Production constatée : 56e028bb293c596ce0475e9683d2c11badd30b52, métadonnée publique et image Nuxt sha256:e1202855f3501e063a1ba02e9257a73a96ae6dd63b76f6fc1e2efd9b5cdf6c05. Worktree distinct pixelprowlers-vitrine-commerciale-20261006, branche release/pixelprowlers-vitrine-commerciale-20261006. Le dépôt initial, sa branche c0d9c13, backend/.dockerignore et tous les fichiers non suivis restent conservés. Aucun ajout global, nouvelle dépendance, secret, asset non autorisé ou modification backend.

## Changements

Accueil : hero demandé, trois symptômes, composant/micro-soudure, réemploi avec CTA propre, portrait existant de Grégory, trois activités numériques et contact. Méthode et avertissements commerciaux répétés retirés. Les illustrations gardent leur signalement généré et ne représentent pas des exemplaires vendus.

Réparation : explication courte de micro-soudure, cartes de symptômes, batterie/chauffe visible et troisième étape « Organiser la prise en charge ». Réemploi : usages et demande de disponibilités, aucun stock supposé. Services numériques : trois entrées, ancres et destinations historiques conservées, autorisations regroupées. Formation : objectifs observables et format convenu avec le groupe ; les modalités non confirmées et les réserves répétées sont retirées. À propos : visage et rôle visibles avant le parcours.

Contact : besoin contextualisé, choix repliables retirés du DOM lorsqu’ils sont fermés, retour du focus, description avant coordonnées, nom distinct de société, compteur, erreurs et champs optionnels. Les six codes, l’allowlist et les valeurs API historiques sont inchangés. Une sélection différente conserve les saisies ; seules les précisions du besoin actif sont envoyées. Aucun stockage nouveau. Attente, double-envoi et conservation après erreur restent dans useContactForm. Nom 160, email 254, téléphone 40, description 20–500, message enrichi 4000 maximum. Confidentialité près de l’action.

Urgence : CTA contextuel vers le formulaire, lien secondaire dans le menu, aide courte près de la description. La confirmation d’absence d’accès privés reste obligatoire : urgencies/serializers.py la valide côté serveur. Son retrait demanderait un lot backend distinct. Référence enregistrée ne signifie plus prise en charge humaine. Audit : exemples de succès et réponse 24 h sans preuves retirés, y compris les rappels historiques accessibles. Bilan numérique : nombre calculé depuis les quatre questions effectives ; aucune création de dossier annoncée avant la mutation.

## Preuves et informations métier

Aucun cas complet autorisé (symptôme, cause, intervention, résultat) n’est disponible dans la documentation examinée. Les originaux non suivis ne sont pas publiés : aucune présomption sur les droits, l’appareil ou les clients. Le portrait déjà publié en randonnée est réutilisé ; aucune scène d’établi ni photo de machine assemblée n’est présentée comme réelle sans preuve. Voir cas-reparation-collecte.md.

Zone, dépôt/expédition/collecte/déplacement, rendez-vous, adresse d’accueil et autorisation d’usage commercial du téléphone ont été demandés ensemble. Sans réponse, seules les formulations neutres sont publiées, aucun placeholder.

## SMTP : constat distinct

Relevé runtime du 6 octobre : EMAIL_BACKEND console, EMAIL_HOST smtp.example.com, port 587, TLS/SSL désactivés, CONTACT_TO absent. Aucun secret, demande client ou log de production consulté ; aucune soumission de production. Le transport SMTP et la réception restent non testés et bloqués. Le correctif proposé et le protocole d’envoi autorisé sont dans test-reception-contact.md ; ils restent séparés de cette livraison. Une confirmation d’enregistrement ne prouve ni envoi SMTP ni réception dans une boîte.

## Validation et procédure

Mesures initiales confirmées à 1363 × 936 : coordonnées 1387 px, description 1851 px, bouton 2102 px. Captures avant conservées dans /tmp/pixelprowlers-commercial-before-ps5kjxh5. Les mesures finales et les captures publiées figurent dans le compte rendu.

Tests existants plus contrats nom/société, changement de besoin et CTA Urgence : 39 réussis au premier passage. Build Nuxt réussi. Le contrôle vue-tsc retourne 22 erreurs également présentes sur la base 56e028 (même liste, décalage de ligne du test modifié seulement), ainsi qu’un avertissement de plugin vue-router non exporté. Il n’est donc pas déclaré réussi ; aucune erreur nouvelle identifiée. Pas d’installation pour corriger un prérequis historique dans ce lot.

Avant bascule : artefact final après commit, SHA dans _delivery.json avant build, suppression de la seule source temporaire ensuite, SHA-256 de l’archive, préflight sans réseau. Push de la branche release seulement : le workflow master redéploie aussi Django et reste exclu. Depuis /opt/pixelprowlers, override delivery.yml externe, up -d --no-deps --no-build nuxt. Conserver les overrides précédents et générer rollback.yml vers l’image 56e028 avant bascule. Comparer images ET conteneurs Django/PostgreSQL avant/après. Vérifier SHA public, rendu, assets et navigation ; aucune soumission publique.
