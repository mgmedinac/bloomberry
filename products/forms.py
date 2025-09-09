# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: products/forms.py
# Descripción: Formularios para la app products, para las reseñas de productos.


from django import forms
from .models import Review
from django.utils.translation import gettext_lazy as _
from .models import Product  


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i,i) for i in range(1,6)]),
            'comment': forms.Textarea(attrs={'rows':4, 'placeholder': 'Escribe tu reseña...'}),
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name", "price", "stock", "category",
             "image",  "description",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "price": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "stock": forms.NumberInput(attrs={"min": "0"}),
        }
        labels = {
            "name": _("Nombre"),
            "price": _("Precio"),
            "stock": _("Stock"),
            "category": _("Categoría"),
            "image": _("Imagen"),
            "description": _("Descripción"),
        }