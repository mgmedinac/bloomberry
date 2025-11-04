# Autor: Salome Serna
# Proyecto: BloomBerry
# Archivo: products/admin.py
# Descripción: Configuración de modelos en el panel de administración.

from django.contrib import admin
from .models import Product, Category, Review, Wishlist

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "description")
    list_editable = ("category", "price", "stock")
    autocomplete_fields = ("category",)
    readonly_fields = ("quantity_of_reviews", "created_at")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at", "product")
    search_fields = ("product__name", "user__username", "comment")

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "created_at")
    search_fields = ("user__username", "name")
    filter_horizontal = ("products",)
