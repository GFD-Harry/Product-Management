#!/bin/bash

set -e

PROJECT="product-management-restore"
DB_NAME="product_management_restore"

echo "==> Starting PostgreSQL..."

docker compose -p "$PROJECT" --env-file .env \
  -f compose.yaml -f compose.dev.yaml up -d db

echo "==> Waiting for PostgreSQL..."

until docker compose -p "$PROJECT" --env-file .env \
  -f compose.yaml -f compose.dev.yaml exec -T db \
  pg_isready -U "${POSTGRES_USER:-odoo}" >/dev/null 2>&1
do
  sleep 2
done

echo "==> Creating restore database..."

docker compose -p "$PROJECT" --env-file .env \
  -f compose.yaml -f compose.dev.yaml run --rm odoo \
  -d "$DB_NAME" \
  --stop-after-init --no-http

echo "==> Starting Odoo..."

docker compose -p "$PROJECT" --env-file .env \
  -f compose.yaml -f compose.dev.yaml up -d odoo

echo "==> Restore environment ready."