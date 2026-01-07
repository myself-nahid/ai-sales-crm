from datetime import datetime

def generate_report(leads_df, path="reports/campaign_summary.md"):
    high_priority_count = len(leads_df[leads_df['priority'] == 'High'])
    interested_count = len(leads_df[leads_df['response_status'] == 'Interested'])
    
    ai_insight = "Focus on high-priority technical decision makers."
    if interested_count > 0:
        successful_personas = leads_df[leads_df['response_status'] == 'Interested']['persona'].mode()
        if not successful_personas.empty:
            ai_insight = f"Campaign analysis suggests that {successful_personas[0]} personas are most receptive. Future campaigns should target this group."

    with open(path, "w") as f:
        f.write(f"# Campaign Summary\n\n")
        f.write(f"Date: {datetime.utcnow()}\n\n")
        f.write(f"- Total Leads: {len(leads_df)}\n")
        f.write(f"- High Priority Leads: {high_priority_count}\n")
        f.write(f"- Emails Sent: {len(leads_df)}\n")
        f.write(f"- Interested Responses: {interested_count}\n")
        f.write(f"\nAI Insight: {ai_insight}\n")