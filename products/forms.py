# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: products/forms.py
# Descripción: Formularios para la app products, para las reseñas de productos.


from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i,i) for i in range(1,6)]),
            'comment': forms.Textarea(attrs={'rows':4, 'placeholder': 'Escribe tu reseña...'}),
        }
