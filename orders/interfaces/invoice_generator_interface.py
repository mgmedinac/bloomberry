from abc import ABC, abstractmethod

class InvoiceGeneratorInterface(ABC):
    """Interfaz para generar facturas."""

    @abstractmethod
    def generate_invoice(self, order):
        """Genera la factura para un pedido."""
        pass
