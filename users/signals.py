# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: users/signals.py
# Descripción: Crea/asegura CustomerAccount al crear User.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerAccount

@receiver(post_save, sender=User)
def create_or_update_customer_account(sender, instance, created, **kwargs):
    if created:
        CustomerAccount.objects.create(user=instance)
    else:
        CustomerAccount.objects.get_or_create(user=instance)
