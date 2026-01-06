import os

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = "llama3.2:3b"
SMTP_HOST = os.getenv("SMTP_HOST", "mailhog")
SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
FROM_EMAIL = "sales@ai-crm.local"
SENDER_NAME = "AI Sales Team"
SENDER_COMPANY = "AI CRM Platform"