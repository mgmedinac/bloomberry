# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: chat/urls.py
# Descripción: Rutas de la app chat.

from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_page, name="page"),
    path("send/", views.send_message, name="send_message"),
]
