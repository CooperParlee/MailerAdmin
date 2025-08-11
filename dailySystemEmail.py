import schedule
import time
import psutil
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

from bs4 import BeautifulSoup

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

    with open("message.html", 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # parse some shit

    date_string_lab = soup.find('span', {'id': 'date_string'})
    if date_string_lab:
        date_string_lab.string = date_string

    sys_name_lab = soup.find('span', {'id': 'system_name'})
    if sys_name_lab:
        sys_name_lab.string = os.getenv('SYSTEM_NAME')

    # parse it with cool graphs now

    body = str(soup)

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