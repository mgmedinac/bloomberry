# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: payments/urls.py
# Descripción: Rutas de la app payments.

from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [
    path('', views.payments_home_view, name='home'),
]
