#!/usr/bin/env sh

# Exit on error
set -eu

echo "Setting up database directory..."
mkdir -p db
chmod -R a+rwX db

echo "Restoring database from Litestream if available..."
# Add error handling for restore
if litestream restore -config litestream.yml -if-db-not-exists -if-replica-exists db/site.sqlite3; then
    echo "Database restored successfully"
else
    echo "No replica found or database already exists, continuing..."
fi

# Cleanup potentially corrupted local state from previous runs
rm -f db/site.sqlite3-litestream

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Optional: Create a superuser if needed (using env vars)
# if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
#     python manage.py createsuperuser --noinput || true
# fi

echo "Starting Litestream with application..."
exec litestream replicate -config litestream.yml -exec "$@"