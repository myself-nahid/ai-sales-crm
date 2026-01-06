from app.services.llm_client import call_llm

def score_lead(lead) -> str:
    prompt = f"Score lead priority for {lead.job_title} at {lead.company}"
    _ = call_llm(prompt)

    if lead.job_title and "CTO" in lead.job_title.upper():
        return "High"
    return "Medium"