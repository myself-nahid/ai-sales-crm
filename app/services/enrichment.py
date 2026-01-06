from app.services.llm_client import call_llm

def enrich_lead(lead):
    prompt = f"Suggest buyer persona for {lead.job_title}"
    _ = call_llm(prompt)

    lead.persona = lead.job_title or "Business Decision Maker"
    return lead