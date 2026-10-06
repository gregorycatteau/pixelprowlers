# Livraison ciblée du backend historique

**Préparation seulement. Aucun push, déploiement ou changement de réglage de production autorisé dans ce lot.** Les commandes serveur ci-dessous sont la procédure pour une décision ultérieure. Ne pas les exécuter automatiquement. Rapport : [qualification](../../docs/security/backend-historique-correctif-20261006.md).

## 1. Construire et qualifier localement l'image exacte

Depuis la racine du worktree dédié, après commits et revue :

```bash
DELIVERY_SHA=$(git rev-parse HEAD)
# This alias is created locally from the verified installed image; never replace it.
# If it already exists, require the exact same ID instead of overwriting it.
BASE_TAG=pixelprowlers-django:security-base-efd98e84bc44
BASE_ID=sha256:efd98e84bc445b342a64b05cb63e40cae0fa62f7e920676261db4f4c1520fd23
if docker image inspect "$BASE_TAG" >/dev/null 2>&1; then
  test "$(docker image inspect -f '{{.Id}}' "$BASE_TAG")" = "$BASE_ID"
else
  docker image tag "$BASE_ID" "$BASE_TAG"
fi
docker build --pull=false --network=none \
  --build-arg BASE_IMAGE="$BASE_TAG" \
  --build-arg DELIVERY_SHA="$DELIVERY_SHA" \
  -f ops/backend-security/Dockerfile \
  -t "pixelprowlers-django:security-${DELIVERY_SHA:0:12}" backend
```

Le contexte est **backend uniquement**, avec sa `.dockerignore` historique. Pas de `.env`, logs, DB locale, média ou archive. Source active sous `/srv/pixelprowlers-backend`, seules applications historiques ; aucun catalogue/comptes/diagnostic récent. Base historique installée localement, versions consignées ; aucune installation/pull. `collectstatic` local sans DB et avec valeurs réservées au build ; elles ne deviennent pas des réglages d'exploitation. Le CMD lance Gunicorn **sans migrate**.

Réexécuter les tests sur cette image, sans bind de source applicative, avec `QUAL_SOURCE=/srv/pixelprowlers-backend` et le dossier `ops/backend-security` monté en lecture seule dans `/qualification`. Le module `qualification.py` refuse tout hôte autre que les deux conteneurs dédiés nommés ; credentials et clé synthétiques réservés aux fixtures, messagerie mémoire et SMS/webhook désactivés. Aucun `.env` du dépôt original monté.

Exemple d'environnement de qualification, réseau Docker **interne**, deux instances `postgres:15-alpine` déjà disponibles :

```bash
docker network create --internal pixelprowlers-backend-qual-20261006
# Ne pas recréer les conteneurs existants ; vérifier d'abord leur nom/identité.
docker run -d --name pixelprowlers-security-db-20261006 \
  --network pixelprowlers-backend-qual-20261006 --tmpfs /var/lib/postgresql/data \
  -e POSTGRES_DB=qualification_only -e POSTGRES_USER=qualification_owner \
  -e POSTGRES_PASSWORD=qualification-only-not-production \
  --pull=never postgres:15-alpine
# Même commande avec le nom pixelprowlers-security-restore-20261006 pour la seconde instance.
```

Exécuter `qualification.py migrate` seulement sur cette base dédiée, puis `qualification.py test audits crm urgencies --verbosity 1`. Pour l'import de citations, prévoir `/srv/pixelprowlers-backend/logs` writable dans le conteneur ; ne pas rendre le source partagé writable. Les tests créent leur base temporaire avec le propriétaire de qualification, puis la détruisent ; le rôle applicatif sans CREATEDB est testé séparément sur la base synthétique persistante.

Appliquer `runtime-role.sql` avec `db_name=qualification_only`, sous `qualification_owner`, puis donner LOGIN et le mot de passe synthétique **uniquement dans les instances dédiées**. Exécuter `qualification-runtime-check.py` avec `QUAL_DB_USER=pixelprowlers_app`, puis le contrôle des 16 contrats `qualification-contracts.py`. Le helper de restauration compare les données originales : le lancer **avant de modifier la base source après son dump**.

Le module WSGI de qualification permet de démarrer Gunicorn de l'image avec les réglages contrôlés, sans copie de secret réel. Faire pointer la vitrine compilée `1205eeb` sur un proxy local de même origine pour conserver cookies et Origin. Vérifier le parcours de contact/ticket/réponse à 390, 768 et 1440 px. La route frontend de résultat refonte a une limite identifiée dans le rapport : ne pas la déclarer opérationnelle.

Commande des tests sur l'image exacte (choisir un nom de conteneur de contrôle encore libre) :

```bash
QUAL_DIRECTORY="$PWD/ops/backend-security"
CORRECTED_IMAGE_ID=$(docker image inspect -f '{{.Id}}' "pixelprowlers-django:security-${DELIVERY_SHA:0:12}")
docker run --name pixelprowlers-security-exact-image-tests-20261006 \
  --network pixelprowlers-backend-qual-20261006 \
  --tmpfs /srv/pixelprowlers-backend/logs \
  --mount "type=bind,src=$QUAL_DIRECTORY,dst=/qualification,readonly" \
  -e QUAL_SOURCE=/srv/pixelprowlers-backend \
  --entrypoint python --pull=never "$CORRECTED_IMAGE_ID" \
  /qualification/qualification.py test audits crm urgencies --verbosity 1
```

Exporter après réussite et conserver le SHA-256 du tar, le ID image, le label de révision et les résultats :

```bash
umask 077
CORRECTED_IMAGE_ID=$(docker image inspect -f '{{.Id}}' "pixelprowlers-django:security-${DELIVERY_SHA:0:12}")
docker save "pixelprowlers-django:security-${DELIVERY_SHA:0:12}" \
  -o /tmp/pixelprowlers-backend-fix-20261006/backend-security-image.tar
sha256sum /tmp/pixelprowlers-backend-fix-20261006/backend-security-image.tar \
  > /tmp/pixelprowlers-backend-fix-20261006/backend-security-image.tar.sha256
CORRECTED_IMAGE_ID="$CORRECTED_IMAGE_ID" \
DELIVERY_DIRECTORY=/tmp/pixelprowlers-backend-fix-20261006/delivery \
  bash ops/backend-security/prepare-delivery.sh
```

`delivery.yml` et `rollback.yml` ne changent que **django.image, pull_policy et command**. Aucun mount, volume, port, autre service ni variable d'environnement modifié. Retour arrière également sans migrate. Le tar et le dump restent hors Git, fichiers 600. Aucun registre externe ni branche distante publié dans cette tâche.

## 2. Avant une future livraison serveur

Existant : SSH `striker@46.202.131.25`, port 2222 ; Compose `/opt/pixelprowlers/compose.yml`, projet `pixelprowlers`, service `django`, réseau partagé `pixelprowlers_default`, PostgreSQL `pixelprowlers-postgres`, volume `pixelprowlers_postgres_data`. Revalider ces identités ; ne pas supposer le checkout serveur égal à l'image qui tourne.

1. Faire approuver le commit, l'image, le périmètre backend seul et les limites de messagerie/audits. Pas de workflow global : `.github/workflows/deploy-preprod.yml` peut builder/migrer/provisionner/recréer plusieurs composants sur push master ou dispatch.
2. Conserver l'image précédente **par ID** `sha256:1fd7de0d2b3028177417e877683cced740ac40955ec1ce25aba93027e671d139`, les ID Django/Nuxt/PostgreSQL et les montages/référence frontend. Ne pas supprimer l'ancienne image.
3. Vérifier que l'environnement issu du Compose courant correspond à celui du Django actif. Comparaison en mémoire par opérateur, sans imprimer de valeurs ni exporter des secrets ; le checkout Compose a déjà des modifications serveur à préserver. Ni `git reset`, ni copie globale de compose, ni remplacement de `.env`.
4. Identifier la DB réelle depuis la configuration Django et confirmer qu'elle correspond à POSTGRES_DB de **ce** conteneur PostgreSQL. Ne pas sélectionner une base par simple convention de nom. Relever les métadonnées, pas les lignes clients.
5. Vérifier DEBUG=False, SECRET_KEY existante, domaines/proxy/CORS/session HTTPS. Ne pas activer SMTP/SMS/rappels, créer de compte, injecter de clé ni réduire les rôles pendant ce déploiement de code. La nouvelle image n'active pas ces fonctions.
6. Importer le tar approuvé, vérifier sa somme et l'ID/label. Préparer une copie distincte de restauration/préproduction si disponible, avec accès réseau et messagerie neutralisés ; aucune donnée client de cette copie n'est à rendre publique.
7. Faire la sauvegarde ci-dessous **avant** recréation Django. Arrêter si son contrôle ou son stockage échoue.

### Sauvegarde future de production — à exécuter après approbation

La valeur EXPECTED_DATABASE doit venir de la vérification ci-dessus. Son nom n'est pas une preuve d'identité ; EXPECTED_PG_ID doit être renouvelé si le conteneur change. Le script refuse une racine de backup déjà ouverte à d'autres comptes.

```bash
umask 077
# Répertoire neuf et protégé, sur stockage dont espace/rétention ont été vérifiés.
mkdir -m 700 /opt/pixelprowlers-deploy-backups/backend-security-db
PG_CONTAINER=pixelprowlers-postgres \
EXPECTED_PG_ID=08996c53c0aefd5119c56fcd64f3f4bb55b08f18e7b9b83310d7d16ba68ddaf5 \
EXPECTED_DATABASE='<base confirmée, sans valeur supposée>' \
BACKUP_ROOT=/opt/pixelprowlers-deploy-backups/backend-security-db \
  bash /chemin/controle/backup.sh
```

Export cohérent complet, incluant tables `api` héritées, sessions et utilisateurs ; il doit donc rester **sensible**. Contrôle SHA ne démontre pas une restauration de production. Qualifier une restauration dédiée avant le changement de privilèges SQL. Conserver la sauvegarde initiale de qualification et ses preuves ; ne pas les confondre avec l'export de production.

Pas de médias montés sur le backend observé aujourd'hui. Si ce constat change, arrêter et ajouter une sauvegarde cohérente du montage concerné. Conserver les références de secrets dans le coffre existant, sans les recopier dans ce répertoire de livraison ou dans Git.

### Recréation future Django seule

Sur le serveur, avec overrides approuvés dans un répertoire externe au checkout :

```bash
# Lecture de schéma uniquement, dans un conteneur temporaire de la nouvelle image.
# Premièrement vérifier que Compose fournit les mêmes réglages que le service actif.
docker compose -p pixelprowlers -f /opt/pixelprowlers/compose.yml \
  -f /opt/pixelprowlers-deploy-backups/backend-security/delivery.yml \
  run --no-deps --rm -T django python manage.py showmigrations --plan
# Aucune nouvelle migration n'est prévue. Arrêter en cas de divergence.
# La commande n'utilise ni build, ni migrate, ni autre service.
docker compose -p pixelprowlers -f /opt/pixelprowlers/compose.yml \
  -f /opt/pixelprowlers-deploy-backups/backend-security/delivery.yml \
  up -d --no-deps --no-build --pull never django
```

Préserver la configuration Caddy, le frontend et les volumes. Ne pas utiliser `up` sans nom de service, `down`, `--remove-orphans`, un workflow global ou le Dockerfile historique dont CMD migre automatiquement. Les fichiers du correctif n'introduisent aucune migration : diff modèles/migrations/manifests nul et `makemigrations --check --dry-run` réussi en qualification.

Contrôles après recréation :

- ID/label et chemins importés de Django conformes ; santé puis connexion DB confirmée par métadonnées, car `/health/` historique est une réponse statique.
- ID et images de Nuxt/PostgreSQL, montages et volume **identiques** à l'avant ; metadata frontend `1205eeb` conservée.
- Pages et assets publics ; exécuter `post-delivery-check.py` seulement après livraison autorisée : refus des sélections privées, suppression et introspection, sans consulter de dossier ni soumettre de formulaire.
- Test du formulaire/ticket/réponse en préproduction ou avec boîte explicitement contrôlée et statut console non trompeur. Aucune soumission de production à un tiers par défaut. Sur production, une réception email réelle n'est affirmée qu'après observation de la boîte contrôlée.
- Ne pas promouvoir audit/refonte comme qualifiés tant que signature et UI indiquées au rapport ne sont pas résolues.

## 3. Retour arrière de code

En cas de régression critique, préserver les demandes créées pendant la période : **ne pas restaurer la DB active**. L'ancien code est compatible avec le même schéma et aucune migration n'est appliquée.

```bash
docker compose -p pixelprowlers -f /opt/pixelprowlers/compose.yml \
  -f /opt/pixelprowlers-deploy-backups/backend-security/rollback.yml \
  up -d --no-deps --no-build --pull never django
```

Recontrôler ancienne image, ID Nuxt/PostgreSQL, volumes et santé. Le rollback restaure également les failles anciennes ; envisager d'abord le confinement ci-dessous et un correctif complémentaire. Si retour à l'ancien backend nécessaire, faire approuver et appliquer le confinement `/graphql/` pendant sa durée. L'ancien code ne doit pas être déclaré sécurisé après rollback.

Le changement de rôle DB est **séparé** de cette livraison. Son rollback est la remise en service de la référence d'identifiants précédente par l'environnement Django uniquement ; aucun transfert de propriétaire, DROP OWNED ou restauration de données. Qualification réalisée par bascule entre rôle de maintenance et rôle applicatif sur les instances dédiées.

## 4. Confinement temporaire proposé — non appliqué

[confinement.caddy](confinement.caddy) est un snippet précis à insérer dans chacun des blocs de domaine existants, avant reverse_proxy. Faire `caddy validate` sur une copie de configuration, puis recharger seulement après approbation et contrôle du vrai Caddyfile. Le snippet seul n'est pas un Caddyfile complet et ne doit pas remplacer le fichier existant.

Effet : toutes les opérations GraphQL renvoient **503**, y compris contact, ticket, diagnostic et réservations ; vitrine et assets restent consultables. Ne pas filtrer uniquement les noms d'opération HTTP : alias/fragments/mutations groupées rendraient ce faux confinement insuffisant. Pas de changement Caddy appliqué par ce lot.
