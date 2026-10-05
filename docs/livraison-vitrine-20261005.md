# Livraison limitée de la vitrine — 5 octobre 2026

La branche repart de `1683fa233434b612a2a8b8b6837074050ece73c5` : son accueil correspond au HTML servi et les empreintes de quatre fichiers Django correspondent aux fichiers exécutés. Le checkout VPS et le dernier workflow réussi indiquent `4e243c6`, mais les conteneurs exécutent des images construites le 14 juillet. La référence exacte de retour arrière est donc l'image Nuxt `sha256:4e80a0448388447d72f9194e73696e2617aac7763f52ea27c7763e158a825ee3`, pas le checkout.

## Périmètre

Accueil, réparation/micro-soudure, présentation du réemploi, services numériques et formations, navigation, styles, sept images WebP, police locale et licence. Le contact existant et son contrat GraphQL sont conservés. Les liens réparation ouvrent `/contact`. Le catalogue est remplacé par une présentation et une demande de disponibilité, sans exemplaire, prix ou stock. Les anciens liens vers le diagnostic sont redirigés vers le contact.

Aucun changement Django, PostgreSQL, Compose ou du workflow global ; aucune migration. Les 17 commits de la branche matériel ne sont pas livrés. Le checkout VPS et sa modification locale de Compose restent intacts.

## Validation

Build Nuxt et six tests de schémas de cette base réussis. Navigateur à 390, 768 et 1440 px : images responsives, police, liens, ancres services, menu par Entrée et fermeture par Échap, absence de débordement et d'exception JavaScript. Accueil : 318 mots après adaptation des CTA. Les canoniques pointent vers pixelprowlers.io. Les URL publiques de l'API utilisent `/graphql/`, jamais une boucle locale dans la configuration de production.

Contact : soumission depuis le navigateur vers un conteneur dédié, utilisant le code backend de la base compatible et SQLite dans `/tmp`, SMTP remplacé par le backend mémoire et connexions sortantes bloquées. Un contact et un message persistent ; le navigateur ouvre le ticket. Ce test qualifie le contrat et l'enregistrement ; il ne qualifie pas la délivrabilité SMTP réelle. Aucun message de test envoyé en production.

## Déploiement et retour arrière

Le push de cette branche ne déclenche pas le workflow (limité à master). Ne pas lancer ce workflow : il reconstruit toute la stack et migre Django.

Les métadonnées `_delivery.json` sont générées avec le SHA Git avant compilation, puis incluses dans le manifeste statique Nitro. Le build autonome `.output` est archivé et son empreinte SHA-256 contrôlée après transfert SSH. Le fichier source temporaire de métadonnées est retiré après compilation ; il ne fait pas partie du code applicatif. Une image contenant cet artefact est construite à partir de l'image runtime actuellement exécutée, sans installer de dépendances. Un conteneur isolé valide l'accueil et le SHA des métadonnées avant bascule. Docker Compose reçoit une surcharge externe avec uniquement la nouvelle image Nuxt et ses URL publiques relatives. La commande `up -d --no-deps --no-build nuxt` conserve Django, PostgreSQL et les volumes.

L'image précédente est taguée et une surcharge `rollback.yml` est conservée sous `/opt/pixelprowlers-deploy-backups/frontend-20261005-<SHA>/`. Retour arrière, depuis `/opt/pixelprowlers` :

```sh
docker compose -f compose.yml -f /opt/pixelprowlers-deploy-backups/frontend-20261005-<SHA>/rollback.yml up -d --no-deps --no-build nuxt
```

Les métadonnées externes gardent les empreintes des trois images précédentes. Aucun volume n'est supprimé et aucune restauration de base n'est nécessaire pour cette livraison frontend.
