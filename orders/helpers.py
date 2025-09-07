# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: orders/helpers.py
# Descripción: Funciones auxiliares para cálculos y lógica de órdenes.

from decimal import Decimal
from .models import ShoppingCart

def calcular_total(user):
    """Calcula el total del carrito de un usuario"""
    items = ShoppingCart.objects.filter(user=user)
    total = sum(item.product.price * item.quantity for item in items)
    return Decimal(total)


def add_to_cart(user, product, quantity=1):
    """
    Añade un producto al carrito del usuario.
    Si el producto ya está en el carrito, incrementa la cantidad.
    """
    item, created = ShoppingCart.objects.get_or_create(
        user=user,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        item.quantity += quantity
        item.save()
    return item

