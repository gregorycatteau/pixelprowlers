# Deploiement GitHub Actions PixelProwlers

Ce document decrit le deploiement preproduction vers le VPS Hostinger avec Caddy comme frontal TLS public.

## Architecture cible

- Domaine principal : `pixelprowlers.io`
- Domaine secondaire : `www.pixelprowlers.io`
- VPS : `46.202.131.25`
- Utilisateur SSH : `striker`
- Port SSH : `2222`
- Dossier applicatif : `/opt/pixelprowlers`
- Frontal public : Caddy sur `80` et `443`
- Gateway applicative Docker : Nginx interne sur `127.0.0.1:8080`
- Services internes Docker :
  - Nuxt : `127.0.0.1:3000`
  - Django : `127.0.0.1:8001`
  - PostgreSQL : `127.0.0.1:5433`

Caddy doit rester le seul service public sur `80` et `443`.

## Secrets GitHub a creer

Dans GitHub : `Settings` -> `Secrets and variables` -> `Actions` -> `Repository secrets`.

Creer :

```text
VPS_HOST=46.202.131.25
VPS_USER=striker
VPS_PORT=2222
VPS_SSH_KEY=<cle privee dediee GitHub Actions>
```

Ne jamais commiter la cle privee. Ne jamais la copier dans un fichier du depot.

## Generer une cle SSH dediee

Depuis la machine d'administration :

```bash
ssh-keygen -t ed25519 -f ~/.ssh/pixelprowlers_github_actions -C "github-actions-pixelprowlers"
```

Tester la connexion avec la cle privee dediee :

```bash
ssh -i ~/.ssh/pixelprowlers_github_actions -p 2222 striker@46.202.131.25
```

Si un autre acces SSH est deja valide, ajouter le contenu de :

```bash
cat ~/.ssh/pixelprowlers_github_actions.pub
```

dans :

```bash
/home/striker/.ssh/authorized_keys
```

Permissions attendues cote VPS :

```bash
chmod 700 /home/striker/.ssh
chmod 600 /home/striker/.ssh/authorized_keys
chown -R striker:striker /home/striker/.ssh
```

Tester :

```bash
ssh -i ~/.ssh/pixelprowlers_github_actions -p 2222 -o BatchMode=yes -o ConnectTimeout=15 striker@46.202.131.25 "whoami && hostname && pwd"
```

## Preparer le VPS

Creer le dossier applicatif :

```bash
sudo mkdir -p /opt/pixelprowlers
sudo chown -R striker:striker /opt/pixelprowlers
```

Creer le fichier d'environnement reel sur le VPS :

```bash
cd /opt/pixelprowlers
nano .env
chmod 600 .env
```

Variables minimales attendues :

```env
DJANGO_SECRET_KEY=<secret long et unique>
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=pixelprowlers.io,www.pixelprowlers.io
DJANGO_CSRF_TRUSTED_ORIGINS=https://pixelprowlers.io,https://www.pixelprowlers.io
DJANGO_SECURE_SSL_REDIRECT=false
DJANGO_SESSION_COOKIE_SECURE=true
DJANGO_CSRF_COOKIE_SECURE=true
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=false
DJANGO_SECURE_HSTS_PRELOAD=false
CORS_ALLOWED_ORIGINS=https://pixelprowlers.io,https://www.pixelprowlers.io
POSTGRES_DB=pixelprowlers
POSTGRES_USER=pixelprowlers
POSTGRES_PASSWORD=<mot de passe fort>
CONTACT_TO=<adresse destination>
CONTACT_FROM=<adresse expediteur autorisee>
SMTP_HOST=<serveur smtp>
SMTP_PORT=587
SMTP_USER=<utilisateur smtp>
SMTP_PASS=<mot de passe smtp>
SMTP_SECURE=false
```

Ne pas activer `DJANGO_SECURE_SSL_REDIRECT=true` tant que Caddy transmet correctement `X-Forwarded-Proto` et que les tests HTTPS ne confirment aucune boucle. Caddy termine TLS, puis proxifie vers `127.0.0.1:8080` en HTTP local.

Ne pas activer `DJANGO_SECURE_HSTS_PRELOAD=true`.
Ne pas activer `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=true` pour l'instant.

## Configuration Caddy attendue

Caddy doit proxifier vers la gateway applicative Docker exposee localement sur `127.0.0.1:8080`.

Exemple a adapter apres sauvegarde du Caddyfile existant :

```caddyfile
pixelprowlers.io, www.pixelprowlers.io {
    encode gzip zstd

    reverse_proxy 127.0.0.1:8080

    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "SAMEORIGIN"
        Referrer-Policy "strict-origin-when-cross-origin"
        Permissions-Policy "geolocation=(), microphone=(), camera=()"
    }
}
```

Avant toute modification :

```bash
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.backup-$(date +%Y%m%d-%H%M%S)
```

Verifier puis recharger :

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
sudo systemctl status caddy --no-pager
```

Si la validation echoue, ne pas recharger Caddy et restaurer la sauvegarde.

## Lancer le workflow

Dans GitHub :

1. Aller dans `Actions`.
2. Choisir `Deploy preproduction`.
3. Cliquer sur `Run workflow`.
4. Choisir la branche a deployer.
5. Lancer manuellement.

Le workflow :

- prepare une cle SSH temporaire sur le runner ;
- ajoute le VPS a `known_hosts` avec `ssh-keyscan` sur le port `2222` ;
- teste la connexion SSH en `BatchMode` ;
- cree `/opt/pixelprowlers` si necessaire ;
- synchronise le depot par `rsync`;
- exclut `.env`, caches, builds, screenshots, SQLite, pycache et cles ;
- conserve le `.env` distant ;
- lance `docker compose up -d --build postgres django nuxt nginx` ;
- verifie Django, migrations, Caddy et HTTPS public.

## Verifications manuelles apres deploiement

Depuis le VPS :

```bash
cd /opt/pixelprowlers
docker compose ps
docker compose logs --tail=120 django
docker compose logs --tail=120 nginx
curl -fsS http://127.0.0.1:8080/health/
systemctl status caddy --no-pager
journalctl -u caddy -n 120 --no-pager
curl -I https://pixelprowlers.io
curl -I https://www.pixelprowlers.io
curl -i https://pixelprowlers.io/health/
```

Tester le formulaire `/contact` depuis le navigateur et confirmer la reception email.

## Rollback

Option simple :

1. Revenir au commit precedent dans Git.
2. Relancer le workflow sur la branche ou le tag stable.

Option manuelle si le workflow a casse le rendu mais Docker fonctionne :

```bash
cd /opt/pixelprowlers
docker compose ps
docker compose logs --tail=120
```

Puis redeployer un commit stable via GitHub Actions.

Ne jamais executer :

```bash
docker compose down -v
```

Cette commande supprimerait les volumes, dont PostgreSQL.

## Backup PostgreSQL manuel

Depuis le VPS :

```bash
mkdir -p ~/backups/pixelprowlers
cd /opt/pixelprowlers
docker compose exec -T postgres pg_dump -U pixelprowlers pixelprowlers > ~/backups/pixelprowlers/backup-$(date +%F-%H%M).sql
ls -lh ~/backups/pixelprowlers/
```

Le backup doit rester hors du depot Git.

## Points a valider avant production

- DNS `pixelprowlers.io` et `www.pixelprowlers.io` vers le VPS.
- HTTPS Caddy valide, sans boucle.
- SMTP reel fonctionnel.
- `/health/` public OK.
- Formulaire `/contact` OK et email recu.
- Logs sans secrets ni messages complets.
- Rate limit base sur la vraie IP client.
- Backup PostgreSQL cree et restauration testee sur environnement separe.
