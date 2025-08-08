from os import getenv
from dotenv import load_dotenv

load_dotenv()

sender_email = getenv('SENDER_EMAIL')
smtp_server = getenv('SMTP_SERVER')
smtp_port = getenv('SMTP_PORT')
sender_password = getenv('SENDER_PASSWORD')

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

receiver_email = "cparlee9@gmail.com"
subject = "Custom Email from Python"
body = "This is a custom email sent from Python using Mail-in-a-Box."

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain')) # or 'html' for HTML content

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection with TLS
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")