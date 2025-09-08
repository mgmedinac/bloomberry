# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: orders/views.py
# Descripción: Vistas para carrito de compras y checkout.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ShoppingCart, OrderInfo, OrderItem
from .helpers import calcular_total
from products.models import Product


@login_required
def cart_view(request):
    """Muestra el carrito del usuario autenticado"""
    items = ShoppingCart.objects.filter(user=request.user)
    total = calcular_total(request.user)
    return render(request, "orders/cart.html", {"items": items, "total": total})


@login_required
def add_to_cart(request, product_id):
    """Agrega un producto al carrito"""
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = ShoppingCart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("orders:cart")


@login_required
def checkout_view(request):
    """Procesa el checkout y genera la orden"""
    items = ShoppingCart.objects.filter(user=request.user)
    total = calcular_total(request.user)

    if request.method == "POST":
        order = OrderInfo.objects.create(user=request.user, total=total, status="pending")
        for item in items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        items.delete()  # Vaciar carrito después del checkout
        return redirect("payments:checkout", order_id=order.id)

    return render(request, "orders/checkout.html", {"items": items, "total": total})

@login_required
def update_cart(request, item_id):
    """Actualiza la cantidad de un producto en el carrito"""
    item = get_object_or_404(ShoppingCart, id=item_id, user=request.user)
    if request.method == "POST":
        new_quantity = int(request.POST.get("quantity", 1))
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
        else:
            item.delete()  # si la cantidad es 0, eliminamos el producto
    return redirect("orders:cart")


@login_required
def remove_from_cart(request, item_id):
    """Elimina un producto del carrito"""
    item = get_object_or_404(ShoppingCart, id=item_id, user=request.user)
    item.delete()
    return redirect("orders:cart")

@login_required
def order_history_view(request):
    """Lista todas las órdenes del usuario actual"""
    orders = OrderInfo.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_history.html", {"orders": orders})
