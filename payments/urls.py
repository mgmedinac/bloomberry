# Autor: Maria Clara Medina Gomez y Salomé Serna
# Proyecto: BloomBerry
# Archivo: payments/urls.py
# Descripción: Rutas de la app payments.

from django.urls import path
from payments import views 


app_name = 'payments'

urlpatterns = [
    path("checkout/<int:order_id>/", views.payment_checkout_view, name="checkout"),
    path("success/<int:payment_id>/", views.payment_success_view, name="success"),  
]