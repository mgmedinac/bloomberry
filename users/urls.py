# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: users/urls.py
# Descripción: Rutas de la app users.

from django.urls import path
from . import views
from django.utils.translation import gettext as _

app_name = 'users'

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit_view, name="profile_edit"),
    path("admin-dashboard/", views.admin_dashboard_view, name="admin_dashboard"),  # solo staff
    path("orders/history/", views.order_history_view, name="order_history"), 
    
]