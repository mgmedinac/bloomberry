# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: chat/urls.py
# Descripción: Rutas de la app chat.

from django.urls import path
from . import views


app_name = 'chat'

urlpatterns = [
    path('', views.chat_home_view, name='home'),
]
