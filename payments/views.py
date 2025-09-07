# Create your views here.
# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: payments/views.py
# Descripción: Vistas simples para sección pública.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import OrderInfo

@login_required
def payment_checkout_view(request, order_id):
    """Simulación de checkout de pago"""
    order = get_object_or_404(OrderInfo, id=order_id, user=request.user)

    if request.method == "POST":
        # En un escenario real aquí estaría la integración con la pasarela
        order.status = "paid"
        order.save()
        return redirect("payments:success", order_id=order.id)

    return render(request, "payments/checkout.html", {"order": order})


@login_required
def payment_success_view(request, order_id):
    """Vista de éxito después de pagar"""
    order = get_object_or_404(OrderInfo, id=order_id, user=request.user)
    return render(request, "payments/success.html", {"order": order})
