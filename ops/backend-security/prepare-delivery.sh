#!/usr/bin/env bash
# LOCAL ONLY: generate reviewable backend-only overrides. Does not contact production.
set -euo pipefail
umask 077
: "${CORRECTED_IMAGE_ID:?Use the tested immutable sha256 image ID}"
: "${DELIVERY_DIRECTORY:?New absolute output directory required}"
[[ "$CORRECTED_IMAGE_ID" =~ ^sha256:[0-9a-f]{64}$ ]] || exit 2
[[ "$DELIVERY_DIRECTORY" = /* ]] || exit 2
mkdir -m 700 "$DELIVERY_DIRECTORY"
for spec in "delivery:$CORRECTED_IMAGE_ID" "rollback:sha256:1fd7de0d2b3028177417e877683cced740ac40955ec1ce25aba93027e671d139"; do
  name="${spec%%:*}"
  image="${spec#*:}"
  cat > "$DELIVERY_DIRECTORY/$name.yml" <<EOF
services:
  django:
    image: $image
    pull_policy: never
    command: ["gunicorn", "pixelprowlers.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
EOF
done
# Keeping a gunicorn-only command in rollback also avoids unnecessary migrations.
printf '%s\n' "$DELIVERY_DIRECTORY"
