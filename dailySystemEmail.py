import schedule
import time
import psutil
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

load_dotenv()

sender_email = os.getenv('SENDER_EMAIL')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
sender_password = os.getenv('SENDER_PASSWORD')

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

receiver_email = ["cooper@cooperparlee.com","cparlee9@gmail.com"]

def dailyEmail():
    date_string = datetime.now().strftime("%d %b %Y")
    subject = date_string + ": Daily System Status Update"
    body = """
    <html>
    <head></head>
    <body>
        <h2>System Stats Report</h2>
        <p><b>CPU Usage:</b> 45%</p>
        <p><b>Memory Usage:</b> 68%</p>
        <p><b>Disk Space:</b> 72% used</p>
        <hr>
        <p style="color: gray; font-size: small;">Generated automatically by the monitoring script.</p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_email)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html')) # or 'html' for HTML content

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection with TLS
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

dailyEmail()