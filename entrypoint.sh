#!/usr/bin/env sh

# Exit on error
set -eux

echo "Setting up database directory..."
mkdir -p db
chmod -R a+rwX db

echo "Restoring database from Litestream if available..."
litestream restore -config litestream.yml -if-db-not-exists -if-replica-exists db/site.sqlite3

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Litestream with application..."
exec litestream replicate -config litestream.yml -exec "gunicorn mysite.wsgi:application --bind=0.0.0.0:80 --workers=3"
