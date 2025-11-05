#!/bin/bash
set -e

echo "🚀 Aplicando migraciones..."
python manage.py migrate --noinput

echo "📦 Recolectando estáticos..."
python manage.py collectstatic --noinput

echo "🧪 Cargando fixtures si está vacío..."
python - <<'PY'
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bloomberry.settings")
django.setup()
from products.models import Category
from django.core.management import call_command

if Category.objects.count() == 0:
    print("→ Sin categorías: cargando fixtures…")
    try:
        call_command("loaddata", "fixtures/seed_categories.json", verbosity=1)
    except Exception as e:
        print("WARN: no se pudo seed_categories:", e)
    try:
        call_command("loaddata", "fixtures/seed_data.json", verbosity=1)
    except Exception as e:
        print("WARN: no se pudo seed_data:", e)
else:
    print("→ Ya había datos, no se cargan fixtures.")
PY

echo "✅ Iniciando Gunicorn…"
exec gunicorn bloomberry.wsgi:application --bind 0.0.0.0:${PORT}
