#!/usr/bin/env bash
set -euo pipefail
umask 077
: "${RESTORE_CONTAINER:?}"
: "${RESTORE_EXPECTED_ID:?}"
: "${DUMP_DIRECTORY:?}"
# This script is intentionally unusable against the production service.
[[ "$RESTORE_CONTAINER" = pixelprowlers-security-restore-* ]] || exit 2
[[ "$(docker inspect -f '{{.Id}}' "$RESTORE_CONTAINER")" = "$RESTORE_EXPECTED_ID" ]] || exit 2
(cd "$DUMP_DIRECTORY" && sha256sum -c SHA256SUMS)
docker exec "$RESTORE_CONTAINER" sh -ec 'test "$POSTGRES_DB" = qualification_only; test "$(psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc "select count(*) from information_schema.tables where table_schema=current_schema()")" = 0'
docker exec -i "$RESTORE_CONTAINER" sh -ec 'exec pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --no-acl --exit-on-error --single-transaction' < "$DUMP_DIRECTORY/database.dump"
