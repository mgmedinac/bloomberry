# ===============================
# BloomBerry - Dockerfile Final con imágenes funcionando en Cloud Run
# ===============================

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto completo (incluyendo media)
COPY . .

# Crear carpetas si no existen
RUN mkdir -p /app/staticfiles /app/media

# Recolectar estáticos y cargar datos
RUN python manage.py collectstatic --noinput

# Ejecutar migraciones y cargar fixtures en el arranque
CMD python manage.py migrate && \
    python manage.py loaddata fixtures/seed_data.json && \
    gunicorn --bind 0.0.0.0:$PORT bloomberry.wsgi:application

EXPOSE 8000
