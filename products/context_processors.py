# Autor: Salome Serna
# Proyecto: BloomBerry
# Archivo: products/context_processors.py
# Descripción: Devuelve categorías en el contexto global.

from .models import Category

def categories_processor(request):
    return {
        "categories": Category.objects.all()
    }
