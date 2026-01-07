import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from app.services import email_sender, llm_client

def noop_send_email(to_email, subject, body):
    print(f"[MOCK] send_email -> to={to_email} subject={subject}")

def mock_call_llm(prompt: str) -> str:
    # Return simple JSON string that enrich_lead expects
    return '{"priority":"High","persona":"CTO – Technical Decision Maker"}'

email_sender.send_email = noop_send_email
llm_client.call_llm = mock_call_llm

if __name__ == '__main__':
    from app.pipelines.campaign_pipeline import run_campaign
    run_campaign()
