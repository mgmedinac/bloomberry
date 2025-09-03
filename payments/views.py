# Create your views here.
# Autor: 
# Proyecto: BloomBerry
# Archivo: payments/views.py
# Descripción: Vistas simples para sección pública.

from django.shortcuts import render
from django.utils.translation import gettext as _



def payments_home_view(request):
    return render(request, 'payments/home.html')
