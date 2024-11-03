#!/usr/bin/env sh

# Exit on error
set -e

# Ensure the static and media directories are writable
chown -R wagtail:wagtail /usr/src/app/static
chown -R wagtail:wagtail /usr/src/app/media

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Execute the main command
exec "$@"
