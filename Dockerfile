# ============================
# BloomBerry - Dockerfile
# ============================

# 1️⃣ Imagen base
FROM python:3.11-slim

# 2️⃣ Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Crear directorio y copiar proyecto
WORKDIR /app
COPY . /app/

# 4️⃣ Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5️⃣ Exponer puerto (el que usa Django)
EXPOSE 8000

# 6️⃣ Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
