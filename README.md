# 🌸 BloomBerry – E-commerce Django Project

## 📝 Descripción
**BloomBerry** es una aplicación web de comercio electrónico desarrollada en **Django**, como proyecto académico de **Tópicos Especiales en Ingeniería de Software**.

Permite a los usuarios navegar productos, gestionar un carrito de compras, realizar pedidos, consultar el historial de órdenes y descargar facturas en PDF.  
Incluye un **chatbot de IA**, soporte **multilenguaje (Español / Inglés)** mediante i18n, servicios JSON, consumo de APIs externas, aplicación del principio de **Inversión de Dependencias (DI)** y **despliegue en Google Cloud Run con Docker**.

---

## 👩‍💻 Integrantes
- **María Clara Medina Gómez** – Arquitecta principal (Entrega 1)
- **Salomé Serna** – Arquitecta (Entrega 2) 

---

## 🚀 Funcionalidades principales
- 🛍️ **Catálogo de productos** con búsqueda, wishlist y paginación.
- 🛒 **Carrito de compras** persistente por usuario.
- 💳 **Checkout y gestión de órdenes** con facturas PDF.
- 👤 **Autenticación y perfiles** de usuario editables.
- 🌎 **Internacionalización (i18n)** en Español / Inglés.
- 🧾 **Servicio JSON público** con información de productos.
- 🤝 **Consumo de servicio aliado** (productos del equipo anterior).
- 🌐 **Consumo de API externa** para conversión COP ⇄ USD.
- 🧩 **Inversión de dependencias (DI)** en el módulo de conversión de moneda.
- 🧪 **Pruebas unitarias** en productos y órdenes.
- 🐳 **Despliegue en Docker + Google Cloud Run**.

---

## 🗂️ Estructura del proyecto
```txt
BLOOMBERRYPROJECT/
├── bloomberry/               # Configuración principal Django
├── chat/                     # Chatbot con integración IA
├── orders/                   # Órdenes, historial, facturas PDF
├── payments/                 # Pasarela de pagos simulada
├── products/                 # Productos, API JSON
├── users/                    # Autenticación y perfiles
├── core/services/            # Inversión de dependencias (CurrencyConverter)
├── fixtures/                 # Datos iniciales en JSON
├── static/                   # Archivos estáticos (CSS, imágenes, JS)
├── templates/                # Templates globales
├── resources/lang/           # Traducciones (.po / .mo)
├── Dockerfile
├── netlify.toml
└── manage.py
```

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



### 🌸 Servicio JSON - Productos BloomBerry
**Endpoint:** `/products/api/`  
**Método:** `GET`  
**Descripción:** Retorna la lista de productos disponibles con su nombre, descripción, precio, stock, imagen y enlace de detalle.  
**Ejemplo de respuesta:**
```json
[ {"id": 2, "nombre": "Kit aromático", 
    "descripcion": "Este kit incluye aceite esencial de árbol de té, aceite de romero, y aceite esencial relajante de lavanda y un jabón liquido con esencia de romero", 
    "precio": 80000.0, 
    "stock": 5, 
    "imagen": "http://127.0.0.1:8000/media/products/IMG-20250905-WA0054.jpg", 
    "detalle_url": "http://127.0.0.1:8000/2/"}]
