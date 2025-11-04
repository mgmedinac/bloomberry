# ===============================
# BloomBerry - Dockerfile Final
# ===============================

# Imagen base ligera con Python
FROM python:3.11-slim

# Evitar buffer de salida
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    gettext \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Compilar archivos de traducción (.po → .mo)
RUN django-admin compilemessages -l es -l en

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Aplicar migraciones
RUN python manage.py migrate --noinput

# Cargar fixtures JSON (ajusta los nombres si son diferentes)
RUN python manage.py loaddata fixtures/seed_data.json || true

# Exponer el puerto de Django
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bloomberry.wsgi:application"]
