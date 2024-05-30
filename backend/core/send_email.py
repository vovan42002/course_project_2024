import smtplib
from email.mime.text import MIMEText
from core import config


def send_email(body, recipient):
    msg = MIMEText(body)
    msg["Subject"] = "Tickets for Cinema"
    msg["From"] = config.EMAIL_SENDER
    msg["To"] = recipient
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(config.EMAIL_SENDER, config.EMAIL_SENDER_PASSWORD)
        smtp_server.sendmail(config.EMAIL_SENDER, recipient, msg.as_string())
