#!/bin/bash
# entrypoint.sh — ejecutar migraciones antes de arrancar Gunicorn

echo "🚀 Aplicando migraciones..."
python manage.py migrate --noinput

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Iniciando servidor Gunicorn..."
gunicorn bloomberry.wsgi:application --bind 0.0.0.0:${PORT}
