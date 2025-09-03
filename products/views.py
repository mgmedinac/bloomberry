# Create your views here.
# Autor: 
# Proyecto: BloomBerry
# Archivo: products/views.py
# Descripción: Vistas simples para sección pública.

from django.shortcuts import render
from django.utils.translation import gettext as _

def home_view(request):
    """
    Muestra la página principal de productos.
    Regla: la vista es simple; la lógica pesada va a helpers o modelos.
    """
    return render(request, 'products/home.html')
