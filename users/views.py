# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: users/views.py
# Descripción: Registro, perfil y edición de perfil + dashboard solo para staff.

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from .forms import RegisterForm, CustomerAccountForm
from .models import CustomerAccount

def register_view(request):
    if request.user.is_authenticated:
        return redirect("products:home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso. ¡Bienvenida/o a BloomBerry!")
            return redirect("products:home")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def profile_view(request):
    """
    Perfil del usuario autenticado.
    """
    profile = get_object_or_404(CustomerAccount, user=request.user)
    return render(request, "users/profile.html", {"profile": profile})


@login_required
def profile_edit_view(request):
    """
    Edición del perfil del usuario autenticado.
    """
    profile = get_object_or_404(CustomerAccount, user=request.user)

    if request.method == "POST":
        form = CustomerAccountForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Perfil actualizado."))
            return redirect("users:profile")
        else:
            messages.error(request, _("Revisa los errores y vuelve a intentar."))
    else:
        form = CustomerAccountForm(instance=profile)

    return render(request, "users/profile_edit.html", {"form": form})


@staff_member_required(login_url="login")
def admin_dashboard_view(request):
    """
    Vista solo para staff.
    - Si NO está autenticado -> redirige a login.
    - Si está autenticado pero NO es staff -> 403 Forbidden.
    """
    return render(request, "users/admin_dashboard.html")

@login_required
def order_history_view(request):
    """Muestra el historial de órdenes del usuario autenticado"""
    orders = request.user.orders.all().order_by("-created_at")
    return render(request, "orders/order_history.html", {"orders": orders})