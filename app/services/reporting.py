from datetime import datetime

def generate_report(leads_df, path="reports/campaign_summary.md"):
    high = len(leads_df[leads_df['priority'] == 'High'])
    
    with open(path, "w") as f:
        f.write(f"# Campaign Summary\n\n")
        f.write(f"Date: {datetime.utcnow()}\n\n")
        f.write(f"- Total Leads: {len(leads_df)}\n")
        f.write(f"- High Priority Leads: {high}\n")
        f.write(f"- Emails Sent: {len(leads_df)}\n")
        f.write("\nAI Insight: Focus on high-priority technical decision makers.\n")