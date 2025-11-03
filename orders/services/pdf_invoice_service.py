# Autor: Salomé Serna
# Proyecto: BloomBerry
# Archivo: orders/services/pdf_invoice_service.py 
# Descripción: Servicio para generar facturas en formato PDF. 


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from orders.models import OrderItem


class PDFInvoiceGenerator:
    def generate_invoice(self, order):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Factura_{order.id}.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        # Encabezado
        p.setFont("Helvetica-Bold", 18)
        p.drawString(100, height - 80, "BloomBerry - Factura")
        p.setFont("Helvetica", 11)
        p.drawString(100, height - 110, f"Orden ID: {order.id}")
        p.drawString(100, height - 125, f"Cliente: {order.user.username}")
        p.drawString(100, height - 140, f"Estado: {order.status}")
        p.drawString(100, height - 160, f"Total: ${order.total}")  

        # Línea divisoria
        p.line(80, height - 170, 500, height - 170)
        y = height - 190

        # Productos
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Producto")
        p.drawString(300, y, "Cantidad")
        p.drawString(400, y, "Subtotal")
        p.setFont("Helvetica", 11)
        y -= 20

        for item in OrderItem.objects.filter(order=order):
            subtotal = item.product.price * item.quantity 
            p.drawString(100, y, item.product.name)
            p.drawString(300, y, str(item.quantity))
            p.drawString(400, y, f"${subtotal:.2f}")
            y -= 20

        p.showPage()
        p.save()
        return response
