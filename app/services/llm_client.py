import os
import requests
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL


def call_llm(prompt: str) -> str:
    """Call the LLM. If OFFLINE_MODE is enabled, return deterministic mock outputs.

    The mock outputs aim to satisfy the enrichment/email/classification prompts used
    by the pipeline so demos are deterministic.
    """
    OFFLINE = os.getenv("OFFLINE_MODE", "false").lower() in ("1", "true", "yes")
    if OFFLINE:
        text = prompt.lower()
        if "return json" in text or "return json like" in text:
            return '{"priority":"Medium","persona":"Business Decision Maker"}'
        if "write a complete outreach email" in text or "outreach email" in text or "subject:" in text:
            return "Subject: Quick introduction\nHello,\nThis is a demo outreach email generated in OFFLINE_MODE.\nBest regards,\nAI Sales Team"
        if "classify this response" in text:
            return "Interested"
        # Generic fallback
        return "{\"priority\":\"Medium\",\"persona\":\"Business Decision Maker\"}"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 200,
            "temperature": 0.3
        }
    }

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json=payload,
        timeout=180
    )

    response.raise_for_status()
    return response.json()["response"]