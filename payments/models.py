# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: payments/models.py
# Descripción: Modelos para la app de pagos.


from django.db import models
from django.contrib.auth.models import User
from orders.models import OrderInfo
from decimal import Decimal

# Create your models here.
class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(OrderInfo, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id} - {self.user.username} - {self.status}"
