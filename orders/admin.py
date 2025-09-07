# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: orders/admin.py
# Descripción: Configuración de modelos en el panel de administración para órdenes.

from django.contrib import admin
from .models import ShoppingCart, OrderInfo, OrderItem


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "created_at")
    search_fields = ("user__username", "product__name")
    list_filter = ("created_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total", "status", "created_at")
    search_fields = ("user__username", "status")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]
