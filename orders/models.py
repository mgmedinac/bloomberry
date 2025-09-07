# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: orders/models.py
# Descripción: Modelos para gestionar carritos de compra y órdenes.

from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class ShoppingCart(models.Model):
    """Modelo para representar un carrito de compras de un usuario"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shopping_cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.user.username} - {self.product.name} ({self.quantity})"


class OrderInfo(models.Model):
    """Modelo para representar una orden finalizada"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, through="OrderItem")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pendiente"),
            ("paid", "Pagada"),
            ("shipped", "Enviada"),
            ("completed", "Completada"),
            ("cancelled", "Cancelada"),
        ],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden {self.id} de {self.user.username} - {self.status}"


class OrderItem(models.Model):
    """Relación intermedia entre OrderInfo y Product para guardar cantidades"""
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Orden {self.order.id})"
