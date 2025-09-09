# Autor: Salome Serna
# Proyecto: BloomBerry
# Archivo: products/models.py
# Descripción: Modelos para productos, categorias, reseñas y listas de deseos.

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse  



class Category(models.Model):
    """Categorías para organizar los productos"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name



class Product(models.Model):
    """Modelo para los productos ecológicos de la tienda"""
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    fabrication_date = models.DateField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    quantity_of_reviews = models.PositiveIntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """
        Devuelve la URL de detalle del producto.
        Si tu ruta es path("<int:pk>/", views.product_detail, name="product_detail"),
        esto generará "/<pk>/" (ej. /1/).
        """
        return reverse("product_detail", args=[self.pk])

    def __str__(self):
        return self.name


class Review(models.Model):
    """Modelo para reseñas de los productos"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)  # escala 1-5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review de {self.user.username} - {self.product.name}"


class Wishlist(models.Model):
    """Modelo para listas de deseos de los usuarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name="wishlists")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist de {self.user.username}"
