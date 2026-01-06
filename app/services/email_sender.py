import smtplib
from email.message import EmailMessage
from app.config import SMTP_HOST, SMTP_PORT, FROM_EMAIL

def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.send_message(msg)