import schedule
import time

from servStatusMessage import csvUpdateWrapper, collectGarbage
from dailySystemEmail import dailyEmail

print("Starting Server Manager...")

def main():
    schedule.every().minute.do(csvUpdateWrapper)
    schedule.every().day.at("05:30").do(dailyEmail)
    schedule.every().day.at("00:15").do(collectGarbage)

    while(True):
        schedule.run_pending()
        time.sleep(10)
        
main()