# Autor: Salomé Serna y Maria Clara
# Proyecto: BloomBerry
# Archivo: orders/views.py
# Descripción: Vistas para carrito de compras y checkout.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ShoppingCart, OrderInfo, OrderItem
from .helpers import calcular_total
from products.models import Product

# ====== IMPORTS PARA PDF======
from decimal import Decimal
from django.http import HttpResponse
from django.utils import timezone

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
# ============================


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


@login_required
def order_invoice_pdf(request, order_id):
    """
    Genera y descarga la factura en PDF para una orden del usuario actual.
    Usa OrderInfo y OrderItem. Si OrderItem no guarda precio, toma product.price.
    """
    order = get_object_or_404(OrderInfo, id=order_id, user=request.user)

    items = OrderItem.objects.filter(order=order).select_related("product")

    filename = f"Factura_BloomBerry_Orden_{order.id}.pdf"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    # === PDF con ReportLab ===
    p = canvas.Canvas(response, pagesize=A4)
    w, h = A4
    x = 20 * mm
    y = h - 25 * mm

    # Encabezado
    p.setFont("Helvetica-Bold", 20)
    p.drawString(x, y, "BloomBerry - Factura")
    y -= 12 * mm

    p.setFont("Helvetica", 11)
    p.drawString(x, y, f"Orden: #{order.id}")
    y -= 6 * mm

    created = getattr(order, "created_at", None) or getattr(order, "created", timezone.now())
    p.drawString(x, y, f"Fecha: {timezone.localtime(created).strftime('%d/%m/%Y %H:%M')}")
    y -= 6 * mm

    p.drawString(x, y, f"Cliente: {request.user.get_full_name() or request.user.username}")
    y -= 6 * mm
    p.drawString(x, y, f"Email: {request.user.email}")
    y -= 10 * mm

    # Separador
    p.line(x, y, w - x, y)
    y -= 8 * mm

    # Cabecera tabla
    p.setFont("Helvetica-Bold", 12)
    p.drawString(x, y, "Producto")
    p.drawString(w/2, y, "Cantidad")
    p.drawRightString(w - x, y, "Subtotal")
    y -= 7 * mm
    p.setFont("Helvetica", 11)

    total = Decimal("0.00")

    for it in items:
        # Datos por ítem
        name = getattr(getattr(it, "product", None), "name", None) or getattr(it, "product_name", "Producto")
        qty = getattr(it, "quantity", 1)

        unit_price = getattr(it, "price", None)
        if unit_price is None and getattr(it, "product", None) is not None:
            unit_price = getattr(it.product, "price", Decimal("0.00"))
        unit_price = Decimal(str(unit_price or "0.00"))

        subtotal = unit_price * Decimal(qty)
        total += subtotal

        # Salto de página simple
        if y < 25 * mm:
            p.showPage()
            y = h - 25 * mm
            p.setFont("Helvetica", 11)

        p.drawString(x, y, f"{name}")
        p.drawString(w/2, y, f"{qty}")
        p.drawRightString(w - x, y, f"${subtotal:,.2f}")
        y -= 6 * mm

    # Total
    y -= 8 * mm
    p.line(x, y, w - x, y)
    y -= 10 * mm

    p.setFont("Helvetica-Bold", 13)
    p.drawRightString(w - x, y, f"Total: ${total:,.2f}")

    y -= 20 * mm
    p.setFont("Helvetica", 9)
    p.drawString(x, y, "Gracias por tu compra 💜")

    p.showPage()
    p.save()
    # === /PDF ===

    return response