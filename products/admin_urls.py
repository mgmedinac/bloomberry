# products/admin_urls.py
from django.urls import path
from . import admin_views as padmin

app_name = "products_admin"

urlpatterns = [
    path("products/", padmin.ProductAdminList.as_view(), name="admin_products_list"),
    path("products/new/", padmin.ProductAdminCreate.as_view(), name="admin_products_create"),
    path("products/<int:pk>/edit/", padmin.ProductAdminUpdate.as_view(), name="admin_products_edit"),
    path("products/<int:pk>/delete/", padmin.ProductAdminDelete.as_view(), name="admin_products_delete"),
]
