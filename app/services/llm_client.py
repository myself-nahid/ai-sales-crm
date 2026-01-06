import requests
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL

def call_llm(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json=payload,
        timeout=60
    )

    response.raise_for_status()
    return response.json()["response"]
