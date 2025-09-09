# Autor: Maria Clara Medina 
# Proyecto: BloomBerry
# Archivo: chat/models.py
# Descripción: Modelos para chat de chatbot


from django.db import models
from django.conf import settings

class ChatSession(models.Model):
    """Una sesión de chat por cookie de sesión de Django (usuario opcional)."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    session_key = models.CharField(max_length=40, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = self.user.username if self.user else "anon"
        return f"ChatSession({who}, {self.session_key})"

    @classmethod
    def for_request(cls, request):
        """Obtiene/crea la sesión de chat para la request actual."""
        # Asegura que exista una session_key
        if not request.session.session_key:
            request.session.save()
        key = request.session.session_key
        obj, _ = cls.objects.get_or_create(
            session_key=key,
            defaults={"user": request.user if request.user.is_authenticated else None},
        )
        return obj


class Message(models.Model):
    """Mensaje dentro de una sesión."""
    ROLE_CHOICES = [
        ("user", "user"),
        ("assistant", "assistant"),
        ("system", "system"),
    ]
    chat = models.ForeignKey(ChatSession, related_name="messages", on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"[{self.role}] {self.content[:40]}"
