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
@require_http_methods(["GET"])
def chat_page(request):
    chat = ChatSession.for_request(request)

    # Si la sesión no tiene mensajes, crea el nuevo saludo
    if not chat.messages.exists():
        Message.objects.create(chat=chat, role="assistant", content=AIRecommender.GREETING)
    else:
        # Si el primer mensaje fue el saludo viejo, lo actualizamos
        first = chat.messages.order_by("created_at").first()
        if first and first.role == "assistant" and "tipo de piel" in first.content.lower():
            first.content = AIRecommender.GREETING
            first.save(update_fields=["content"])

    chat_msgs = list(chat.messages.all().order_by("created_at"))[:50]
    return render(request, "chat/chat.html", {"chat": chat, "chat_messages": chat_msgs})


@require_http_methods(["POST"])
@require_http_methods(["POST"])
def send_message(request):
    msg = (request.POST.get("message") or "").strip()
    if not msg:
        return HttpResponseBadRequest("Mensaje vacío")

    chat = ChatSession.for_request(request)

    if not chat.messages.exists():
        Message.objects.create(chat=chat, role="assistant", content=AIRecommender.GREETING)
    else:
        first = chat.messages.order_by("created_at").first()
        if first and first.role == "assistant" and "tipo de piel" in first.content.lower():
            first.content = AIRecommender.GREETING
            first.save(update_fields=["content"])

    Message.objects.create(chat=chat, role="user", content=msg)

    bot = AIRecommender()
    result = bot.answer(chat, msg)
    reply = result.get("reply", "")
    items = (result.get("items") or [])[:5]

    Message.objects.create(chat=chat, role="assistant", content=reply)

    products = [
        {
            "name": it.get("name", "Producto"),
            "url": it.get("url", "#"),
            "price": it.get("price"),
            "brand": it.get("brand", ""),
        } for it in items
    ]
    return JsonResponse({"ok": True, "reply": reply, "products": products})
