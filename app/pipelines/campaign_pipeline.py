import os
import pandas as pd
from datetime import datetime
import json
import os

from app.models.lead import Lead
from app.services.enrichment import enrich_lead
from app.services.email_generator import generate_email
from app.services.email_sender import send_email
from app.services.response_classifier import classify_response
from app.services.reporting import generate_report

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
DEFAULT_REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "reports")

DATA_DIR = os.getenv("DATA_DIR", DEFAULT_DATA_DIR)
REPORT_DIR = os.getenv("REPORT_DIR", DEFAULT_REPORT_DIR)

INPUT_CSV = os.getenv("INPUT_CSV", os.path.join(DATA_DIR, "leads.csv"))
OUTPUT_CSV = os.getenv("OUTPUT_CSV", os.path.join(DATA_DIR, "enriched_leads.csv"))


def run_campaign():
    print("=" * 50)
    print("Starting AI Sales Campaign Pipeline...")
    print("=" * 50)

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    print(f"Data directory: {DATA_DIR}")
    print(f"Report directory: {REPORT_DIR}")

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

    # leads
    print(f"Reading leads from: {INPUT_CSV}")
    if not os.path.exists(INPUT_CSV):
        raise FileNotFoundError(f"Input CSV not found: {INPUT_CSV}")
    df = pd.read_csv(INPUT_CSV)
    print(f"Read {len(df)} rows from {INPUT_CSV}")
    if len(df) < 20:
        print("Warning: fewer than 20 leads found — demo acceptance requires 20+ leads")
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

    print(f"Loaded {len(leads)} leads")
    processed_rows = []

    for idx, lead in enumerate(leads, start=1):
        print(f"\n[{idx}/{len(leads)}] Processing: {lead.email}")

        try:
            print(f"Enriching lead...")
            lead = enrich_lead(lead)
            print(f"Priority: {lead.priority}, Persona: {lead.persona}")

            # Generate email
            print(f"Generating email...")
            subject, body = generate_email(lead)
            print(f"Subject: {subject}")

            # Send email
            print(f"Sending email...")
            send_email(
                to_email=lead.email,
                subject=subject,
                body=body
            )
            lead.email_status = "Sent"
            response_file_path = os.path.join(DATA_DIR, "responses", f"{lead.email}.txt")
            if os.path.exists(response_file_path):
                with open(response_file_path, 'r') as f:
                    response_text = f.read()
                lead.response_status = classify_response(response_text)
                print(f"Classified response: {lead.response_status}")
            else:
                lead.response_status = "Pending"
            print(f"Email sent successfully")

        except Exception as e:
            print(f"Error: {e}")
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

    # Save enriched CSV
    print(f"\nSaving enriched data to: {OUTPUT_CSV}")
    enriched_df = pd.DataFrame(processed_rows)
    enriched_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Enriched CSV saved with {len(enriched_df)} leads")

    # Generate report
    report_path = os.path.join(
        REPORT_DIR,
        f"campaign_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    )
    print(f"Generating report at: {report_path}")
    generate_report(enriched_df, report_path)
    print(f"Report generated")

    print("\n" + "=" * 50)
    print("Campaign completed successfully!")
    print(f"Enriched CSV: {OUTPUT_CSV}")
    print(f"Report: {report_path}")
    print("=" * 50)