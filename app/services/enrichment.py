from app.services.llm_client import call_llm

def enrich_lead(lead):
    prompt = f"""
Suggest a buyer persona based on this lead:

Job Title: {lead.job_title}
Company: {lead.company}
Industry: {lead.industry}

Return a short persona description.
"""
    lead.persona = call_llm(prompt).strip()
    return lead