# Autor: Salomé Serna
# Proyecto: BloomBerry 
# Archivo: products/tests.py
# Descripción: Pruebas para la aplicación de productos.

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Product
from orders.models import ShoppingCart

# Create your tests here.

class CartTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.product = Product.objects.create(name="Bálsamo labial", price=15000, stock=5, fabrication_date="2024-02-20")

    def test_add_to_cart_creates_item(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse('orders:add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirección correcta
        self.assertTrue(ShoppingCart.objects.filter(user=self.user, product=self.product).exists())