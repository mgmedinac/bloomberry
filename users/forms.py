# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: users/forms.py
# Descripción: Formularios de registro y edición de perfil.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomerAccount

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CustomerAccountForm(forms.ModelForm):
    class Meta:
        model = CustomerAccount
        fields = ("phone", "address", "city")
