from app.services.llm_client import call_llm

def generate_email(lead):
    prompt = f"""
Write a short, friendly B2B sales outreach email.

Lead:
Name: {lead.name}
Company: {lead.company}
Persona: {lead.persona}

Include subject and email body.
"""
    response = call_llm(prompt)

    subject = f"Quick idea for {lead.company}"
    body = response

    return subject, body