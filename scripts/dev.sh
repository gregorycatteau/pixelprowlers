#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
PYTHON_BIN="$BACKEND_DIR/.venv/bin/python"
BACKEND_HOST="${BACKEND_HOST:-127.0.0.1}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_HOST="${FRONTEND_HOST:-localhost}"
FRONTEND_PORT="${FRONTEND_PORT:-3000}"
POSTGRES_HOST_LOCAL="${POSTGRES_HOST_LOCAL:-127.0.0.1}"
POSTGRES_PORT_LOCAL="${POSTGRES_PORT_LOCAL:-5433}"
BACKEND_URL="http://${BACKEND_HOST}:${BACKEND_PORT}"
FRONTEND_URL="http://${FRONTEND_HOST}:${FRONTEND_PORT}"
HEALTH_URL="${BACKEND_URL}/health/"
GRAPHQL_URL="${BACKEND_URL}/graphql/"
BACKEND_PID=""
FRONTEND_PID=""

info() {
  printf '%s\n' "$*"
}

fail() {
  printf 'Erreur: %s\n' "$*" >&2
  exit 1
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

port_is_busy() {
  ss -ltn "sport = :$1" | tail -n +2 | grep -q .
}

wait_http() {
  local url="$1"
  local label="$2"
  local attempts="${3:-60}"

  for _ in $(seq 1 "$attempts"); do
    if "$PYTHON_BIN" - "$url" >/dev/null 2>&1 <<'PY'
import sys
from urllib.request import urlopen

with urlopen(sys.argv[1], timeout=1.5) as response:
    if 200 <= response.status < 500:
        raise SystemExit(0)
raise SystemExit(1)
PY
    then
      return 0
    fi

    if [[ -n "$BACKEND_PID" ]] && ! kill -0 "$BACKEND_PID" 2>/dev/null; then
      fail "$label s'est arrêté pendant le démarrage."
    fi

    if [[ -n "$FRONTEND_PID" ]] && ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
      fail "$label s'est arrêté pendant le démarrage."
    fi

    sleep 0.5
  done

  fail "$label ne répond pas sur $url."
}

cleanup() {
  local exit_code=$?

  trap - INT TERM EXIT

  if [[ -n "$FRONTEND_PID" ]] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
    kill "$FRONTEND_PID" 2>/dev/null || true
  fi

  if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi

  wait "$FRONTEND_PID" 2>/dev/null || true
  wait "$BACKEND_PID" 2>/dev/null || true

  exit "$exit_code"
}

start_existing_postgres_container() {
  if ! command_exists docker; then
    return 0
  fi

  if ! docker container inspect pixelprowlers-postgres >/dev/null 2>&1; then
    return 0
  fi

  local running
  running="$(docker inspect -f '{{.State.Running}}' pixelprowlers-postgres)"
  if [[ "$running" != "true" ]]; then
    info "Démarrage du conteneur PostgreSQL local existant: pixelprowlers-postgres"
    docker start pixelprowlers-postgres >/dev/null
  fi
}

trap cleanup INT TERM EXIT

cd "$ROOT_DIR"

info "PixelProwlers — environnement local"

[[ -d "$BACKEND_DIR" ]] || fail "dossier backend introuvable: $BACKEND_DIR"
[[ -d "$ROOT_DIR/app" ]] || fail "dossier frontend Nuxt introuvable: $ROOT_DIR/app"
[[ -x "$PYTHON_BIN" ]] || fail "virtualenv backend introuvable. Attendu: $PYTHON_BIN"
[[ -f "$ROOT_DIR/package.json" ]] || fail "package.json introuvable à la racine."
[[ -d "$ROOT_DIR/node_modules" ]] || fail "dépendances frontend absentes. Lancez: npm install"
[[ -f "$ROOT_DIR/.env" ]] || info "Avertissement: .env absent à la racine. Django utilisera ses valeurs par défaut et les exports locaux du script."

command_exists node || fail "Node.js est introuvable."
command_exists npm || fail "npm est introuvable."
command_exists ss || fail "ss est introuvable; impossible de vérifier les ports."

"$PYTHON_BIN" -c 'import django' >/dev/null 2>&1 || fail "Django n'est pas installé dans backend/.venv."

if port_is_busy "$BACKEND_PORT"; then
  fail "le port backend $BACKEND_PORT est déjà occupé."
fi

if port_is_busy "$FRONTEND_PORT"; then
  fail "le port frontend $FRONTEND_PORT est déjà occupé."
fi

start_existing_postgres_container

export POSTGRES_HOST="$POSTGRES_HOST_LOCAL"
export POSTGRES_PORT="$POSTGRES_PORT_LOCAL"
export DJANGO_DEBUG="true"
export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS:-127.0.0.1,localhost}"
export CORS_ALLOWED_ORIGINS="${CORS_ALLOWED_ORIGINS:-http://localhost:${FRONTEND_PORT},http://127.0.0.1:${FRONTEND_PORT}}"
export DJANGO_CSRF_TRUSTED_ORIGINS="${DJANGO_CSRF_TRUSTED_ORIGINS:-http://localhost:${FRONTEND_PORT},http://127.0.0.1:${FRONTEND_PORT}}"
export DJANGO_SECURE_SSL_REDIRECT="false"
export DJANGO_SESSION_COOKIE_SECURE="false"
export DJANGO_CSRF_COOKIE_SECURE="false"
export DJANGO_SECURE_HSTS_SECONDS="0"
export DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS="false"
export DJANGO_SECURE_HSTS_PRELOAD="false"
export EMAIL_BACKEND="${EMAIL_BACKEND:-django.core.mail.backends.console.EmailBackend}"
export NUXT_PUBLIC_API_BASE_URL="${NUXT_PUBLIC_API_BASE_URL:-$BACKEND_URL}"
export NUXT_PUBLIC_GRAPHQL_API_URL="${NUXT_PUBLIC_GRAPHQL_API_URL:-$GRAPHQL_URL}"
export GRAPHQL_API_URL="${GRAPHQL_API_URL:-$GRAPHQL_URL}"

info "Vérification Django..."
"$PYTHON_BIN" "$BACKEND_DIR/manage.py" check >/dev/null
"$PYTHON_BIN" "$BACKEND_DIR/manage.py" migrate --check >/dev/null

info "Backend Django : $BACKEND_URL"
info "Frontend Nuxt  : $FRONTEND_URL"
info "Health backend : $HEALTH_URL"

"$PYTHON_BIN" "$BACKEND_DIR/manage.py" runserver "${BACKEND_HOST}:${BACKEND_PORT}" \
  > >(sed -u 's/^/[django] /') 2>&1 &
BACKEND_PID=$!

wait_http "$HEALTH_URL" "Django" 80

npm run dev -- --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" \
  > >(sed -u 's/^/[nuxt] /') 2>&1 &
FRONTEND_PID=$!

wait_http "$FRONTEND_URL" "Nuxt" 80

info ""
info "Frontend et backend sont prêts."
info "Ctrl+C arrêtera l’ensemble des services."

wait -n "$BACKEND_PID" "$FRONTEND_PID"
fail "un service s'est arrêté."
