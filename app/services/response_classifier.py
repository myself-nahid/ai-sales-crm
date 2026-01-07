import os
from app.services.llm_client import call_llm


def classify_response(response_text=None):
    if not response_text:
        return "Pending"

    text = response_text.lower()
    if "yes" in text or "interested" in text or "count me in" in text:
        return "Interested"
    if "no" in text or "not interested" in text or "no thanks" in text:
        return "Not Interested"

    OFFLINE = os.getenv("OFFLINE_MODE", "false").lower() in ("1", "true", "yes")
    if OFFLINE:
        return "Follow Up"

    prompt = f"""
Classify this response into:
Interested, Not Interested, or Follow Up.

Response:
"{response_text}"
"""
    try:
        return call_llm(prompt).strip()
    except Exception:
        return "Follow Up"