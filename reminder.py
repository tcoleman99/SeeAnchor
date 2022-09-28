import tkinter.ttk as ttk
from turtle import title
from datetime import datetime
from datetime import date
import time
import threading
from threading import Event
from plyer import notification

class Reminder:
    def __init__(self, parent, hours, minutes, ampm, date, title, description, count):
        self.parent = parent
        self.hours = hours
        self.min = minutes
        self.ampm = ampm
        self.date = date
        self.title = title
        self.desc = description
        self.row = count
        self.alarm_time = ""
        self.stop_event = Event()

        self.displayhours = self.hours

        self.daemon = threading.Thread(target=self.alarm, args=(self.stop_event,), daemon=True, name="Alarm")
        self.daemon.start()

    def alarm(self, event):
        if(0 <= int(self.hours) < 10 and self.ampm == "AM"):
            self.displayhours = self.hours
            self.hours= "0" + self.hours
        elif(1 <= int(self.hours) < 12 and self.ampm == "PM"):
            self.displayhours = self.hours
            self.hours = int(self.hours) + 12
        elif(int(self.hours) == 12 and self.ampm == "AM"):
            self.displayhours = self.hours
            self.hours = "00"
        
        self.alarm_time = str(self.hours) + ":" + self.min + ":00"

        while not event.is_set():
            time.sleep(1)
            current_time = datetime.now()
            now = current_time.strftime("%H:%M:%S") # Set to 24 hour to accept both 12 hour as well
            date = current_time.strftime("%m/%d/%Y")
            if(now == self.alarm_time and date == self.date):
                notification.notify(title=self.title, message=self.desc, timeout=1)
                self.parent.remind_button_list[self.row].configure(bg="tomato")
                break

    # def reminder(self):
    #     notification.notify(title=self.title, message=self.desc, timeout=1)

    def update(self):
        self.stop_event.set()
        self.daemon.join()
        self.stop_event.clear()
        self.daemon = threading.Thread(target=self.alarm, args=(self.stop_event,), daemon=True, name="Alarm")
        self.daemon.start()

    def open(self, calendar, hentry, mentry, drop, tentry, dentry):
        hentry.configure(bg="white")
        mentry.configure(bg="white")
        tentry.configure(bg="white")
        dentry.configure(bg="white")

        hentry.delete(0, "end")
        mentry.delete(0, "end")
        tentry.delete(0, "end")
        dentry.delete(1.0, "end")

        calendar.selection_set(self.date)
        if(self.hours == "00" and self.ampm == "AM"):
            hentry.insert(0, "12")
        elif(self.ampm == "PM" and int(self.hours) > 12):     # Might need
            hentry.insert(0, (str(int(self.hours) - 12)))
        else:
            hentry.insert(0, self.hours)
        mentry.insert(0, self.min)
        drop.set(self.ampm)
        tentry.insert(0, self.title)
        dentry.insert(1.0, self.desc)