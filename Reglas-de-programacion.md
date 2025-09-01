Reglas para rutas
Toda ruta debe estar asociada a un View.
No se permiten rutas sueltas sin uso.

Reglas para vistas
Toda vista debe extender de base.html.
Usar include cuando se repita código.

Reglas para modelos
Cada modelo debe tener un método __str__.
Después de cada cambio en los modelos se debe ejecutar makemigrations y migrate.

Reglas para controladores (views.py)
Cada vista debe tener un propósito claro.
Evitar lógica complicada en la vista: delegar en modelos o helpers.

Reglas para templates
Todos los templates deben ser .html.
Respetar los colores e identidad visual de Bloom Berry.