import json
import re
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
        # Extract first JSON object from response (robust against LLM extra text)
        m = re.search(r"\{.*\}", response, re.DOTALL)
        if m:
            data = json.loads(m.group(0))
        else:
            data = json.loads(response)

        lead.priority = data.get("priority", "Medium")
        lead.persona = data.get("persona", "Business Decision Maker")
    except Exception:
        lead.priority = "Medium"
        lead.persona = "Business Decision Maker"

    return lead