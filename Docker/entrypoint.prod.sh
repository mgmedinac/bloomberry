#!/usr/bin/env bash
set -e

python manage.py migrate --noinput
python manage.py compilemessages || true
python manage.py collectstatic --noinput || true

# Inicia el servidor Gunicorn (modo producción)
exec gunicorn bloomberry.wsgi:application --bind 0.0.0.0:${PORT} --workers 3 --timeout 90
