# Développement local

Commande principale depuis la racine du dépôt :

```bash
make dev
```

Par défaut, le frontend démarre sur `localhost:3000` et le backend sur `127.0.0.1:8000`. Pour un diagnostic ponctuel si un autre projet occupe déjà `3000`, le script accepte une surcharge locale :

```bash
FRONTEND_PORT=3006 ./scripts/dev.sh
```

## Prérequis

- Linux avec Bash.
- Node.js et npm.
- Python 3.13.
- Environnement virtuel backend dans `backend/.venv`.
- Dépendances frontend installées dans `node_modules`.
- PostgreSQL PixelProwlers accessible en local sur `127.0.0.1:5433`.

Le dépôt contient aussi `backend/venv`, mais la procédure locale utilise `backend/.venv`.

## Installation initiale

Créer le virtualenv backend si `backend/.venv` n’existe pas :

```bash
cd backend
python3.13 -m venv .venv
.venv/bin/pip install -e .
```

Installer les dépendances frontend depuis la racine :

```bash
npm install
```

## Variables d’environnement

Le fichier `.env` racine peut contenir la configuration Docker interne. Pour le développement lancé depuis l’hôte, `make dev` exporte explicitement :

```env
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
NUXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
NUXT_PUBLIC_GRAPHQL_API_URL=http://127.0.0.1:8000/graphql/
GRAPHQL_API_URL=http://127.0.0.1:8000/graphql/
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Les mots de passe, clés SMTP, tokens et secrets restent dans `.env` ou dans l’environnement local. Ne pas les commiter.
En local, `make dev` utilise le backend email console par défaut pour éviter les envois réels pendant les tests.

## Base de données

Le backend utilise PostgreSQL. En local, le conteneur attendu est `pixelprowlers-postgres`, exposé sur `127.0.0.1:5433`.

`make dev` démarre ce conteneur s’il existe déjà et qu’il est arrêté. Il ne supprime aucun volume et ne lance aucune commande destructive.

Si le conteneur n’existe pas, créer ou démarrer PostgreSQL selon la procédure Docker locale du projet, puis relancer :

```bash
make dev
```

## Démarrage

```bash
make dev
```

La commande :

- vérifie les dossiers `app/` et `backend/` ;
- vérifie `backend/.venv` ;
- vérifie Python, Django, Node, npm et `node_modules` ;
- vérifie que les ports `8000` et `3000` sont libres ;
- vérifie `manage.py check` et `migrate --check` ;
- lance Django avec `backend/.venv/bin/python` ;
- lance Nuxt ;
- attend que Django réponde sur `/health/` ;
- attend que Nuxt réponde ;
- préfixe les logs avec `[django]` et `[nuxt]`.

URLs locales :

```text
Backend Django : http://127.0.0.1:8000
Frontend Nuxt  : http://localhost:3000
Health backend : http://127.0.0.1:8000/health/
GraphQL        : http://127.0.0.1:8000/graphql/
```

## Arrêt

Un seul `Ctrl+C` arrête Nuxt et Django. Le script propage `SIGINT`/`SIGTERM`, attend l’arrêt des deux processus et évite de laisser des processus orphelins.

## Diagnostics courants

Port occupé :

```bash
ss -ltnp | grep ':3000\|:8000'
```

Backend Django :

```bash
POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=5433 backend/.venv/bin/python backend/manage.py check
POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=5433 backend/.venv/bin/python backend/manage.py migrate --check
```

Health backend :

```bash
python - <<'PY'
from urllib.request import urlopen
print(urlopen("http://127.0.0.1:8000/health/").read().decode())
PY
```

Si le formulaire affiche que le service d’audit est indisponible, vérifier que `make dev` est lancé et que `NUXT_PUBLIC_GRAPHQL_API_URL` pointe vers `http://127.0.0.1:8000/graphql/`.
