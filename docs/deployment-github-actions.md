# Déploiement GitHub Actions PixelProwlers

Le workflow `Deploy Preprod` déploie automatiquement chaque push sur `master`
vers le VPS. Le checkout `/opt/pixelprowlers` est un artefact de déploiement :
il ne doit jamais être modifié manuellement.

## Architecture déployée

- VPS : `46.202.131.25`, SSH `striker` sur le port `2222` ;
- checkout applicatif : `/opt/pixelprowlers` ;
- sauvegardes hors checkout : `/opt/pixelprowlers-deploy-backups` ;
- frontal TLS : conteneur Caddy administré hors de ce dépôt, seul service
  PixelProwlers publié sur les ports `80` et `443` ;
- réseau partagé : `pixelprowlers_default` ;
- services de ce dépôt : `postgres`, `django` et `nuxt` ;
- PostgreSQL : port hôte facultatif limité à `127.0.0.1:5433` ;
- Django et Nuxt : ports `8000` et `3000` exposés uniquement au réseau Docker.

Caddy rejoint Django et Nuxt par `pixelprowlers_default`. Il ne faut pas
réintroduire Nginx ni publier directement Django ou Nuxt sans revalider cette
architecture.

## Configuration sensible

Le fichier `/opt/pixelprowlers/.env` reste sur le VPS, avec le mode `0600`. Il
n'est ni synchronisé vers GitHub ni inclus dans les logs. Les variables
minimales sont celles de `.env.example`, notamment la clé Django, la connexion
PostgreSQL, les hôtes autorisés et la configuration SMTP.

Les secrets GitHub Actions requis sont :

- `VPS_SSH_KEY` : clé SSH privée dédiée ;
- `VPS_KNOWN_HOSTS` : entrée vérifiée pour `[46.202.131.25]:2222`.

L'entrée `known_hosts` doit provenir du serveur via une connexion déjà
authentifiée. Le workflow utilise `StrictHostKeyChecking=yes` et n'accepte pas
automatiquement une nouvelle identité du VPS.

## Séquence de déploiement

1. Préparer la clé SSH et le `known_hosts` vérifié.
2. Détecter les modifications suivies dans `/opt/pixelprowlers` et, si
   nécessaire, les sauvegarder sous forme de patch externe.
3. Récupérer `origin/master`, positionner le checkout exactement sur le SHA du
   workflow et vérifier cette égalité. Les fichiers non suivis sont conservés.
4. Valider Compose et construire les images.
5. Démarrer PostgreSQL et attendre réellement `pg_isready`.
6. Créer un `pg_dump` externe, restrictif et non vide.
7. Exécuter `manage.py check`, puis les migrations une seule fois via un
   conteneur ponctuel.
8. Démarrer Django et Nuxt et attendre leurs contrôles HTTP internes.
9. Vérifier le SHA distant puis HTTPS et `/health/` via Caddy.
10. En cas d'échec après synchronisation, restaurer le SHA applicatif précédent
    et redémarrer l'ancienne stack. La sauvegarde PostgreSQL est conservée pour
    une restauration contrôlée ; elle n'est jamais restaurée automatiquement.

Les attentes PostgreSQL, Django et Nuxt sont bornées et bloquantes. Un timeout
affiche au maximum 40 lignes du service concerné avant de retourner un code non
nul.

## Migrations et sauvegardes

Les migrations sont pilotées uniquement par le workflow. L'image Django lance
Gunicorn directement et ne migre pas au démarrage.

Chaque déploiement crée un dossier restrictif :

```text
/opt/pixelprowlers-deploy-backups/<horodatage>-<sha>/
```

Il contient le SHA précédent, l'éventuel patch des modifications suivies et le
dump PostgreSQL. Le déploiement s'arrête si le dump échoue ou est vide. Aucun
volume n'est supprimé et `docker compose down -v` est interdit.

## Vérifications opérateur

Après un run réussi :

```bash
cd /opt/pixelprowlers
git rev-parse HEAD
docker compose ps
curl -fsSI https://pixelprowlers.io
curl -fsS https://pixelprowlers.io/health/
```

Ne pas afficher `.env` ni le contenu des sauvegardes dans les journaux.

## Rollback

Le workflow tente automatiquement un rollback applicatif vers le SHA précédent
si le build, le démarrage ou la vérification échoue. Il reconstruit les images
de ce SHA et relance seulement la stack PixelProwlers.

Une restauration PostgreSQL est une opération distincte et potentiellement
destructive. Elle doit être décidée après analyse de la migration et utiliser
le dump du déploiement concerné. Ne jamais supprimer le volume PostgreSQL pour
effectuer un rollback.

## Règles d'exploitation

- ne jamais développer ni corriger directement dans `/opt/pixelprowlers` ;
- placer toute configuration spécifique dans `.env` ou dans l'infrastructure
  Caddy hors dépôt ;
- ne jamais utiliser `git pull` pour déployer ;
- ne jamais lancer `git clean`, supprimer les fichiers non suivis ou supprimer
  les volumes ;
- toute modification suivie détectée sur le VPS est sauvegardée, puis remplacée
  par le SHA exact du workflow.
