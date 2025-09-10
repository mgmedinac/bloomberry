# 🌸 BloomBerry – E-commerce Django Project

##  Descripción
BloomBerry es una aplicación web de comercio electrónico desarrollada en **Django**, como proyecto académico de **Tópicos Especiales en Ingeniería de Software**.  
Permite a los usuarios navegar productos, gestionar un carrito de compras, realizar pedidos, consultar historial de órdenes y descargar facturas en PDF.  
Además, incluye integración con un **chatbot de IA** que responde a comandos definidos y funcionalidades de internacionalización (i18n).

---

##  Integrantes
- Maria Clara Medina Gómez  
- Salomé Serna  

---

##  Funcionalidades principales
- **Catálogo de productos** con búsqueda y wishlist.  
- **Carrito de compras** persistente por usuario.  
- **Checkout y gestión de órdenes**.  
- **Historial de compras** con descarga de **factura PDF**.  
- **Autenticación de usuarios** (registro, login, perfil).  
- **Perfil de usuario** editable.  
- **Traducciones i18n** (Español / Inglés) con ficheros `.po`/`.mo`.  
- **Chatbot de IA** conectado a API externa.  

---

## 🗂️ Estructura del proyecto

BLOOMBERRYPROJECT/
├── bloomberry/ # Configuración principal Django

├── chat/ # Chatbot con integración a API de IA

├── orders/ # Órdenes, historial, facturas PDF

├── payments/ # Pasarela de pagos (simulada)

├── products/ # Productos, búsqueda, wishlist

├── users/ # Autenticación y perfiles

├── fixtures/ # Datos iniciales en JSON (productos, usuarios, etc.)

├── static/ # Archivos estáticos (CSS, imágenes, JS)

├── templates/ # Templates globales y de apps

├── resources/lang/ # Archivos de traducción (.po / .mo)

├── manage.py

└── requirements.txt



---


##  Instalación y configuración

### 1) Clonar el repositorio

git clone https://github.com/mgmedinac/bloomberry.git
cd bloomberry

## 2) Crear y activar entorno virtual
python3 -m venv env
source env/bin/activate   # en Mac/Linux
env\Scripts\activate      # en Windows

## 3) Instalar dependencias
pip install -r requirements.txt

## 4) Base de datos
La base de datos no se incluye (db.sqlite3 está en .gitignore).
Se debe cargar desde los fixtures JSON:
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json


## 5) Chatbot de IA
El chatbot se encuentra en la app chat/.
Para activarlo:
Configura la variable de entorno con tu API Key (por ejemplo, en .env):
OPENAI_API_KEY=tu_api_key_aqui
Inicia el servidor y accede al chat en la sección correspondiente.
Los comandos soportados se encuentran documentados en chat/views.py y en la Wiki del repo.


## 6)  Internacionalización
Idiomas disponibles: Español (default), Inglés.
Traducciones en resources/lang/.
Para compilar mensajes:
django-admin makemessages -l en
django-admin makemessages -l es
django-admin compilemessages

## 7) Ejecución
python manage.py runserver
Accede en tu navegador a: http://localhost:8000

