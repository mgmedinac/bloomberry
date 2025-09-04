# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: users/admin.py
# Descripción: Registro de CustomerAccount en admin.

from django.contrib import admin
from .models import CustomerAccount

@admin.register(CustomerAccount)
class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'created_at')
    search_fields = ('user__username', 'phone', 'city')
