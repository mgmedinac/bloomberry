# Autor: Maria Clara
# Proyecto: BloomBerry
# Archivo: products/admin_views.py
# Descripción: vistas para el panel de admin 


# products/admin_views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm

class StaffPermMixin(LoginRequiredMixin, PermissionRequiredMixin):
    raise_exception = True  # 403 si no tiene permisos

# LEER/LISTAR
class ProductAdminList(StaffPermMixin, ListView):
    model = Product
    template_name = "admin/products_list.html"
    context_object_name = "products"
    paginate_by = 12
    permission_required = "products.view_product"

    def get_queryset(self):
        qs = Product.objects.all().order_by("-updated_at" if hasattr(Product, "updated_at") else "-id")
        q = self.request.GET.get("q")
        active = self.request.GET.get("active")
        if q:
            qs = qs.filter(name__icontains=q)
        if active in ("1", "0"):
            qs = qs.filter(is_active=(active == "1"))
        return qs

# CREAR
class ProductAdminCreate(StaffPermMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "admin/product_form.html"
    success_url = reverse_lazy("admin_products_list")
    permission_required = "products.add_product"
    def form_valid(self, form):
        messages.success(self.request, _("Producto creado correctamente."))
        return super().form_valid(form)

# EDITAR
class ProductAdminUpdate(StaffPermMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "admin/product_form.html"
    success_url = reverse_lazy("admin_products_list")
    permission_required = "products.change_product"
    def form_valid(self, form):
        messages.success(self.request, _("Producto actualizado correctamente."))
        return super().form_valid(form)

# ELIMINAR
class ProductAdminDelete(StaffPermMixin, DeleteView):
    model = Product
    template_name = "admin/product_confirm_delete.html"
    success_url = reverse_lazy("admin_products_list")
    permission_required = "products.delete_product"
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Producto eliminado."))
        return super().delete(request, *args, **kwargs)
