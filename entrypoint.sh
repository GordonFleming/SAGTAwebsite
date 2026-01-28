#!/usr/bin/env sh

# Exit on error
set -eu

echo "Setting up database directory..."
mkdir -p db
chmod -R a+rwX db

echo "Restoring database from Litestream if available..."
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

echo "Starting Litestream with application..."
# Pass all CMD arguments to litestream -exec
exec litestream replicate -config litestream.yml -exec "$*"