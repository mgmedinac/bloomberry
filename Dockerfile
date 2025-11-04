# ===============================
# BloomBerry - Dockerfile Final con Imágenes
# ===============================

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código (incluyendo static y media)
COPY . .

# Crear carpetas necesarias
RUN mkdir -p /app/staticfiles /app/media

# Exponer puerto
EXPOSE 8000

# Ejecutar migraciones, cargar datos, recolectar archivos estáticos y correr Gunicorn
CMD python manage.py migrate && \
    python manage.py loaddata fixtures/seed_data.json && \
    python manage.py collectstatic --noinput && \
    gunicorn --bind 0.0.0.0:$PORT bloomberry.wsgi:application
