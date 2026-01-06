from app.services.llm_client import call_llm

def generate_email(lead):
    prompt = f"Write short sales email for {lead.name}"
    _ = call_llm(prompt)

    subject = f"Quick idea for {lead.company}"
    body = f"""
Hi {lead.name},

I noticed your role as {lead.job_title}.
We help teams like yours improve sales efficiency using AI.

Would you be open to a quick chat?

Best regards,
AI Sales Team
"""
    return subject, body