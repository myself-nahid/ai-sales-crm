from app.services.llm_client import call_llm

def classify_response():
    prompt = """
Classify this response into:
Interested, Not Interested, or Follow Up.

Response:
"Thanks, this looks interesting. Let's talk next week."
"""
    return call_llm(prompt).strip()