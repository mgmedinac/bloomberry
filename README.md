🌸 BloomBerry
BloomBerry es una aplicación web desarrollada con Django 4 y SQLite3 que permite la gestión de productos, clientes, pedidos y pagos.
Cuenta con un sistema de login, carrito de compras y un chatbot con IA para recomendaciones.

 Instalación y ejecución
1. Clonar el repositorio
git clone https://github.com/tu-usuario/bloomberry.git
cd bloomberry

2. Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Instalar dependencias
pip install -r requirements.txt

4. Ejecutar migraciones
python manage.py migrate

5. Crear superusuario (admin)
python manage.py createsuperuser

6. Ejecutar el servidor
python manage.py runserver
Luego abre en tu navegador:
http://127.0.0.1:8000/

7. Roles y secciones
Usuario final (/): puede ver productos, agregar al carrito, hacer compras, usar el chatbot.
Administrador (/admin/): gestiona productos, usuarios, pedidos y pagos.

8. Funcionalidades interesantes
   
Además de las operaciones CRUD básicas, la aplicación incluye:

🔍 Búsqueda de productos por nombre.

🛒 Ver el Top 3 productos más vendidos.

📄 Generar factura de venta en PDF.

⭐ Ver el Top 4 productos más comentados.


10. Estructura del proyecto
bloomberry/

│── bloomberry/       # Configuración principal del proyecto

│── users/            # Gestión de usuarios y login

│── products/         # Productos, reseñas y wishlist

│── orders/           # Pedidos y carrito de compras

│── payments/         # Pagos

│── chat/             # Chat y recomendaciones IA

│── static/           # Archivos estáticos (CSS, JS, imágenes)

│── templates/        # Plantillas HTML

│── db.sqlite3        # Base de datos

│── manage.py

│── requirements.txt

│── README.md

11. Tecnologías usadas
Django 4
SQLite3
HTML, CSS, Bootstrap
Python 3.x

12. Equipo
Arquitecta: Maria Clara Medina Gomez
Desarrolladora: Salome Serna Restrepo
