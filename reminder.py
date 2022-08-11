import tkinter.ttk as ttk
from turtle import title
from datetime import datetime
from datetime import date
import time
import threading
from plyer import notification

class Reminder:
    def __init__(self, hours, minutes, ampm, date, title, description):
        self.hours = hours
        self.min = minutes
        self.ampm = ampm
        self.date = date
        self.title = title
        self.desc = description

        daemon = threading.Thread(target=self.actual_time, daemon=True, name="Alarm")
        daemon.start()

    def alarm(self, alarm_time):
        while(True):
            time.sleep(1)
            current_time = datetime.now()
            now = current_time.strftime("%H:%M:%S") # Set to 24 hour to accept both 12 hour as well
            date = current_time.strftime("%m/%d/%Y")
            if(now == alarm_time and date == self.date):
                self.reminder()
                break

    def reminder(self):
        notification.notify(title=self.title, message=self.desc, timeout=1)

    def actual_time(self):
        if(0 <= int(self.hours) < 10 and self.ampm == "AM"):
            self.hours= "0" + self.hours
        elif(1 <= int(self.hours) < 12 and self.ampm == "PM"):
            self.hours = int(self.hours) + 12
        elif(int(self.hours) == 12 and self.ampm == "AM"):
            self.hours = "00"
        
        alarm_time = str(self.hours) + ":" + self.min + ":00"
        self.alarm(alarm_time)