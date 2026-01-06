from app.services.lead_loader import load_leads, save_leads
from app.services.lead_scoring import score_lead
from app.services.enrichment import enrich_lead
from app.services.email_generator import generate_email
from app.services.email_sender import send_email
from app.services.response_classifier import classify_response
from app.services.reporting import generate_report

DATA_PATH = "data/leads.csv"
OUT_PATH = "data/enriched_leads.csv"

def run_campaign():
    leads = load_leads(DATA_PATH)

    for lead in leads:
        lead.priority = score_lead(lead)
        enrich_lead(lead)

        subject, body = generate_email(lead)
        send_email(lead.email, subject, body)

        lead.email_sent = True
        lead.response_status = classify_response()

    save_leads(leads, OUT_PATH)
    generate_report(leads)

    return {"status": "Campaign completed", "leads": len(leads)}