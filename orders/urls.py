# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: orders/urls.py
# Descripción: Rutas de la app orders.

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.orders_home_view, name='home'),
]
