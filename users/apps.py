# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: users/apps.py
# Descripción: Config de la app users (carga de señales).

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Cargar señales para crear/asegurar CustomerAccount al crear User
        from . import signals  # noqa: F401
