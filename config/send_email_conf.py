from decouple import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage

email_addr = config("sender_email_addr")
email_pwd = config("sender_email_pwd")


def send_email_gmail(subject, message, destination):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    # This is where you would replace your password with the app password
    server.login(email_addr, email_pwd)

    msg = EmailMessage()

    message = f"{message}\n"

    msg.set_content(message, "html")
    msg["Subject"] = subject
    msg["From"] = email_addr
    msg["To"] = destination
    server.send_message(msg)
    server.close()
