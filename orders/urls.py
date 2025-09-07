# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: orders/urls.py
# Descripción: Rutas de la app de órdenes.

from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("cart/update/<int:item_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("order_detail/<int:order_id>/", views.order_detail_view, name="order_detail"),
]
