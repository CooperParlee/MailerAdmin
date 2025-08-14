import psutil
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd

load_dotenv()

# Server Manager Configuration Parameters

#   Where to check disk usage
DISK_UTIL_DIR = "/"

#   Location for CSV logs
CSV_DIR = "usage_logs"

#   After how many days log files should be deleted
LOG_RETENTION_DUR = 30

# DO NOT EDIT BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING

os.makedirs(CSV_DIR, exist_ok=True)

def checkStats():

    memory_info = psutil.virtual_memory()

    cpu_percent = psutil.cpu_percent(interval=1)

    disk_info = psutil.disk_usage(DISK_UTIL_DIR)

    return {
        "cpu_percent": cpu_percent,
        "memory_used": memory_info.used / (1024**2),
        "memory_avail": memory_info.total / (1024**2),
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
        "memory used [MB]": f"{stats['memory_used']:.2f}",
        "memory avail [MB]": f"{stats['memory_avail']:.2f}",
        "disk used [GB]": f"{stats['disk_used']:.2f}",
        "disk avail [GB]": f"{stats['disk_avail']:.2f}"
    }])

    if not os.path.isfile(path):
        new_row.to_csv(path, index=False)
    else:
        new_row.to_csv(path, mode='a', header=False, index=False)

def csvUpdateWrapper():
    return write_stats_to_csv(checkStats())

def collectGarbage():
    for entry in os.listdir(CSV_DIR):
        path = os.path.join(CSV_DIR, entry)
        if os.path.isfile(path):
            try:
                mod_time = datetime.fromtimestamp(os.path.getmtime(path))
                if datetime.now() - mod_time > timedelta(days=LOG_RETENTION_DUR):
                    os.remove(path)
                    print("removing file: " + path)
                else:
                    print ("Preserving file due to age: " + path)
            except Exception as e:
                print("Unable to check file age given error: " + e)
                print("For file: " + path)