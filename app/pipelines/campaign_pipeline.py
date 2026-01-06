import os
import pandas as pd
from datetime import datetime

from app.models.lead import Lead
from app.services.enrichment import enrich_lead
from app.services.email_generator import generate_email
from app.services.email_sender import send_email
from app.services.response_classifier import classify_response
from app.services.reporting import generate_report

DATA_DIR = "data"
REPORT_DIR = "reports"

INPUT_CSV = os.path.join(DATA_DIR, "leads.csv")
OUTPUT_CSV = os.path.join(DATA_DIR, "enriched_leads.csv")


def run_campaign():
    print("Starting AI Sales Campaign Pipeline...")

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

    df = pd.read_csv(INPUT_CSV)
    leads = []

    for _, row in df.iterrows():
        lead = Lead(
            name=row.get("name"),
            email=row.get("email"),
            company=row.get("company"),
            job_title=row.get("job_title"),
            industry=row.get("industry"),
        )
        leads.append(lead)

    processed_rows = []

    for idx, lead in enumerate(leads, start=1):
        print(f"Processing lead {idx}/{len(leads)}: {lead.email}")

        try:
            lead = enrich_lead(lead)
            subject, body = generate_email(lead)

            send_email(
                to_email=lead.email,
                subject=subject,
                body=body
            )
            lead.email_status = "Sent"
            lead.response_status = classify_response()

        except Exception as e:
            print(f"Error processing lead {lead.email}: {e}")
            lead.email_status = "Failed"
            lead.response_status = "Unknown"

        processed_rows.append({
            "name": lead.name,
            "email": lead.email,
            "company": lead.company,
            "job_title": lead.job_title,
            "industry": lead.industry,
            "priority": lead.priority,
            "persona": lead.persona,
            "email_status": lead.email_status,
            "response_status": lead.response_status,
        })

    enriched_df = pd.DataFrame(processed_rows)
    enriched_df.to_csv(OUTPUT_CSV, index=False)

    report_path = os.path.join(
        REPORT_DIR,
        f"campaign_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    )

    generate_report(enriched_df, report_path)

    print("Campaign completed successfully")
    print(f"Enriched CSV saved to: {OUTPUT_CSV}")
    print(f"Report generated at: {report_path}")