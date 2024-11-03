#!/usr/bin/env sh

# Exit on error
set -e

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Execute the main command
exec "$@"
