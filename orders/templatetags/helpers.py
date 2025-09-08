# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: orders/templatetags/helpers.py
# Descripción: Filtros personalizados para plantillas de la app orders.


from django import template

register = template.Library()

def mul(value, arg):
    """Multiplica el valor por el argumento."""
    return value * arg
mul.is_safe = True

register.filter('mul', mul)
