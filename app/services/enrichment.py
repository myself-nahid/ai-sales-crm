from app.services.llm_client import call_llm

def enrich_lead(lead):
    prompt = f"""
You are a sales assistant.

Lead:
Name: {lead.name}
Company: {lead.company}
Job Title: {lead.job_title}
Industry: {lead.industry}

Tasks:
1. Assign priority: High, Medium, or Low
2. Suggest a short buyer persona

Return JSON like:
{{"priority":"High","persona":"CTO – Technical Decision Maker"}}
"""

    response = call_llm(prompt)

    try:
        data = eval(response)
        lead.priority = data.get("priority", "Medium")
        lead.persona = data.get("persona", "Business Decision Maker")
    except Exception:
        lead.priority = "Medium"
        lead.persona = "Business Decision Maker"

    return lead