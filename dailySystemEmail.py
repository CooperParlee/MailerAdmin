import schedule
import time
import psutil
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
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

CSV_DIR = "usage_logs"

receiver_email = ["cooper@cooperparlee.com","cparlee9@gmail.com"]

def dailyEmail():
    date = datetime.now() - timedelta(days=1)

    date_string = date.strftime("%d %b %Y")
    subject = date_string + ": Daily System Status Update"

    with open("message.html", 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # parse some shit

    date_string_lab = soup.find('span', {'id': 'date_string'})
    if date_string_lab:
        date_string_lab.string = date_string

    sys_name_lab = soup.find('span', {'id': 'system_name'})
    if sys_name_lab:
        sys_name = os.getenv('SYSTEM_NAME')
        sys_name_lab.string = sys_name

    high_resource = False
    if high_resource:
        res_warn = soup.find('span', {'id': 'warning'})
        if res_warn:
            with open('./elements/warning.html', 'r') as warn_file:
                warn_soup = BeautifulSoup(warn_file, "html.parser")
                res_warn.append(warn_soup)

    # parse it with cool graphs now

    csv_path = os.path.join(CSV_DIR, f"{date.strftime("%Y-%m-%d")}.csv")

    try:
        csv = pd.read_csv(csv_path)

        # Read from the CSV file

        timestamps = csv["timestamp [HR:Mn]"].tolist()
        cpus = csv["cpu usage [%]"].to_list()

        memory_used = csv["memory used [GB]"].to_list()
        memory_total = csv["memory avail [GB]"].to_list()

        disk_used = csv["disk used [GB]"].to_list()
        disk_total = csv["disk avail [GB]"].to_list()
        
        







    except Exception as e:
        print(f"Error reading CSV file: {e}")

    # Compose an email message to send

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