import schedule
import time

from servStatusMessage import csvUpdateWrapper
from dailySystemEmail import dailyEmail

print("Starting Server Manager...")

def main():
    schedule.every().minute.do(csvUpdateWrapper)
    schedule.every().day.at("05:30").do(dailyEmail)

    while(True):
        schedule.run_pending()
        time.sleep(10)
        
main()