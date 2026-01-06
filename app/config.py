import os

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")  # groq / hf / ollama / mock
SMTP_HOST = os.getenv("SMTP_HOST", "mailhog")
SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
FROM_EMAIL = "sales@ai-crm.local"