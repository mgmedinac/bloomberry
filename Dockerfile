# ===============================
# BloomBerry - Dockerfile Final
# ===============================

# Imagen base ligera con Python
FROM python:3.11-slim

# Evitar buffer de salida y escritura de bytecode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar y usar Django + Gunicorn
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto donde correrá Django
EXPOSE 8000

# Ejecutar migraciones y luego lanzar Gunicorn
CMD python manage.py migrate && exec gunicorn --bind 0.0.0.0:$PORT bloomberry.wsgi:application
