# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: products/urls.py
# Descripción: Rutas de la app products.

from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home_view, name='home'),
]
