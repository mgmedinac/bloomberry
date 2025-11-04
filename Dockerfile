# Dockerfile
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Para compilar traducciones (.po -> .mo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt && pip check || true

# Copiar todo el proyecto
COPY . /app

# Variables por defecto (se pueden sobrescribir en compose)
ENV DJANGO_SETTINGS_MODULE=bloomberry.settings \
    DEBUG=0 \
    ALLOWED_HOSTS="*" \
    PORT=8000

# Compilar traducciones y recopilar estáticos dentro de la imagen
RUN python manage.py compilemessages || true
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
