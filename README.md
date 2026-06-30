# Pixelprowlers

Structure applicative classique:

- `frontend/`: Nuxt 3, Vue, Tailwind CSS.
- `backend/`: Django, Django REST Framework, PostgreSQL.
- `docker-compose.yml`: PostgreSQL, Django, Nuxt et Nginx pour un lancement complet.
- `nginx.conf`: reverse proxy local vers le front et l'API.

Les exports `Hostinger _ Agents*` présents à la racine ont été laissés intacts et ne sont pas utilisés par la nouvelle structure.

## Prérequis

- Node.js 20 ou plus récent.
- Python 3.11 ou plus récent.
- Docker avec Docker Compose.

## Démarrage Docker

Vérifier que le `.env` racine existe:

```env
DEBUG=False
SECRET_KEY=django-insecure-change-this-in-production
DB_PASSWORD=pixelprowlers_local_password
ALLOWED_HOSTS=localhost,127.0.0.1
```

Valider la configuration Docker Compose:

```bash
docker compose config
```

Lancer les services:

```bash
docker compose up --build
```

Services exposés:

- Front Nuxt direct: `http://localhost:3000`
- API Django directe: `http://localhost:8001/api/`
- Admin Django direct: `http://localhost:8001/admin/`
- Reverse proxy Nginx: `http://localhost:8080`

Créer un super-utilisateur:

```bash
docker compose exec django python manage.py createsuperuser
```

## Base de données seule

Pour travailler avec les serveurs locaux hors Docker:

```bash
docker compose up -d postgres
```

La base locale par défaut est:

- base: `pixelprowlers`
- utilisateur: `pixelprowlers`
- mot de passe: `pixelprowlers`
- port Docker local: `5433`
- port interne Docker: `5432`

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Endpoints principaux:

- `POST /api/contacts/`
- `POST /api/leads/`
- `GET /api/formations/`
- `POST /api/registrations/`
- `GET /api/services/`
- `GET /admin/`

Les listes de contacts, leads et inscriptions sont réservées aux administrateurs Django.

## Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Le front attend l'API Django sur `NUXT_PUBLIC_API_URL`, avec `http://localhost:8001` dans Docker Compose.

Pages disponibles:

- `/`
- `/contact`
- `/developpement`
- `/materiel`
- `/formations`

## Variables d'environnement

Exemples disponibles:

- `backend/.env.example`
- `frontend/.env.example`

Ne pas committer les vrais fichiers `.env`.
