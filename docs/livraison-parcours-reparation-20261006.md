# Parcours visuel de réparation — 6 octobre 2026

## Base et conservation

Base de production vérifiée dans `_delivery.json` : `f16e604c96b93b409c06336e31fc06e907c367a4`. Image Nuxt remplacée : `sha256:de2781708d64d25d3530c4e25ccfbe859a6441082687f2304023c83a7cb4e3d7`. Worktree distinct `pixelprowlers-parcours-reparation-20261006`, branche `release/pixelprowlers-parcours-reparation-20261006`. Le dépôt principal c0d9c13, sa modification backend/.dockerignore et ses fichiers non suivis sont préservés. AGENTS.md du projet vide ; règles globales appliquées. Aucun ajout de dépendance, modification backend, migration de production, volume ou workflow global.

## Grille et limite métier

Grille `reparation-20261006-v1-sans-tarifs`, datée du 6 octobre 2026. Quatre familles déjà annoncées sur la page publiée : portable, fixe, téléphone, tablette. Console, manette et autre sont prévus dans le modèle, mais pas proposés comme prestations confirmées ; lien de contact général disponible.

La recherche ciblée dans les sources et documents des bases locale et publiée ne trouve aucun tarif matériel confirmé, aucune liste de modèles avec prestations tarifées, aucune inclusion/exclusion tarifaire validée, ni coût ou déduction du diagnostic. Ces informations ont été demandées en une seule clarification. Aucun tarif du site de référence n’est repris. Les montants synthétiques sont définis uniquement dans les tests et ne sont jamais importés par la configuration publique.

**Aucun parcours ne dispose actuellement d’un montant validé. L’objectif d’estimation chiffrée n’est donc pas réalisé.** Le résultat annonce explicitement une estimation après diagnostic et un coût à préciser avant prise en charge, sans montant nul ou diagnostic gratuit supposé. Les types et règles supportent prix fixe TTC, fourchette TTC, diagnostic tarifé avec déduction documentée et estimation indisponible. Une règle spécifique ne s’applique pas à un modèle inconnu. Ni addition de symptômes ni conversion automatique d’un symptôme en cause.

## Parcours et contrat

Appareil → problème → budget avant toute coordonnée. Cartes SVG originales locales ; observations propres à chaque famille, autres symptômes et inconnu accessibles. Modèle demandé seulement si la grille dispose de modèles utiles. Retour compatible conservé ; changement de famille invalide symptôme/modèle ; reset explicite. État créé dans chaque appel du composable, aucun stockage navigateur ni données personnelles en URL.

Micro-soudure expliquée conditionnellement dans les résultats électroniques et dans la section éditoriale conservée. Illustration générée signalée, aucune machine fictive ni cas client supposé. Précaution batterie/chauffe et confidentialité conservées.

Formulaire Contact intégré et conservé dans le DOM lors des retours, avec contexte réactif : appareil, modèle connu, symptôme, prestation envisagée, repère présenté et version de grille. Besoin reparation, mapping API materiel/diagnostic, coordonnées et limites historiques inchangés. Message enrichi limité à 4000 caractères sans troncature ; description 20–500. Attente, double envoi et erreur avec conservation. Ancien /contact?besoin=reparation inchangé. CTA accueil/menu vers le parcours ; demande directe disponible.

## Vérifications

Tests unitaires : règles tarifaires, absence/incohérence, modèle inconnu, incompatibilité, retours, reset, isolation des visiteurs, recalcul, message enrichi, limite API et réessai avec contexte changé. Build Nuxt. Vue-tsc : 22 erreurs strictement identiques à f16e604 après normalisation des numéros de lignes ; aucune nouvelle erreur identifiée. Le contrôle de types global reste en échec et n’est pas déclaré réussi.

Navigateur Chromium à 390, 768 et 1440 px : deux colonnes mobile, contrôles natifs au clavier, focus à chaque étape, retours, reset, absence de débordement, résultat avant formulaire et conservation après erreur. Formulaire envoyé uniquement vers Django en conteneur dédié, SQLite /tmp dédiée, e-mails en mémoire et connexions sortantes bloquées. Un Contact et un ContactMessage persistés, mapping et contexte actualisé vérifiés ; ticket affiché. Ce test prouve l’enregistrement isolé, pas la délivrabilité.

SMTP connu au 6 octobre : backend console, CONTACT_TO absent ; réception externe non testée. Aucun formulaire envoyé en production ni notification réelle à un tiers.

## Livraison et retour arrière

Workflow historique limité à master/workflow_dispatch : il redéploie Django et migre, donc exclu. Branche dédiée seulement. Artefact .output lié au SHA de commit par métadonnée générée avant build, archive vérifiée par SHA-256 ; image runtime existante sans téléchargement/installation ; préflight sans réseau ; surcharge externe delivery.yml et `up -d --no-deps --no-build nuxt`. Images et conteneurs Django/PostgreSQL comparés avant/après. Référence de retour arrière : image Nuxt f16e604 ci-dessus et rollback.yml créé avant bascule. Les preuves exactes SHA/captures et le statut public figurent dans le compte rendu final de livraison.
