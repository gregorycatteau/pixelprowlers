# PixelProwlers Backend

Target runtime:

- Python 3.13
- Django 6.0.6
- PostgreSQL 18.4

Local database:

```bash
docker compose up -d postgres
```

Install backend dependencies in an isolated environment:

```bash
cd backend
python3.13 -m venv .venv
. .venv/bin/activate
pip install -e .
```
