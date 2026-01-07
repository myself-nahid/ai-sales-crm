import os
import smtplib
from email.message import EmailMessage
from app.config import SMTP_HOST, SMTP_PORT, FROM_EMAIL


def send_email(to_email, subject, body):
    """Send an email unless SEND_EMAILS is false; in demos MailHog is expected."""
    SEND = os.getenv("SEND_EMAILS", "true").lower() in ("1", "true", "yes")

    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    if not SEND:
        print(f"[DRY RUN] Email to {to_email} skipped (SEND_EMAILS=false). Subject: {subject}")
        try:
            import pathlib
            rpt_dir = pathlib.Path("./reports")
            rpt_dir.mkdir(parents=True, exist_ok=True)
            with open(rpt_dir / "emails.log", "a", encoding="utf-8") as f:
                f.write(f"To: {to_email}\nSubject: {subject}\nBody:\n{body}\n---\n")
        except Exception:
            pass
        return

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.send_message(msg)