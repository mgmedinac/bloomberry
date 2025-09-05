# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: users/forms.py
# Descripción: Formularios de registro y edición de perfil.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomerAccount


# === Formulario de Registro (solo username, email y password) ===
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# === Formulario de Perfil (se usa para editar el perfil luego) ===
class CustomerAccountForm(forms.ModelForm):
    class Meta:
        model = CustomerAccount
        fields = ("phone", "address", "city")
        labels = {
            "phone": "Teléfono",
            "address": "Dirección",
            "city": "Ciudad",
        }
