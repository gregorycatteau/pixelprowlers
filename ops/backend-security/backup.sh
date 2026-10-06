#!/usr/bin/env bash
set -euo pipefail
umask 077
: "${PG_CONTAINER:?Explicit target container required}"
: "${EXPECTED_PG_ID:?Explicit verified container ID required}"
: "${EXPECTED_DATABASE:?Identify the application database before export}"
: "${BACKUP_ROOT:?Protected absolute backup directory required}"
[[ "$BACKUP_ROOT" = /* && "$BACKUP_ROOT" != / ]] || exit 2
[[ "$(docker inspect -f '{{.Id}}' "$PG_CONTAINER")" = "$EXPECTED_PG_ID" ]] || { echo 'Container identity mismatch' >&2; exit 2; }
# Compare internally; neither credential values nor records are printed.
docker exec -e EXPECTED_DATABASE="$EXPECTED_DATABASE" "$PG_CONTAINER" sh -ec 'test "$POSTGRES_DB" = "$EXPECTED_DATABASE"'
mkdir -p "$BACKUP_ROOT"
[[ "$(stat -c %a "$BACKUP_ROOT")" = 700 ]] || { echo 'Backup root must be mode 700' >&2; exit 2; }
target="$BACKUP_ROOT/$(date -u +%Y%m%dT%H%M%SZ)-backend-security"
mkdir -m 700 "$target"
# pg_dump obtains a coherent MVCC snapshot; no table contents in stdout of this script.
docker exec "$PG_CONTAINER" sh -ec 'exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc --no-owner --no-acl' > "$target/database.dump"
test -s "$target/database.dump"
docker exec -i "$PG_CONTAINER" pg_restore --list < "$target/database.dump" > "$target/archive-list.txt"
(cd "$target" && sha256sum database.dump > SHA256SUMS && sha256sum -c SHA256SUMS)
docker inspect -f '{{.Id}} {{.Image}}' "$PG_CONTAINER" > "$target/postgres-image.txt"
printf '%s\n' "$target"
# Retain every pre-delivery copy through acceptance, then 7 daily / 4 weekly / 6 monthly.
# No automatic deletion here. An operator must review the retention job separately.
