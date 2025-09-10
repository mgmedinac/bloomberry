# Autor: Salome Serna
# Proyecto: BloomBerry
# Archivo: products/views.py
# Descripción: Vistas para listar y detallar productos.


from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Category, Product, Review, Wishlist
from .forms import ReviewForm

def home_view(request):
    featured_products = Product.objects.all()[:4]
    return render(request, "products/home.html", {"featured_products": featured_products})

def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.all()

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, "products/product_list.html", {
        "categories": categories,
        "products": products,
        "selected_category": category,
    })


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
    


def search_products(request):
    query = request.GET.get('q')  # lo que el usuario escribe en la lupa
    results = []

    if query:
        results = Product.objects.filter(name__icontains=query)

    return render(request, 'products/search_results.html', {
        'query': query,
        'results': results,
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
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user, name="Favoritos")
    items = wishlist.products.all()
    return render(request, "products/wishlist.html", {"wishlist": wishlist, "items": items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user, name="Favoritos")
    if wishlist.products.filter(pk=product.pk).exists():
        messages.info(request, "Este producto ya está en tus favoritos.")
    else:
        wishlist.products.add(product)
        messages.success(request, "Producto agregado a tu lista de favoritos.")
    # Volver a donde estaba el usuario
    return redirect(request.META.get("HTTP_REFERER") or "products:detail", product_id)

@login_required
def remove_from_wishlist(request, item_id):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user, name="Favoritos")
    product = get_object_or_404(Product, pk=item_id)
    if wishlist.products.filter(pk=product.pk).exists():
        wishlist.products.remove(product)
        messages.success(request, "Producto eliminado de tus favoritos.")
    else:
        messages.info(request, "El producto no estaba en tu lista.")
    return redirect("products:view_wishlist")