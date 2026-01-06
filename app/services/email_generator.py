from app.services.llm_client import call_llm
from app.config import SENDER_NAME, SENDER_COMPANY

def generate_email(lead):
    prompt = f"""
You are a professional B2B sales assistant.

Write a complete outreach email (100–120 words).

Rules:
- Include a clear subject line
- Personalize for the lead
- End with a meeting request
- Do NOT use placeholders like [Your Name]
- Sign off with sender name and company

Lead Details:
Name: {lead.name}
Company: {lead.company}
Job Title: {lead.job_title}
Persona: {lead.persona}

Sender:
Name: {SENDER_NAME}
Company: {SENDER_COMPANY}

Return format exactly:
Subject: ...
Body: ...
"""

    response = call_llm(prompt)

    subject = "Quick introduction"
    body = ""

    for line in response.splitlines():
        if line.startswith("Subject:"):
            subject = line.replace("Subject:", "").strip()
        elif line.strip():
            body += line + "\n"

    body = body.replace("[Your Name]", SENDER_NAME)
    body = body.replace("[Your Company]", SENDER_COMPANY)

    return subject, body.strip()