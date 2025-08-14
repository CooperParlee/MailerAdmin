import base64
from email.mime.image import MIMEImage
import schedule
import time
import psutil
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd

from generatePlot import generatePlot, generateBase64

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

def toHTML(string):
    return BeautifulSoup(string, "html.parser")

def dailyEmail():
    date = datetime.now() - timedelta(days=1)

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

        timestamps = csv['timestamp [HR:Mn]'].tolist()
        cpus = csv['cpu usage [%]'].to_list()

        memory_used = csv['memory used [MB]'].to_list()
        memory_total = csv['memory avail [MB]'].to_list()

        disk_used = csv['disk used [GB]'].to_list()
        disk_total = csv['disk avail [GB]'].to_list()
        
        cpu_plot = generatePlot("Server CPU Usage", ["Timestamp [EST]", "CPU Usage [%]"], [timestamps, cpus], "blue", "Blues")
        mem_plot = generatePlot("Server Memory Usage", ["Timestamp [EST]", "Memory Used [MB]"], [timestamps, memory_used, memory_total], "green", "Greens")
        disk_plot = generatePlot("Server Disk Usage", ["Timestamp [EST]", "Disk Usage [GB]"], [timestamps, disk_used, disk_total], "orange", "Oranges")

        img_cpu = generateBase64(cpu_plot)
        img_mem = generateBase64(mem_plot)
        img_disk = generateBase64(disk_plot)

    except Exception as e:
        print(f"Error reading CSV file: {e}")

    # Compose an email message to send

    cpu_loc = soup.find('div', {'id': 'CPU_graph'})
    if cpu_loc:
        cpu_loc.append(toHTML(f"<img src='cid:plot1' alt='Graph' />"))
    mem_loc = soup.find('div', {'id': 'Mem_graph'})
    if mem_loc:
        mem_loc.append(toHTML(f"<img src='cid:plot2' alt='Graph' />"))
    disk_loc = soup.find('div', {'id': 'Disk_graph'})
    if disk_loc:
        disk_loc.append(toHTML(f"<img src='cid:plot3' alt='Graph' />"))


    body = str(soup)

    msg = MIMEMultipart("related")
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_email)
    msg['Subject'] = subject

    msg_alt = MIMEMultipart("alternative")
    msg.attach(msg_alt)
    msg_alt.attach(MIMEText(body, 'html'))

    # Attach the generated PNG files as MIMEs
    
    mime_cpu = MIMEImage(base64.b64decode(img_cpu), _subtype="png")
    mime_cpu.add_header("Content-ID", "<plot1>")
    mime_cpu.add_header("Content-Disposition", "inline", filename="plot1.png")

    mime_mem = MIMEImage(base64.b64decode(img_mem), _subtype="png")
    mime_mem.add_header("Content-ID", "<plot2>")
    mime_mem.add_header("Content-Disposition", "inline", filename="plot2.png")

    mime_disk = MIMEImage(base64.b64decode(img_disk), _subtype="png")
    mime_disk.add_header("Content-ID", "<plot3>")
    mime_disk.add_header("Content-Disposition", "inline", filename="plot3.png")

    msg.attach(mime_cpu)
    msg.attach(mime_mem)
    msg.attach(mime_disk)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection with TLS
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

