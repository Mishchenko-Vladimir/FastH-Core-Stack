#!/usr/bin/env bash

set -e

echo "Run apply migrations.."
uv run alembic upgrade head

echo "Check/Create superuser.."
uv run python -m actions.create_superuser

echo "Migrations applied!"
exec "$@"
