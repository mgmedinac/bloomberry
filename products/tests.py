# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: products/tests.py
# Descripción: Pruebas para la aplicación de productos.


from django.test import TestCase, Client
from django.urls import reverse
from .models import Product

# Create your tests here.
class ProductAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        Product.objects.create(name="Crema facial", price=25000, stock=10, fabrication_date="2024-01-15")

    def test_api_products_returns_json(self):
        response = self.client.get(reverse('products:product_list_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn("Crema facial", response.content.decode())