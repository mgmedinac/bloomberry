# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: products/views_api.py
# Descripción: Servicio JSON que provee la lista de productos disponibles.

from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from .models import Product

def product_list_api(request):
    products = Product.objects.all()
    data = []

    for product in products:
        image_url = (
            request.build_absolute_uri(product.image.url)
            if product.image else None
        )
        detail_url = request.build_absolute_uri(
            reverse('products:detail', args=[product.id])
        )

        data.append({
            "id": product.id,
            "nombre": product.name,
            "descripcion": product.description,
            "precio": float(product.price),
            "stock": product.stock,
            "imagen": image_url,
            "detalle_url": detail_url,
        })

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
