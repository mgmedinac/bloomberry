#!/usr/bin/env bash
set -e

python manage.py migrate
python manage.py compilemessages || true

# Inicia el servidor de desarrollo con autoreload
exec python manage.py runserver 0.0.0.0:8000
