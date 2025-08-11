import schedule
import time
import psutil
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

load_dotenv()

# Server Manager Configuration Parameters

#   Where to check disk usage
DISK_UTIL_DIR = "/"

#   Location for CSV logs
CSV_DIR = "usage_logs"

#   After how many days log files should be deleted
LOG_RETENTION_DUR = 30

os.makedirs(CSV_DIR, exist_ok=True)

def checkStats():

    memory_info = psutil.virtual_memory()
    #print (f"Memory: {memory_info.used / (1024**3):.2f} / {memory_info.total / (1024**3):.2f} GB")

    cpu_percent = psutil.cpu_percent(interval=1)
    #print (f"CPU Usage: {cpu_percent} %")

    disk_info = psutil.disk_usage(DISK_UTIL_DIR)
    #print(f"Disk Usage: {disk_info.used / (1024**3):.2f} / {disk_info.total / (1024**3):.2f} GB")

    return {
        "cpu_percent": cpu_percent,
        "memory_used": memory_info.used / (1024**3),
        "memory_avail": memory_info.total / (1024**3),
        "disk_used": disk_info.used / (1024**3),
        "disk_avail": disk_info.total / (1024**3),
    }

def write_stats_to_csv(stats):

    # Generate date-specific filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(CSV_DIR, f"{date_str}.csv")

    new_row = pd.DataFrame([{
        "timestamp [HR:Mn]": datetime.now().strftime("%H:%M"),
        
        "cpu usage [%]": stats["cpu_percent"],
        "memory used [GB]": f"{stats["memory_used"]:.2f}",
        "memory avail [GB]": f"{stats["memory_avail"]:.2f}",
        "disk used [GB]": f"{stats["disk_used"]:.2f}",
        "disk avail [GB]": f"{stats["disk_avail"]:.2f}"
    }])

    if not os.path.isfile(path):
        new_row.to_csv(path, index=False)
    else:
        new_row.to_csv(path, mode='a', header=False, index=False)

def csvUpdateWrapper():
    return write_stats_to_csv(checkStats())

def main():
    schedule.every().minute.do(csvUpdateWrapper)

    while(True):
        schedule.run_pending()
        time.sleep(20)
        
main()