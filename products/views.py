# Autor: Salome Serna
# Proyecto: BloomBerry
# Archivo: products/views.py
# Descripción: Vistas para listar y detallar productos.


from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from .models import Product

def home_view(request):
    """Muestra productos destacados en la página principal"""
    featured_products = Product.objects.all()[:4]  # los primeros 4
    return render(request, "products/home.html", {"featured_products": featured_products})


def product_list(request):
    """Vista para listar todos los productos"""
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, product_id):
    """Vista para mostrar detalle de un producto"""
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})
