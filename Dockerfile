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
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requerimientos
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Exponer el puerto donde corre Django
EXPOSE 8000

# Comando de arranque: migrar, cargar datos y correr el servidor
#CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "bloomberry.wsgi:application"]

# --- al final del Dockerfile ---
CMD sh -c "gunicorn bloomberry.wsgi:application --bind 0.0.0.0:${PORT}"
