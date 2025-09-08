# Autor: Salome Serna
# Proyecto: BloomBerry
# Archivo: products/views.py
# Descripción: Vistas para listar y detallar productos.


from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Review, Wishlist
from .forms import ReviewForm

def home_view(request):
    featured_products = Product.objects.all()[:4]
    return render(request, "products/home.html", {"featured_products": featured_products})

def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.select_related('user').order_by('-created_at')
    review_form = ReviewForm()
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = product.wishlists.filter(user=request.user).exists()
    return render(request, "products/product_detail.html", {
        "product": product,
        "reviews": reviews,
        "review_form": review_form,
        "in_wishlist": in_wishlist,
    })

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Si ya existe reseña del mismo usuario para el producto, la actualiza;
            # si no, la crea.
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment']
                }
            )
            messages.success(request, _("Tu reseña fue guardada."))
        else:
            messages.error(request, _("Hubo un error al enviar la reseña."))
    return redirect('products:detail', product_id=product.id)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # nombre por defecto de la wishlist (puedes cambiar / permitir elegir)
    wishlist_name = request.POST.get('wishlist_name', 'Favoritos')
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, name=wishlist_name)
    wishlist.products.add(product)
    messages.success(request, _("Producto agregado a tu lista de deseos."))
    return redirect('products:detail', product_id=product.id)

