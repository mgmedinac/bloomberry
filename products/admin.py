# Autor: Salome Serna
# Proyecto: BloomBerry
# Archivo: products/admin.py
# Descripción: Configuración de modelos en el panel de administración.

from django.contrib import admin
from .models import Product, Review, Wishlist


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'fabrication_date', 'quantity_of_reviews', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('fabrication_date', 'created_at')
    ordering = ('-created_at',)
    list_editable = ('price', 'stock')  


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'created_at')
    search_fields = ('user__username', 'name')
    filter_horizontal = ('products',) 
    ordering = ('-created_at',)
