# Create your views here.
# Autor: 
# Proyecto: BloomBerry
# Archivo: chat/views.py
# Descripción: Vistas simples para sección pública.
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .models import ChatSession, Message
from .utils import AIRecommender

@require_http_methods(["GET"])
def chat_page(request):
    """Página de chat (plantilla chat/chat.html)."""
    chat = ChatSession.for_request(request)
    msgs = list(chat.messages.all().order_by("-created_at")[:50])[::-1]  # últimos 50 en orden cronológico
    return render(request, "chat/chat.html", {"chat": chat, "messages": msgs})

@require_http_methods(["POST"])
def send_message(request):
    """Endpoint AJAX que envía el mensaje al LLM y devuelve JSON."""
    msg = (request.POST.get("message") or "").strip()
    if not msg:
        return HttpResponseBadRequest("Mensaje vacío")

    chat = ChatSession.for_request(request)
    Message.objects.create(chat=chat, role="user", content=msg)

    bot = AIRecommender()
    result = bot.answer(chat, msg)     # {'reply': str, 'items': [..]}
    reply = result["reply"]
    items = (result.get("items") or [])[:5]

    Message.objects.create(chat=chat, role="assistant", content=reply)

    products = [{
        "name": it.get("name", "Producto"),
        "url": it.get("url", "#"),
        "price": it.get("price"),
        "brand": it.get("brand", ""),
    } for it in items]

    return JsonResponse({"ok": True, "reply": reply, "products": products})
