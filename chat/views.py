# Create your views here.
# Autor: 
# Proyecto: BloomBerry
# Archivo: chat/views.py
# Descripción: Vistas simples para sección pública.

from django.shortcuts import render
from django.utils.translation import gettext as _

from django.shortcuts import render

def chat_home_view(request):
    return render(request, 'chat/home.html')
