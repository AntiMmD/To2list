#!/bin/sh
set -e

mkdir -p /app/data

python manage.py makemigrations user task --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn 2doList.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 60
