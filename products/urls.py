# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: products/urls.py
# Descripción: Rutas de la app products.

from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path("", views.home_view, name="home"),
    path("list/", views.product_list, name="list"),
    path("<int:product_id>/", views.product_detail, name="detail"),
    path("<int:product_id>/review/", views.add_review, name='add_review'),
    path("<int:product_id>/wishlist/", views.add_to_wishlist, name='add_to_wishlist'),
]