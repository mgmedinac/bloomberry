# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: chat/views.py
# Descripción: Vistas para la sección de chat con el asistente AI.

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .models import ChatSession, Message
from .utils import AIRecommender


@require_http_methods(["GET"])
def chat_page(request):
    """
    Página principal del chat.
    Renderiza la plantilla con la sesión activa y los últimos mensajes.
    """
    chat = ChatSession.for_request(request)
    msgs = list(
        chat.messages.all().order_by("-created_at")[:50]
    )[::-1]  # últimos 50 en orden cronológico
    return render(request, "chat/chat.html", {"chat": chat, "messages": msgs})


@require_http_methods(["POST"])
def send_message(request):
    """
    Endpoint AJAX que recibe el mensaje del usuario,
    lo guarda en la sesión, llama al recomendador AI
    y devuelve JSON con la respuesta y productos sugeridos.
    """
    msg = (request.POST.get("message") or "").strip()
    if not msg:
        return HttpResponseBadRequest("Mensaje vacío")

    # Crear/recuperar sesión de chat
    chat = ChatSession.for_request(request)

    # Guardar mensaje del usuario
    Message.objects.create(chat=chat, role="user", content=msg)

    # Llamar al recomendador AI
    bot = AIRecommender()
    result = bot.answer(chat, msg)  # esperado: {'reply': str, 'items': [..]}

    reply = result.get("reply", "")
    items = (result.get("items") or [])[:5]

    # Guardar respuesta del asistente
    Message.objects.create(chat=chat, role="assistant", content=reply)

    # Preparar productos recomendados
    products = [
        {
            "name": it.get("name", "Producto"),
            "url": it.get("url", "#"),
            "price": it.get("price"),
            "brand": it.get("brand", ""),
        }
        for it in items
    ]

    return JsonResponse({"ok": True, "reply": reply, "products": products})
