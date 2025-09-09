#!/usr/bin/env python3
import os, sys, requests

API = os.environ.get("OPENROUTER_API_KEY")
if not API:
    print("ERROR: Falta OPENROUTER_API_KEY en el entorno.")
    sys.exit(1)

def choose_free_model():
    # 1) Traer catálogo de modelos
    r = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {API}"},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()

    # 2) Candidatos :free de propósito general (evitar coder/vision)
    candidates = []
    for m in data.get("data", []):
        mid = m["id"]
        name = mid.lower()
        if not mid.endswith(":free"):
            continue
        if any(x in name for x in ("coder", "code", "vl", "vision")):
            continue
        candidates.append(mid)

    preferred_front = [
        "google/gemma-3n-e2b-it:free",
        "z-ai/glm-4.5-air:free",
        "tencent/hunyuan-a13b-instruct:free",
        "deepseek/deepseek-chat-v3.1:free",
        "openai/gpt-oss-20b:free",
    ]
    seen = set()
    ordered = [m for m in preferred_front + candidates if not (m in seen or seen.add(m))]

    print(f"Probando {len(ordered)} candidatos…")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API}",
        "Content-Type": "application/json",
        "Referer": "http://localhost:8000",
        "X-Title": "BloomBerry",
    }

    for model in ordered[:20]:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Di hola en una frase."}],
            "temperature": 0.4,
            "max_tokens": 60,
        }
        print(f"→ {model} … ", end="", flush=True)
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            if resp.status_code == 200:
                txt = resp.json()["choices"][0]["message"]["content"].strip()
                print("OK ✅")
                print("Respuesta:", txt.replace("\n", " ")[:200])
                return model
            else:
                print(f"FAIL [{resp.status_code}] {resp.text[:120]}")
        except Exception as e:
            print("ERROR:", e)

    return None

if __name__ == "__main__":
    model = choose_free_model()
    if model:
        print("\nModelo elegido:", model)
        sys.exit(0)
    print("\nNo pude encontrar un modelo :free disponible ahora.")
    sys.exit(2)
