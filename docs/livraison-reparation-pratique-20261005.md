# Livraison frontend : prise en charge et préparation des preuves réelles

## Base et protection

Version exécutée au départ : cd5e888b9f20be9be6cd4b5cf0d7a5f0b0fa686c, confirmée par https://pixelprowlers.io/_delivery.json et le label de l’image Nuxt. Branche release/pixelprowlers-reparation-pratique-20261005 dans un worktree distinct. La branche initiale feat/pixelprowlers-repositionnement-sasu reste au SHA c0d9c13, avec sa correction backend/.dockerignore et tous ses fichiers non suivis conservés.

Aucun backend, PostgreSQL, migration ou volume ne change. Aucun workflow master : il déploie aussi Django. Utiliser la procédure frontend existante de livraison-vitrine-20261005.md, conserver delivery.yml externe et préparer rollback.yml vers la version réellement remplacée. Aucun secret lu/affiché, installation ou ajout global à Git.

## Références et applicabilité

Les fichiers suivants n’ont pas été localisés dans le dépôt, ses dossiers documentaires ni les worktrees Pixelprowlers accessibles : SECURITY_INDEX.md, SECURITY_GATES.md, ARCHITECTURE_SECURITE.md, POLITIQUES_OPSEC_PRIVACY.md, MODELES_DE_MENACES.md, LOGS_BACKUPS_ACCES.md, UX_INDEX_V1.md, DS_COMPONENT_CATALOG_V1.md, DS_TOKEN_REGISTRY_V1.md, DS_CSS_ARCHITECTURE_V1.md. Leur lecture n’est donc pas revendiquée ; leur chemin ou copie est nécessaire pour en examiner les exigences précises.

Les références de livraison présentes, docs/dossiers.md et le code exécuté ont été examinés. Sur la branche initiale, docs/contact-service.md décrit un backend et un contrat plus récents, non livrés ; docs/diagnostic-retention.md concerne un questionnaire et une purge différents. Ces documents n’autorisent ni migration du contact, ni restauration de P1–P5, ni purge des contacts actuels. Principes maintenus : minimisation, interpolation Vue, zéro nouvelle persistance du formulaire, composants existants, scoped/@apply, focus et inert, tokens vert/ivoire et police locale. Aucune migration du design system ou CSS.

## Implémentation

RepairHandoff.vue fournit trois indications courtes : décrire la panne, convenir des modalités, attendre leur confirmation. Réparation l’affiche juste après le hero avec le lien /contact?besoin=reparation. Contact réutilise son rappel compact. Aucune zone, adresse, date, horaire, délai ou modalité effective n’est supposé. Les six besoins, mapping, détails optionnels, validation et saisie après erreur ne sont pas modifiés.

Le suivi affiche uniquement un enregistrement confirmé après lecture du ticket, invite à conserver le lien personnel et à ne pas le partager. Il ne promet aucune notification délivrée. Les données restent rendues par interpolation, sans v-html ; aucun stockage, tracking, log, upload ou API supplémentaire. Le jeton déjà utilisé par le suivi n’est pas ajouté à une nouvelle URL ni aux preuves.

Aucune nouvelle photographie ni aucun cas réel n’est publié : les assets éditoriaux gardent leur mention générée. Le modèle cas-reparation-collecte.md fournit les faits et autorisations nécessaires, les recommandations photo, l’anonymisation et les exports sans métadonnées. Les originaux non suivis restent intacts.

## Réception : blocage indépendant du frontend

Le runtime utilise EmailBackend console, SMTP_HOST d’exemple, TLS désactivé et CONTACT_TO vide. Une valeur sent ne prouve donc pas du SMTP. Aucun email interne n’est envoyé et la délivrabilité ne peut pas être validée. Aucune demande client ni aucun log de production consulté. Les six fichiers du contrat/persistance/notifications contrôlés ont la même empreinte entre le worktree et le conteneur exécuté.

Le document test-reception-contact.md décrit les destinataires possibles, un marqueur synthétique unique, les préconditions, quatre niveaux de preuve, le correctif proposé dans un lot séparé et le traitement ciblé des données de test. Adresse propriétaire, destinataires autorisés, transport qualifié et preuve de réception restent requis. Aucun envoi réel tant que ces éléments ne sont pas satisfaits.

## Vérification et livraison

34 tests existants réussis après le build initial qui génère les tsconfig Nuxt, sans installation. Aucune logique nouvelle ne justifie une batterie de tests de textes. Revue navigateur des pages touchées à 390/768/1440, menu clavier, focus, liens, présélections, images et métadonnées. Soumission dédiée vers SQLite/messagerie mémoire avec connexions sortantes bloquées, échec simulé, conservation et lecture du suivi confirmés. Aucun test SMTP de production.

L’artefact final doit être figé après commit : générer _delivery.json avec ce SHA avant build, retirer seulement cette source temporaire après build, contrôler le contenu de l’artefact et son SHA-256, valider avant bascule. Déployer Nuxt avec l’override existant et --no-deps --no-build ; comparer les images backend avant/après. Contrôler le SHA servi, les pages et les assets publics ; appliquer le rollback si régression critique.

Le compte rendu final contient le SHA réellement publié, les captures finales et les preuves en ligne. Les sections de cas réels et les coordonnées pratiques non confirmées restent hors publication. Retour arrière : /opt/pixelprowlers-deploy-backups/frontend-20261005-<SHA livré>/rollback.yml depuis /opt/pixelprowlers, avec docker compose -f compose.yml -f <override> up -d --no-deps --no-build nuxt.
