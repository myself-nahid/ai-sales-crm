from app.services.llm_client import call_llm

def score_lead(lead) -> str:
    prompt = f"""
You are a sales AI assistant.
Score this lead priority as High, Medium, or Low.

Name: {lead.name}
Company: {lead.company}
Job Title: {lead.job_title}
Industry: {lead.industry}

Return only one word.
"""
    response = call_llm(prompt).strip()

    if response not in ["High", "Medium", "Low"]:
        return "Medium"
    return response