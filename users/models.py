# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: users/models.py
# Descripción: Modelo de perfil para usuarios (CustomerAccount).

from django.contrib.auth.models import User
from django.db import models

class CustomerAccount(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer_account'
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=80, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Customer Account"
        verbose_name_plural = "Customer Accounts"

    def __str__(self):
        return f"CustomerAccount({self.user.username})"
