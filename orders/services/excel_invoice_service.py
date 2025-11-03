# Autor: Salomé Serna
# Proyecto: BloomBerry 
# Archivo: orders/services/excel_invoice_service.py
# Descripción: Servicio para generar facturas en formato Excel.


import pandas as pd
from django.http import HttpResponse
from orders.models import OrderItem


class ExcelInvoiceGenerator:
    def generate_invoice(self, order):
        """Genera una factura en formato Excel a partir de una orden."""
        items = OrderItem.objects.filter(order=order)

        data = []
        for item in items:
            subtotal = item.product.price * item.quantity 
            data.append({
                "Producto": item.product.name,
                "Cantidad": item.quantity,
                "Precio Unitario": item.product.price,
                "Subtotal": subtotal
            })

        df = pd.DataFrame(data)
        df.loc[len(df.index)] = ["", "", "TOTAL", order.total]  

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Factura_{order.id}.xlsx"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Factura')

        return response
