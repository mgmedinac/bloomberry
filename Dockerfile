# ===============================
# BloomBerry - Dockerfile Final
# ===============================

FROM python:3.11-slim

# Evita problemas de buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Exponer el puerto usado por Django
EXPOSE 8000

# Ejecutar migraciones, cargar fixtures y arrancar el servidor con Gunicorn
CMD python manage.py migrate && \
    python manage.py loaddata fixtures/seed_categories.json && \
    python manage.py loaddata fixtures/seed_products.json && \
    python manage.py loaddata fixtures/seed_data.json && \
    gunicorn --bind 0.0.0.0:$PORT bloomberry.wsgi:application
