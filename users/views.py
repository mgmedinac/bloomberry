# Create your views here.
# Autor: 
# Proyecto: BloomBerry
# Archivo: users/views.py
# Descripción: Vistas simples para sección pública.

from django.shortcuts import render

def home_view(request):
    """
    Muestra la página principal de users.
    Regla: la vista es simple; la lógica pesada va a helpers o modelos.
    """
    return render(request, 'users/home.html')
