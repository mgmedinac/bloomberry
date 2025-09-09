# Autor: Maria Clara Medina Gomez
# Proyecto: BloomBerry
# Archivo: utils.py
# Descripción: Conector a LLM (OpenRouter) y recomendador de productos para el chat.

import os
import re
import json
import requests
from django.conf import settings
from django.db.models import Q
from django.urls import reverse, NoReverseMatch
from products.models import Product  # ajusta si tu app/tabla difiere


# -------------------------------------------------------
# Utilidades de catálogo
# -------------------------------------------------------
def _short(txt, n=220):
    return (txt or "")[:n].strip()


def _infer_goals(text: str):
    """Detecta objetivos mencionados por el usuario."""
    t = (text or "").lower()
    keys = [
        "hidratación", "hidratacion",
        "acné", "acne",
        "manchas",
        "arrugas", "antiedad",
        "poros", "sensibilidad",
        "brillo", "seborrea", "grasa", "resequedad", "sequedad",
        "rojeces", "rosácea", "rosacea"
    ]
    goals = []
    for k in keys:
        if k in t and k not in goals:
            goals.append(k)
    return goals


def _product_url(p):
    """
    Resuelve la URL del producto de forma robusta.
    1) Si el modelo define get_absolute_url, úsalo.
    2) Intenta nombres de ruta comunes (product_detail, products:detail, products:product_detail).
    3) Fallback: "/<pk>/".
    """
    if hasattr(p, "get_absolute_url"):
        try:
            return p.get_absolute_url()
        except Exception:
            pass
    # intenta por nombre (args y kwargs)
    candidates = ("product_detail", "products:detail", "products:product_detail")
    for name in candidates:
        try:
            return reverse(name, args=[p.pk])
        except NoReverseMatch:
            try:
                return reverse(name, kwargs={"pk": p.pk})
            except NoReverseMatch:
                continue
    return f"/{p.pk}/"


def retrieve_catalog(filters: dict, limit=None):
    """
    Devuelve lista de dicts con productos relevantes según filtros:
    skin_type (str), goals (list[str]), price_max (int), price_min (int),
    keywords (list[str])  <-- uso principal para matching por texto
    """
    limit = limit or getattr(settings, "CHATBOT_MAX_PRODUCTS", 12)
    qs = Product.objects.all()

    skin = (filters or {}).get("skin_type")
    goals = (filters or {}).get("goals") or []
    price_max = (filters or {}).get("price_max")
    price_min = (filters or {}).get("price_min")
    keywords = (filters or {}).get("keywords") or []

    # 1) Filtros directos si existen campos dedicados en tu modelo
    if hasattr(Product, "skin_type") and skin:
        qs = qs.filter(skin_type__icontains=skin)
    if hasattr(Product, "concerns") and goals:
        q = Q()
        for g in goals:
            q |= Q(concerns__icontains=g)
        qs = qs.filter(q)
    if hasattr(Product, "price"):
        if price_max is not None:
            qs = qs.filter(price__lte=price_max)
        if price_min is not None:
            qs = qs.filter(price__gte=price_min)

    # 2) Búsqueda por keywords en name/description/brand/categorías
    if keywords:
        qk = Q()
        for k in keywords:
            qk |= Q(name__icontains=k) | Q(description__icontains=k)
            if hasattr(Product, "brand"):
                qk |= Q(brand__icontains=k)
            # Relaciones de categoría si existen
            if hasattr(Product, "category"):
                qk |= Q(category__name__icontains=k)
            if hasattr(Product, "categories"):  # ManyToMany
                qk |= Q(categories__name__icontains=k)
        qs = qs.filter(qk)

    # 3) Fallback: filtra por texto si no tienes campos dedicados
    if ((not hasattr(Product, "skin_type")) or (not hasattr(Product, "concerns"))) and skin:
        qs = qs.filter(Q(description__icontains=skin) | Q(name__icontains=skin))
    for g in goals:
        qs = qs.filter(Q(description__icontains=g) | Q(name__icontains=g))

    qs = qs.distinct()[:limit]

    items = []
    for p in qs:
        items.append({
            "id": getattr(p, "id", None),
            "name": getattr(p, "name", getattr(p, "title", "Producto")),
            "price": getattr(p, "price", None),
            "brand": getattr(p, "brand", ""),
            "skin_type": getattr(p, "skin_type", ""),
            "concerns": getattr(p, "concerns", ""),
            "summary": _short(getattr(p, "description", ""), 280),
            "url": _product_url(p),  # ⬅️ URL correcta según tus rutas
        })
    return items


# -------------------------------------------------------
# LLM Backend: OpenRouter (solo online)
# -------------------------------------------------------
class OpenRouterBackend:
    """
    Cliente mínimo para OpenRouter (endpoint /chat/completions).
    Incluye fallback a varios modelos :free por si alguno no está disponible.
    """
    def __init__(self):
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise RuntimeError("Falta OPENROUTER_API_KEY en el entorno.")
        self.base = getattr(settings, "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        # Principal desde settings
        main = getattr(settings, "OPENROUTER_MODEL", "google/gemma-3n-e2b-it:free")
        # Backups (ajusta si alguno no te funciona en tu cuenta)
        self.fallbacks = [
            main,
            "z-ai/glm-4.5-air:free",
            "tencent/hunyuan-a13b-instruct:free",
            "deepseek/deepseek-chat-v3.1:free",
            "openai/gpt-oss-20b:free",
        ]
        self.site_url = getattr(settings, "OPENROUTER_SITE_URL", "http://localhost:8000")
        self.app_name = getattr(settings, "OPENROUTER_APP_NAME", "BloomBerry")

    def chat(self, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Referer": self.site_url,   # opcional pero recomendado
            "X-Title": self.app_name,   # opcional pero recomendado
        }
        url = f"{self.base}/chat/completions"

        last_error = None
        for model in self.fallbacks:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.4,
                "max_tokens": 600,
            }
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=60)
                if r.status_code == 200:
                    data = r.json()
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    # 402 (saldo) / 404 (no endpoint) / otros -> intenta el siguiente
                    last_error = f"{r.status_code} {r.text[:200]}"
                    continue
            except Exception as e:
                last_error = str(e)
                continue

        return f"No pude generar respuesta (OpenRouter): {last_error or 'sin detalle'}"


def get_backend():
    """Actualmente solo OpenRouter para mantener el proyecto limpio."""
    return OpenRouterBackend()


# -------------------------------------------------------
# Recomendador “BloomBerry”
# -------------------------------------------------------
class AIRecommender:
    SYSTEM_INSTRUCTIONS = (
        "Eres el asistente de BloomBerry (cosmética). Hablas en español claro y útil. "
        "Puedes explicar productos, ingredientes, rutinas y políticas de la tienda. "
        "Debes priorizar los productos del catálogo que te doy. "
        "Si la pregunta no es de cuidado de la piel o la tienda, responde brevemente o pide aclaración. "
        "Nunca inventes precios: si no hay precio, dilo. "
        "Pregunta por tipo de piel, objetivos y presupuesto si faltan datos. "
        "Cuando recomiendes productos, usa estrictamente los del catálogo provisto (no inventes)."
    )

    def __init__(self):
        self.backend = get_backend()
        self.max_history = getattr(settings, "CHATBOT_MAX_HISTORY", 8)
        self.max_products = getattr(settings, "CHATBOT_MAX_PRODUCTS", 12)

    def build_catalog_context(self, items):
        lines = []
        for it in items:
            price = it.get("price")
            # No inventar precios
            if isinstance(price, (int, float)):
                price_str = f"${float(price):.0f}"
            elif price:
                price_str = str(price)
            else:
                price_str = "N/D"
            lines.append(
                f"- {it['name']} ({it.get('brand','')}) | {price_str} | "
                f"piel:{it.get('skin_type','')} | objetivos:{it.get('concerns','')} | "
                f"{it['summary']} | URL:{it['url']}"
            )
        return "\n".join(lines) if lines else "No hay productos relevantes."

    def _extract_keywords(self, text: str):
        """
        Extrae keywords útiles para buscar productos (ES/EN).
        Se queda con palabras >3 letras, quita stopwords básicas y añade sinónimos.
        """
        t = (text or "").lower()

        # sinónimos multi-palabra primero
        multi = []
        if "lip balm" in t:
            multi += ["lip balm", "bálsamo labial", "balsamo labial"]
        if "bálsamo labial" in t or "balsamo labial" in t:
            multi += ["bálsamo labial", "balsamo labial", "lip balm"]
        if "protector solar" in t or "spf" in t:
            multi += ["protector solar", "spf"]
        if "serum" in t or "suero" in t:
            multi += ["serum", "suero"]
        if "hidratante" in t or "moisturizer" in t:
            multi += ["hidratante", "moisturizer"]
        if "tonico" in t or "tónico" in t or "toner" in t:
            multi += ["tónico", "tonico", "toner"]

        # tokenización simple
        raw = re.findall(r"[a-záéíóúñü][a-záéíóúñü0-9\-]{2,}", t)
        stop = {
            "para","con","sin","los","las","unos","unas","de","del","la","el","y","o","en","por","que",
            "tipo","piel","mixta","grasa","seca","normal","sensible","presupuesto","hasta","max","máx",
            "quiero","necesito","mostrar","productos","producto","ver","tengo","me","ayuda","ayúdame",
            "acne","acné","manchas","poros","arrugas","antiedad","brillo","sensibilidad"
        }
        kws = [w for w in raw if w not in stop and len(w) > 3]

        # combina multi y tokens únicos
        out = []
        for k in multi + kws:
            if k not in out:
                out.append(k)
        return out[:6]  # no más de 6 keywords

    def _parse_filters(self, text):
        """Extrae filtros simples desde el mensaje del usuario."""
        text = (text or "").lower()
        skin = None
        for w in ["seca", "grasa", "mixta", "normal", "sensible"]:
            if w in text:
                skin = w
                break
        goals = _infer_goals(text)
        price_max = None
        m = re.search(r"(?:hasta|máx|max|tope|presupuesto)\s*\$?\s*(\d{2,6})", text)
        if m:
            try:
                price_max = int(m.group(1))
            except Exception:
                price_max = None

        keywords = self._extract_keywords(text)  # <— para buscar por “lip balm”, etc.
        return {"skin_type": skin, "goals": goals, "price_max": price_max, "keywords": keywords}

    def answer(self, chat, user_message: str):
        filters = self._parse_filters(user_message)
        items = retrieve_catalog(filters, limit=self.max_products)
        catalog_block = self.build_catalog_context(items)

        # Historial acotado (últimos N mensajes)
        last_msgs = list(chat.messages.all().order_by("-created_at")[:self.max_history])
        last_msgs.reverse()

        messages = [{"role": "system", "content": self.SYSTEM_INSTRUCTIONS}]
        messages.append({
            "role": "system",
            "content": f"CATÁLOGO ACTUAL (máx {self.max_products} ítems, prioriza estos al recomendar):\n{catalog_block}"
        })
        for m in last_msgs:
            messages.append({"role": m.role, "content": m.content})
        messages.append({"role": "user", "content": user_message})

        reply = self.backend.chat(messages).strip()

        # Devolvemos también items para que el front muestre links/chips
        return {"reply": reply, "items": items}
