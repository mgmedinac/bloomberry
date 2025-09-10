# Autor: Maria Clara Medina Gomez + asist
# Proyecto: BloomBerry
# Archivo: chat/utils.py
# Descripción: Conector a LLM (OpenRouter) y recomendador de productos generalista.

import os
import re
import unicodedata
import difflib
import requests
from django.conf import settings
from django.db.models import Q
from django.urls import reverse, NoReverseMatch
from products.models import Product


# =========================
# Utilidades de texto
# =========================
def _short(txt, n=220):
    return (txt or "").strip()[:n]

def _norm(s: str) -> str:
    """Minúsculas + quita acentos/diacríticos."""
    s = (s or "").lower().strip()
    return "".join(
        c for c in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(c)
    )

def _deaccent(s: str) -> str:
    s = (s or "")
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def _tokenize(s: str):
    return re.findall(r"[a-záéíóúñü][a-záéíóúñü0-9\-]{2,}", (s or "").lower())

def _unique(seq):
    out = []
    for x in seq:
        if x not in out:
            out.append(x)
    return out


# =========================
# Vocabulario de dominio
# =========================
DOMAIN_TERMS = [
    # categorías/verticales
    "cosmética","maquillaje","skincare","cuidado facial","medicamentos",
    "suplementos","vitaminas","minerales","esencias","aromas","fragancias",
    # familias/ingredientes habituales
    "serum","suero","hidratante","cleanser","limpiador","tonico","tónico","toner",
    "protector solar","spf","retinol","ácido hialurónico","hialuronico","niacinamida",
    "biotina","colágeno","magnesio","omega","melatonina","vitamina c","vitamina b12","vitaminas",
    "vitamina d","probióticos","probioticos","multivitamínico","multivitaminico",
    # síntomas/objetivos
    "acné","acne","manchas","arrugas","poros","sensibilidad","rojeces","rosacea","rosácea",
    "resequedad","sequedad","grasa","brillo","energía","energia","estrés","estres","sueño","sueno",
    "ansiedad","dolor","resfriado","inmunidad","defensas","falta de vitaminas",
    # formatos
    "cápsulas","capsulas","tabletas","ungüento","unguento","crema","gel","spray","aceite",
    
]

# errores frecuentes → forma normalizada “correcta”
COMMON_MISSPELLINGS = {
    "acido hialuronico": "ácido hialurónico",
    "tonico": "tónico",
    "balsamo labial": "bálsamo labial",
    "rosacea": "rosácea",
    "vitamina b7": "biotina",
    "sueno": "sueño",
    "estres": "estrés",
}

# =========================
# Heurísticas de intención
# =========================
def _infer_goals(text: str):
    """Detecta objetivos/síntomas generales (no solo piel)."""
    t = _norm(text)
    keys = [
        "hidratacion","acne","manchas","arrugas","poros","sensibilidad","brillo","rosacea",
        "resequedad","sequedad","grasa","rojeces",
        "energia","estres","ansiedad","sueno","dolor","resfriado","inmunidad","defensas",
        "falta de vitaminas",
    ]
    found = []
    for k in keys:
        if k in t and k not in found:
            found.append(k)
    return found


# =========================
# URL de producto robusta
# =========================
def _product_url(p):
    """
    1) get_absolute_url si existe
    2) Nombres comunes de ruta
    3) Fallback /<pk>/
    """
    if hasattr(p, "get_absolute_url"):
        try:
            return p.get_absolute_url()
        except Exception:
            pass
    for name in ("product_detail", "products:detail", "products:product_detail"):
        try:
            return reverse(name, args=[p.pk])
        except NoReverseMatch:
            try:
                return reverse(name, kwargs={"pk": p.pk})
            except NoReverseMatch:
                continue
    return f"/{p.pk}/"


# =========================
# Corrección ortográfica simple (difflib)
# =========================
def build_search_vocab():
    """Construye vocabulario desde productos (nombre, marca, categorías) + términos de dominio."""
    vocab = set()
    for p in Product.objects.all().only("name", "description"):
        if getattr(p, "name", None):
            vocab.update(_tokenize(p.name))
        if hasattr(p, "brand") and p.brand:
            vocab.update(_tokenize(p.brand))
        # categorías
        if hasattr(p, "category") and getattr(p.category, "name", None):
            vocab.update(_tokenize(p.category.name))
        if hasattr(p, "categories"):  # ManyToMany
            for c in p.categories.all():
                vocab.update(_tokenize(c.name))
    for t in DOMAIN_TERMS:
        vocab.update(_tokenize(t))
    vocab = {_norm(w) for w in vocab if len(w) > 2}
    return vocab

def correct_token(tok: str, vocab):
    """Corrige un token si es muy parecido a algo del vocabulario."""
    tok_n = _norm(tok)
    if tok_n in vocab:
        return tok
    if tok_n in COMMON_MISSPELLINGS:
        return COMMON_MISSPELLINGS[tok_n]
    matches = difflib.get_close_matches(tok_n, list(vocab), n=1, cutoff=0.8)
    if matches:
        return matches[0]
    return tok


# =========================
# Extracción/expansión de keywords
# =========================
STOPWORDS = {
    "para","con","sin","los","las","unos","unas","de","del","la","el","y","o","en","por","que",
    "tipo","piel","mixta","grasa","seca","normal","sensible","presupuesto","hasta","max","máx","maximo","máximo",
    "quiero","necesito","mostrar","productos","producto","ver","tengo","ayuda","ayudame","ayúdame",
}

MULTI_SYNONYMS = [
    ("lip balm", ["lip balm","bálsamo labial","balsamo labial"]),
    ("protector solar", ["protector solar","spf"]),
    ("serum", ["serum","suero"]),
    ("hidratante", ["hidratante","moisturizer"]),
    ("tónico", ["tónico","tonico","toner"]),
    ("vitaminas", ["vitamina","vitaminas","vitamins"]),
    ("biotina", ["biotina","vitamina b7","b7"]),
]

KEYWORD_EXPANSIONS = {
    "vitaminas": ["vitamina", "multivitamínico", "multivitaminico",
                  "vitamina c", "vitamina d", "vitamina b12", "biotina"],
    "vitamina":  ["vitaminas", "multivitamínico", "multivitaminico",
                  "vitamina c", "vitamina d", "vitamina b12", "biotina"],
    "vitamina c":["ascórbico","acido ascorbico","ácido ascórbico","vitamina"],
    "vitamina d":["colecalciferol","vitamina"],
    "vitamina b12":["cobalamina","vitamina"],
    "biotina":   ["vitamina b7","vitamina","vitaminas"],
    "multivitamínico":["vitaminas","multivitaminico","vitamina"],
    "suplemento":["suplementos","vitaminas","multivitamínico","multivitaminico"],
    "suplementos":["suplemento","vitaminas","multivitamínico","multivitaminico"],
}

def expand_keywords(base_keywords):
    """Devuelve keywords + sinónimos + versiones sin acentos (únicas)."""
    out = []
    seen = set()
    for k in base_keywords:
        cand = [k]
        kn = _norm(k)
        for key, adds in KEYWORD_EXPANSIONS.items():
            if kn == _norm(key):
                cand += adds
        cand += [_deaccent(c) for c in cand]
        for c in cand:
            if c not in seen:
                seen.add(c)
                out.append(c)
    return out

def extract_keywords(text: str, vocab=None, limit=8):
    """Palabras clave en ES/EN con normalización, sinónimos y corrección."""
    t = (text or "")
    vocab = vocab or build_search_vocab()

    # multi-palabras
    multi = []
    t_l = t.lower()
    for base, alts in MULTI_SYNONYMS:
        if any(a in t_l for a in alts):
            multi.append(base)

    # tokens simples
    raw = _tokenize(t)
    toks = []
    for w in raw:
        w_n = _norm(w)
        if w_n in STOPWORDS or len(w_n) <= 2:
            continue
        corr = correct_token(w_n, vocab)
        toks.append(corr)

    expanded = expand_keywords(_unique(multi + toks))
    return expanded[: max(limit, 12)]


# =========================
# Consulta al catálogo (robusta con fallback)
# =========================
def _q_like(field, term):
    """Q para icontains de term y su versión sin acento."""
    t1 = term
    t2 = _deaccent(term)
    q = Q(**{f"{field}__icontains": t1})
    if t2 != t1:
        q |= Q(**{f"{field}__icontains": t2})
    return q

def _q_any(fields, term):
    q = Q()
    for f in fields:
        q |= _q_like(f, term)
    return q

def retrieve_catalog(filters: dict, limit=None):
    """
    Devuelve lista de dicts con productos relevantes según filtros:
    - goals (list[str])
    - price_max, price_min
    - keywords (list[str])  <-- principal (ya expandidas)
    - category_hint (str)   <-- opcional
    """
    limit = limit or getattr(settings, "CHATBOT_MAX_PRODUCTS", 12)
    qs_base = Product.objects.all()

    goals = (filters or {}).get("goals") or []
    price_max = (filters or {}).get("price_max")
    price_min = (filters or {}).get("price_min")
    keywords = (filters or {}).get("keywords") or []
    category_hint = (filters or {}).get("category_hint")

    # precio
    if hasattr(Product, "price"):
        if price_max is not None:
            qs_base = qs_base.filter(price__lte=price_max)
        if price_min is not None:
            qs_base = qs_base.filter(price__gte=price_min)

    # campos de búsqueda
    text_fields = ["name", "description"]
    if hasattr(Product, "brand"):
        text_fields.append("brand")
    if hasattr(Product, "category"):
        text_fields.append("category__name")
    if hasattr(Product, "categories"):
        text_fields.append("categories__name")

    # primer pase (más dirigido)
    qs = qs_base
    if category_hint and hasattr(Product, "category"):
        qs = qs.filter(_q_like("category__name", category_hint))

    if keywords:
        qk = Q()
        for k in keywords:
            qk |= _q_any(text_fields, k)
        qs = qs.filter(qk)

    for g in goals:
        qs = qs.filter(_q_any(["name","description"], g))

    qs = qs.distinct()[:limit]
    items = list(qs)

    # fallback si quedó vacío
    if not items:
        qs = qs_base
        qk = Q()
        
        vitamin_triggers = ["vitamina", "vitaminas", "multivitam", "b12", "biotina", "vitamina c", "vitamina d"]
        if any(any(vt in _norm(k) for vt in vitamin_triggers) for k in keywords):
            for t in ["vitamin", "vitamina", "multivit", "multivitam",
                      "biotina", "b12", "vitamina c", "vitamina d"]:
                qk |= _q_any(text_fields, t)
            if hasattr(Product, "category"):
                qk |= _q_like("category__name", "suplement")
                qk |= _q_like("category__name", "vitamin")
        else:
            # fallback genérico: usa keywords tal cual + sin acento + algunos comodines
            base_keys = keywords or ["suplemento", "vitamina", "multivitam"]
            for k in base_keys:
                qk |= _q_any(text_fields, k)

        for g in goals:
            qk |= _q_any(["name","description"], g)

        qs = qs.filter(qk).distinct()[:limit]
        items = list(qs)

    out = []
    for p in items:
        out.append({
            "id": getattr(p, "id", None),
            "name": getattr(p, "name", getattr(p, "title", "Producto")),
            "price": getattr(p, "price", None),
            "brand": getattr(p, "brand", ""),
            "summary": _short(getattr(p, "description", ""), 280),
            "url": _product_url(p),
            "category": getattr(getattr(p, "category", None), "name", ""),
        })
    return out


# =========================
# LLM (OpenRouter)
# =========================
class OpenRouterBackend:
    def __init__(self):
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise RuntimeError("Falta OPENROUTER_API_KEY en el entorno.")
        self.base = getattr(settings, "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        main = getattr(settings, "OPENROUTER_MODEL", "google/gemma-3n-e2b-it:free")
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
            "Referer": self.site_url,
            "X-Title": self.app_name,
        }
        url = f"{self.base}/chat/completions"

        last_error = None
        for model in self.fallbacks:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.4,
                "max_tokens": 700,
            }
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=60)
                if r.status_code == 200:
                    data = r.json()
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    last_error = f"{r.status_code} {r.text[:200]}"
                    continue
            except Exception as e:
                last_error = str(e)
                continue

        return f"No pude generar respuesta (OpenRouter): {last_error or 'sin detalle'}"


def get_backend():
    return OpenRouterBackend()


# =========================
# Recomendador generalista
# =========================
class AIRecommender:
    GREETING = (
        "¡Hola! Soy tu asistente virtual de BloomBerry 😊. "
        "Puedo ayudarte con productos de cuidado facial, maquillaje, medicamentos naturales, "
        "esencias y suplementos diarios. ¿Qué estás buscando hoy?"
    )

    SYSTEM_INSTRUCTIONS = (
        "Eres el asistente de BloomBerry (tienda de productos naturales y cosmética). "
        "Hablas en español claro y útil. "
        "Entiendes consultas generales (cosmética, medicamentos naturales, suplementos, maquillaje, esencias). "
        "Prioriza SIEMPRE recomendar productos del catálogo provisto y no inventes artículos o precios. "
        "Si el usuario pide algo que no existe en el catálogo, dilo explícitamente y ofrece alternativas cercanas. "
        "Detecta y corrige errores ortográficos, sinónimos y términos en ES/EN. "
        "Si faltan datos importantes (p.ej., tipo de producto, objetivo o presupuesto) pide una aclaración breve. "
        "Cuando listes recomendaciones, incluye nombre y un breve motivo; nunca inventes stock ni propiedades médicas."
    )

    def __init__(self):
        self.backend = get_backend()
        self.max_history = getattr(settings, "CHATBOT_MAX_HISTORY", 8)
        self.max_products = getattr(settings, "CHATBOT_MAX_PRODUCTS", 12)

    def _guess_category_hint(self, keywords):
        """Intenta inferir una categoría a partir de keywords (para priorizar resultados)."""
        k = " ".join(keywords).lower()
        if any(w in k for w in ["medicamento","medicamentos","resfriado","dolor","inmunidad","defensas"]):
            return "medicamento"
        if any(w in k for w in ["suplemento","suplementos","vitamina","vitaminas","biotina","colágeno","omega","magnesio","melatonina"]):
            return "suplemento"
        if any(w in k for w in ["esencia","aroma","fragancia","aceite esencial","aceite"]):
            return "esencia"
        if any(w in k for w in ["maquillaje","labial","lipstick","pestañina","rubor","base"]):
            return "maquillaje"
        if any(w in k for w in ["limpiador","tonico","tónico","serum","suero","hidratante","protector solar","spf"]):
            return "cuidado"
        return None

    def _parse_filters(self, text):
        vocab = build_search_vocab()
        goals = _infer_goals(text)
        keywords = extract_keywords(text, vocab=vocab, limit=10)
        price_max = None
        m = re.search(r"(?:hasta|máx|max|tope|presupuesto)\s*\$?\s*(\d{2,6})", (text or "").lower())
        if m:
            try:
                price_max = int(m.group(1))
            except Exception:
                price_max = None
        category_hint = self._guess_category_hint(keywords)
        return {"goals": goals, "price_max": price_max, "keywords": keywords, "category_hint": category_hint}

    def build_catalog_context(self, items):
        if not items:
            return "No hay productos relevantes."
        lines = []
        for it in items:
            price = it.get("price")
            price_str = f"${float(price):.0f}" if isinstance(price, (int, float)) else (str(price) if price else "N/D")
            lines.append(
                f"- {it['name']} ({it.get('brand','')}) | {price_str} | cat:{it.get('category','')} | {it['summary']} | URL:{it['url']}"
            )
        return "\n".join(lines)

    def answer(self, chat, user_message: str):
        """
        Devuelve dict: {'reply': str, 'items': list[dict]}
        """
        try:
            filters = self._parse_filters(user_message)
            items = retrieve_catalog(filters, limit=self.max_products)
            catalog_block = self.build_catalog_context(items)

            # Historial (últimos N)
            last_msgs = list(chat.messages.all().order_by("-created_at")[:self.max_history])
            last_msgs.reverse()

            messages = [{"role": "system", "content": self.SYSTEM_INSTRUCTIONS}]
            messages.append({
                "role": "system",
                "content": f"CATÁLOGO ACTUAL (máx {self.max_products} ítems; recomienda SOLO de aquí si es posible):\n{catalog_block}"
            })
            for m in last_msgs:
                messages.append({"role": m.role, "content": m.content})
            messages.append({"role": "user", "content": user_message})

            reply = self.backend.chat(messages).strip()

            if not items:
                reply += "\n\nPor ahora no encuentro ese producto en nuestra tienda. Puedo mostrarte alternativas relacionadas si me das más detalles."

            return {"reply": reply, "items": items}
        except Exception as e:
            return {
                "reply": f"Ups, hubo un problema al procesar tu consulta. ¿Podrías reformularla? (detalle: {e})",
                "items": []
            }
