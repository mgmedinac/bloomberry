# Create your views here.
# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: payments/views.py
# Descripción: Vistas simples para sección pública.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import OrderInfo
from payments.models import Payment

@login_required
def payment_checkout_view(request, order_id):
    """Simulación de checkout de pago"""
    order = get_object_or_404(OrderInfo, id=order_id, user=request.user)

    if request.method == "POST":
        # Marcar la orden como pagada
        order.status = "paid"
        order.save()

        # Crear el registro de pago con el usuario
        payment = Payment.objects.create(
            user=request.user,     
            order=order,
            amount=order.total,
            status="completed"
        )

        # Redirigir a la vista de éxito pasando el payment_id
        return redirect("payments:success", payment_id=payment.id)

    return render(request, "payments/checkout.html", {"order": order})


@login_required
def payment_success_view(request, payment_id):
    """Muestra el detalle del pago exitoso"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, "payments/success.html", {"payment": payment})
