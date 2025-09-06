# Autor: Salome Serna
# Proyecto: BloomBerry
# Archivo: products/signals.py
# Descripción: Señales para actualizar la cantidad de reseñas en productos.


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review, Product


@receiver(post_save, sender=Review)
def update_review_count_on_save(sender, instance, **kwargs):
    product = instance.product
    product.quantity_of_reviews = product.reviews.count()
    product.save(update_fields=["quantity_of_reviews"])


@receiver(post_delete, sender=Review)
def update_review_count_on_delete(sender, instance, **kwargs):
    product = instance.product
    product.quantity_of_reviews = product.reviews.count()
    product.save(update_fields=["quantity_of_reviews"])
