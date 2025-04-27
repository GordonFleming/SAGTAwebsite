#!/usr/bin/env sh

# Exit on error
set -e

cron

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput
# Add the cron jobs
python manage.py crontab add

# Execute the main command
exec "$@"
