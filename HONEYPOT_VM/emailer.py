import smtplib
from email.mime.text import MIMEText
from config import SECURITY_TEAM_EMAIL, SMTP_SERVER, SMTP_USER, SMTP_PASS

def send_alert_email(message):
    msg = MIMEText(message)
    msg["Subject"] = "HONEYPOT SECURITY ALERT"
    msg["From"] = SMTP_USER
    msg["To"] = SECURITY_TEAM_EMAIL
    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)