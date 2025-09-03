# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: users/urls.py
# Descripción: Rutas de la app users.

from django.urls import path
from . import views
from django.utils.translation import gettext as _

app_name = 'users'

urlpatterns = [
    path('', views.home_view, name='home'),
]
