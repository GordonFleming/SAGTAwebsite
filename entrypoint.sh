#!/usr/bin/env sh

# Run migrate and collectstatic
./manage.py migrate --noinput
./manage.py collectstatic --noinput

exec "$@"
