# Autor: Maria Clara y Salome
# Proyecto: BloomBerry
# Archivo: products/urls.py
# Descripción: Rutas de la app products.

# Autor: Maria Clara y Salome
# Proyecto: BloomBerry
# Archivo: products/urls.py
# Descripción: Rutas de la app products.

from django.urls import path
from . import views
from . import views_api

app_name = 'products'

urlpatterns = [
    path("", views.home_view, name="home"),
    path("list/", views.product_list, name="list"),
    path("category/<slug:category_slug>/", views.product_list, name="category"),  # 👈 Filtro por categoría
    path("<int:product_id>/", views.product_detail, name="detail"),

    # Wishlist
    path("<int:product_id>/wishlist/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/", views.wishlist_view, name="view_wishlist"),
    path("wishlist/remove/<int:item_id>/", views.remove_from_wishlist, name="wishlist_remove"),

    # Reseñas
    path("<int:product_id>/review/", views.add_review, name="add_review"),

    # Búsqueda 
    path("search/", views.search_products, name="search_products"),

    # Funcionalidades interesantes: top 3 más vendidor y top 4 más comentados
    path("top-sold/", views.top_selling_products, name="top_selling_products"),
    path("top-reviewed/", views.most_reviewed_products, name="most_reviewed_products"),

    # API JSON
    path("products/api/", views_api.product_list_api, name="product_list_api"),
]
