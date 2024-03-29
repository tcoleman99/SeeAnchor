from cgitb import text
import enum
from pydoc import describe
import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
from tkinter.ttk import Style
from tkinter import CENTER, E, N, NE, NW, TOP, W
from functools import partial
from plyer import notification
from datetime import datetime
from datetime import date
import random
from tkinter.messagebox import askyesno
from tkinter import *
from tkcalendar import Calendar
import custom_button
import reminder
from ttkthemes import ThemedStyle
import os

class Dock(object):

    def __init__(self):

        # Creating dock widget
        self.root = tk.Tk()
        self.notificationBubble = tk.Toplevel(self.root)
        self.notepads = []
        self.reminders = []

        self.note_button_list = []
        self.remind_button_list = []

        self.note_count = 0
        self.reminder_count = 0
        self.expired_count = 0
        self.editable = False

        self.primaryColor = ""
        self.secondaryColor = "SkyBlue1"
        self.font = "Forte"

        # Checking to see if initial directories exist, if not creates them for storing note and reminder details
        self.notes_path = "C:\See Anchor\\Notes\\"
        self.reminders_path = "C:\See Anchor\\Reminders\\"
        try:
            os.mkdir(self.notes_path)
            os.mkdir(self.reminders_path)
        except:
            pass

        # Getting screen size
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Original GUI size is 325x500
        self.w = 325
        self.h = 500

        style = ThemedStyle(self.root)
        style.set_theme("breeze")

        # Setting position of GUI on start up (subtract 40 for the taskbar)
        self.x = self.screen_width - self.w
        self.y = self.screen_height - self.h - 40

        # For getting size of current window?
        self.root.update_idletasks()

        # Setting up frames for root window, title, buttons, and notepad list
        self.root.overrideredirect(True)
        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        self.root.configure(bg=self.secondaryColor)
        self.root.resizable(width=False, height=False)

        self.titleFrame = tk.Frame(self.root, width=325, height=25)
        self.titleFrame.pack_propagate(False)
        self.titleFrame.columnconfigure(0, weight=1)
        self.titleFrame.columnconfigure(1, weight=3)
        self.titleFrame.columnconfigure(2, weight=1)

        self.rootFrame = tk.Frame(self.root, width=315, height=465, bg=self.secondaryColor)
        self.rootFrame.pack_propagate(False)

        self.navigationFrame = tk.Frame(self.rootFrame, width=315, height=25, bg="gray39")
        self.navigationFrame.columnconfigure(0, weight=2)
        self.navigationFrame.columnconfigure(1, weight=2)
        self.navigationFrame.columnconfigure(2, weight=2)

        self.border_frame = tk.Frame(self.rootFrame, width=315, height=50, bg=self.secondaryColor)
        self.border_frame.pack_propagate(False)

        self.buttonFrame = tk.Frame(self.border_frame, width=316, height=38, bg="gray39")
        self.buttonFrame.grid_propagate(False)
        self.buttonFrame.columnconfigure(0, weight=2)
        self.buttonFrame.columnconfigure(1, weight=2)
        self.buttonFrame.columnconfigure(2, weight=2)

        self.testlabel = tk.Label(self.navigationFrame, width=15, text="NOTES", bg="gray39", fg="white", font=(self.font, "21", "underline"))

        # Creating scrollable canvas for note buttons to reside on

        self.reminderFrame = tk.Frame(self.rootFrame, width=315, height=500, bg="gray39")
        self.reminderFrame.grid_propagate(False)
        self.reminderFrame.columnconfigure(0, weight=1)
        self.reminderFrame.columnconfigure(1, weight=1)
        self.reminderFrame.columnconfigure(2, weight=1)

        self.reminderList = tk.Frame(self.rootFrame, width=315, height=500)

        self.RL_buttons = tk.Frame(self.border_frame, width=315, height=38, bg="turquoise1")
        self.RL_buttons.pack_propagate(False)

        self.folderFrame = tk.Frame(self.rootFrame, bg="gray39")
        self.canvas = tk.Canvas(self.folderFrame, width=294, height=370, bg="gray39")
        scrollbar = ttk.Scrollbar(self.folderFrame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, width=265, height=365, bg="gray39")
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.bind("<Enter>", self.mousewheel_bound)
        self.scrollable_frame.bind("<Leave>", self.mousewheel_unbound)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.RL_main = tk.Frame(self.reminderList, bg="gray39")
        self.RL_canvas = tk.Canvas(self.RL_main, width=294, height=370, bg="gray39")
        RL_scrollbar = ttk.Scrollbar(self.RL_main, orient="vertical", command=self.RL_canvas.yview)
        self.RL_scrollable_frame = tk.Frame(self.RL_canvas, width=265, height=365, bg="gray39")
        self.RL_scrollable_frame.columnconfigure(0, weight=1)
        self.RL_scrollable_frame.bind("<Enter>", self.mousewheel_bound)
        self.RL_scrollable_frame.bind("<Leave>", self.mousewheel_unbound)
        self.RL_scrollable_frame.bind("<Configure>", lambda e: self.RL_canvas.configure(scrollregion=self.RL_canvas.bbox("all")))
        self.RL_canvas.create_window((0, 0), window=self.RL_scrollable_frame, anchor="nw")
        self.RL_canvas.configure(yscrollcommand=RL_scrollbar.set)

        self.no_note_cover = tk.Label(self.canvas, text="You have no notes", width=36, height=23, bg="gray39", fg="white", font=self.font)

        # Packing Dock (in order from top to bottom)
        self.titleFrame.pack(side=tk.TOP)
        self.rootFrame.pack(pady=(5,0))
        self.navigationFrame.pack()
        self.border_frame.pack()
        self.testlabel.grid(column=1, row=0, sticky=N, pady=(2,0))
        self.buttonFrame.place(anchor="c", relx=.5, rely=.5)
        self.folderFrame.pack() # padx=(20, 20)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.no_note_cover.pack()
        scrollbar.pack(side="right", fill="y")

        self.RL_main.pack() # padx=(20, 20)
        self.RL_canvas.pack(side="left", fill="both", expand=True)
        RL_scrollbar.pack(side="right", fill="y")

        # Button creation
        minimize = tk.Button(self.titleFrame, text="\/", width=31, command=lambda: self.min_but(), bg="medium spring green", relief="flat")
        minimize.pack(side=tk.TOP)

        close = tk.Button(self.titleFrame, text="X", width=6, bg="firebrick1", command=lambda: self.close_help(), relief="flat")
        close.place(x=273)

        settingsBut = tk.Button(self.titleFrame, text="O", width=6, bg="turquoise1", command=lambda: self.testfun(), relief="flat")
        settingsBut.place(x=0)

        self.maximize = custom_button.custom_button(self.root, text="/\\",command=lambda: self.max_but(), bg="medium spring green", relief="flat")
        self.maximize.menu.add_command(label="Color", command=partial(self.maximize.change_color, self.maximize, self.notepads))
        self.maximize.menu.add_command(label="Font Color", command=partial(self.maximize.font_color, self.maximize, self.notepads))
        self.maximize.menu.add_separator()
        self.maximize.menu.add_command(label="Unlock", command=partial(self.maximize.anchor_unlock, self.maximize, self.root, self.maximize.x_location, self.notepads, self.notificationBubble))
        self.maximize.bind("<Button-3>", self.maximize.color_popup)

        newNote = tk.Button(self.buttonFrame, text="+", width=5, command=lambda: self.new_note(self.note_count), font=self.font)
        newNote.grid(column=1, row=0, sticky=W, pady=(5,0))

        self.right = tk.Button(self.navigationFrame, text=">", width=1, height=2, command=lambda: self.arrow_right(), font=self.font)
        self.right.grid(column=2, row=0, sticky=E, padx=(0, 18))

        self.left = tk.Button(self.navigationFrame, text="<", width=1, height=2, command=lambda: self.arrow_left(), font=self.font)
        self.left.grid(column=0, row=0, sticky=W, padx=(17, 0))
        self.left["state"] = DISABLED

        edit = tk.Button(self.buttonFrame, text="Edit", width=5, command=lambda: self.set_editable(edit), font=self.font)
        edit.grid(column=1, row=0, sticky=E, pady=(5,0))

        calendarFrame = tk.Frame(self.reminderFrame, width=315, height=200)
        calendarFrame.pack_propagate(False)
        calendarFrame.pack()

        reminderDetails = tk.Frame(self.reminderFrame, width=315, height=170, bg="gray39")
        reminderDetails.pack_propagate(False)
        reminderDetails.pack()

        self.selected_reminder = None

        self.cal = Calendar(calendarFrame, date_pattern="MM/dd/yyyy", selectmode='day', width=20, height=20, year=date.today().year, month=date.today().month, day=date.today().day)
        self.cal.pack(fill="both", expand=True)

        timelabel = tk.Label(reminderDetails, text="TIME:", bg="gray39", font=(self.font, "16"))
        timelabel.place(x=50, y=2)

        self.hour_text = StringVar()
        self.minute_text = StringVar()

        self.hours = tk.Entry(reminderDetails, width=2, font=("Times 16"), textvariable=self.hour_text)
        self.hours.bind("<FocusIn>", self.entry_clear)
        self.hours.bind("<FocusOut>", self.hour_check)
        self.hours.place(x=115, y=3)

        colon = tk.Label(reminderDetails, text=":", bg="gray39", font=("Times 16"))
        colon.place(x=142, y=2)

        self.minutes = tk.Entry(reminderDetails, width=2, font=("Times 16"), textvariable=self.minute_text)
        self.minutes.bind("<FocusIn>", self.entry_clear)
        self.minutes.bind("<FocusOut>", self.minute_check)
        self.minutes.place(x=155, y=3)

        hour_options = ["","AM", "PM"]
        self.clicker = StringVar()
        self.clicker.set("AM")

        self.hour_text.trace("w", lambda *args: self.charLimit(self.hour_text))
        self.minute_text.trace("w", lambda *args: self.charLimit(self.minute_text))

        self.drop = ttk.OptionMenu(reminderDetails, self.clicker, *hour_options)
        self.drop.place(x=195, y=0)

        self.new_reminder = tk.Button(self.RL_buttons, text="New Reminder", width=10, height=1, command=lambda: self.define_reminder())
        self.new_reminder.pack()

        back = tk.Button(self.RL_buttons, text="<-", width=3, height=2, command=lambda: self.goback())
        back.place(x=0, y=0)

        self.reminder_confirm = tk.Button(reminderDetails, text="Create Reminder", width=32, height=1, command=lambda: self.create_reminder())
    
        self.edit_reminder = tk.Button(reminderDetails, text="Confirm Changes", width=20, height=1, command=lambda: self.update_reminder(), font="Times 8")

        self.delete_reminder_button = tk.Button(reminderDetails, text="Delete", width=20, height=1, command=lambda: self.delete_reminder(), font="Times 8")

        self.title = tk.Entry(reminderDetails, width=37, font="Times 11", bg="white", fg="gray79")
        self.title.bind("<FocusIn>", self.title_placeholder)
        self.title.bind("<FocusOut>", self.title_place_reinsert)
        self.title.place(x=25, y=35)

        self.description = tk.Text(reminderDetails, width=37, height=3, font="Times 11", bg="white", fg="gray79")
        self.description.bind("<FocusIn>", self.desc_placeholder)
        self.description.bind("<FocusOut>", self.desc_place_insert)
        self.description.place(x=25, y=65)

        self.t1 = tk.Label(self.RL_canvas, text="You have no Reminders", width=36, height=23, bg="gray39", fg="white", font=self.font)
        self.t1.pack()

        dir = os.listdir(self.notes_path)
        self.note_order = []
        if(len(dir) == 0):
            print("Notes folder empty")
        else:
            self.no_note_cover.pack_forget()
            count = 0
            for filename in dir:
                for x in range(len(dir)):
                    f = open(self.notes_path + filename, 'r')
                    Lines = f.readlines()
                    if(int(Lines[0].rstrip('\n')) == x):
                        self.note_order.append(Lines[3].rstrip('\n'))
                    else:
                        pass
                    f.close()
                with open(os.path.join(self.notes_path, filename), 'r'):
                    self.read_note(self.notes_path + filename, count)
                    count += 1
        dir = os.listdir(self.reminders_path)
        if(len(dir) == 0):
            print("Reminders folder empty")
        else:
            count = 0
            for filename in dir:
                with open(os.path.join(self.reminders_path, filename), 'r'):
                    self.read_reminder(self.reminders_path + filename)
                    count += 1

        # Bubble for notifications when reminders expire
        self.notificationBubble.overrideredirect(True)
        self.notificationBubble.attributes("-topmost", True)
        self.notificationBubble.geometry('%dx%d+%d+%d' % (20, 20, (self.maximize.x_location - 20), (self.screen_height - 85)))
        self.notificationBubble.configure(bg="red")
        self.notificationBubble.withdraw()
        self.expire_count = 0
        self.expire_count_num = Label(self.notificationBubble, text=self.expire_count, bg="red", fg="white")
        self.expire_count_num.pack()

        # Sets the app to always be in foreground and runs
        self.root.attributes("-topmost", True)
        self.root.update()
        self.root.mainloop()

    # ============================FUNCTIONS=============================
    # **************************
    # *       NAVIGATION       *
    # **************************

    # Arrow right and left functions are for switching between reminder and note views
    def arrow_right(self):
        self.testlabel.configure(text="REMINDERS")
        self.buttonFrame.place_forget()
        self.folderFrame.pack_forget()
        self.RL_buttons.place(anchor="c", relx=.5, rely=.5)
        self.reminderList.pack()
        self.right["state"] = DISABLED
        self.left["state"] = NORMAL

    def arrow_left(self):
        self.testlabel.configure(text="NOTES")
        self.reminderList.pack_forget()
        self.RL_buttons.place_forget()
        self.reminderFrame.pack_forget()
        self.buttonFrame.place(anchor="c", relx=.5, rely=.5)
        self.folderFrame.pack()
        self.left["state"] = DISABLED
        self.right["state"] = NORMAL

    # Minimize Dock to a small button above the taskbar
    def min_but(self):
        # self.root.geometry('%dx%d+%d+%d' % (self.screen_width - self.maximize.winfo_x(), 25, self.maximize.winfo_x(), (self.screen_height - 65)))
        self.root.configure(bg="#add123")
        self.maximize.place(x=self.maximize.x_location, y=0, width=27)
        self.root.geometry('%dx%d+%d+%d' % (self.screen_width - self.maximize.x_location, 25, self.maximize.x_location, (self.screen_height - 65)))
        self.maximize.place(x=0)

        # Everytime minimize button is pressed the number of expired reminders is updated
        for x in self.reminders:
            if(x.expired == True):
                self.expire_count = self.expire_count + 1
        print(self.expire_count)
        self.expire_count_num.config(text=str(self.expire_count))
        self.notificationBubble.deiconify()

        self.root.wm_attributes("-transparentcolor", "#add123")
        self.root.overrideredirect(True)
        self.titleFrame.pack_forget()
        self.rootFrame.pack_forget()
        if(self.testlabel.cget("text") == "NOTES"):
            self.folderFrame.pack_forget()
        elif(self.testlabel.cget("text") == "REMINDERS"):
            self.reminderFrame.pack_forget()
        for x in self.notepads:
            x.closeOverride()  
        self.root.update_idletasks()

    # Maximize Dock to view notes and reminders
    def max_but(self):
        self.expire_count = 0
        self.root.overrideredirect(True)
        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        self.root.configure(bg=self.secondaryColor)
        self.notificationBubble.withdraw()
        self.maximize.place_forget()
        self.titleFrame.pack(side="top")
        self.rootFrame.pack(pady=(5,0))
        if(self.testlabel.cget("text") == "NOTES"):
            self.border_frame.pack()
            self.folderFrame.pack()
        elif(self.testlabel.cget("text") == "REMINDERS"):
            self.RL_buttons.place(anchor="c", relx=.5, rely=.5)
            self.RL_main.pack()
            self.reminderList.pack()
        self.root.update_idletasks()

    # Saves and destroys all notes when closing dock
    def close_help(self):
        for notepad in self.notepads:
            notepad.top.destroy()
        self.notepads.clear()
        self.note_button_list.clear()
        self.root.destroy()

    # **************************
    # *         NOTES          *
    # **************************

    # Create a new note, makes new entries in lists, makes button draggable if edit is enabled
    def new_note(self, index):   # Have to pass self.note_count as index or else self.notepads[self.note_count] does not accept input
        if(len(self.notepads) == 0):
            self.no_note_cover.pack_forget()
        from notepad import Notepad
        self.notepads.append(Notepad(self, self.note_count))
        self.notepads[index].closeOverride()
        self.notepadButton = custom_button.custom_button(self.scrollable_frame, text="Title %d" % (index), width=32, command=lambda: [self.notepads[index].openOverride()], relief="flat", font=(self.font, "12"))
        self.notepadButton.menu.add_command(label="Color", command=partial(self.notepadButton.change_color, self.notepadButton, self.notepads))
        self.notepadButton.menu.add_command(label="Font Color", command=partial(self.notepadButton.font_color, self.notepadButton, self.notepads))
        self.notepadButton.menu.add_separator()
        self.notepadButton.menu.add_command(label="Delete", command=partial(self.delete_note, self.notepadButton))
        self.notepadButton.grid(column=0, columnspan=2, row=self.note_count, sticky=tk.N+tk.S+tk.E+tk.W, pady=(0, 10))
        self.notepadButton.bind("<Button-3>", self.notepadButton.color_popup)
        self.notepads[index].set_button(self.notepadButton)
        self.note_button_list.append(self.notepadButton)
        self.note_count += 1

        f = open(self.notepads[index].filename, 'w')
        f.close()
        self.notepads[index].saveFile()

        if(self.editable == True):
            for note in self.note_button_list:
                if(note.selected == True):
                    selectedBut = note  # Using note seems to only use the last index in list instead of note with selected == True
                    self.notepadButton.configure(command=lambda: self.swap(selectedBut, self.notepadButton))

    # For when the application is first ran, checks for existing notes and adds them back to the dock with their details and position
    def read_note(self, file, index):
        from notepad import Notepad
        f = open(file, 'r')
        Lines = f.readlines()
        self.notepads.append(Notepad(self, self.note_count))
        self.notepads[index].button_row = int(Lines[0].rstrip('\n'))
        self.notepads[index].titleLabel.configure(bg=Lines[1].rstrip('\n'))
        self.notepads[index].titleLabel.configure(fg=Lines[2].rstrip('\n'))
        self.notepads[index].titleLabel.configure(text=Lines[3].rstrip('\n'))
        for x in Lines[4:]:
            self.notepads[index].notepad.insert(INSERT, x)
        f.close()
        self.notepadButton = custom_button.custom_button(self.scrollable_frame, text=self.notepads[index].titleLabel.cget("text"), width=32, command=lambda: [self.notepads[index].openOverride()], relief="flat", font=(self.font, "12"), bg=self.notepads[index].titleLabel.cget("bg"), fg=self.notepads[index].titleLabel.cget("fg"))
        self.note_button_list.append(self.notepadButton)
        self.notepadButton.menu.add_command(label="Color", command=partial(self.notepadButton.change_color, self.notepadButton, self.notepads))
        self.notepadButton.menu.add_command(label="Font Color", command=partial(self.notepadButton.font_color, self.notepadButton, self.notepads))
        self.notepadButton.menu.add_separator()
        self.notepadButton.menu.add_command(label="Delete", command=partial(self.delete_note, self.notepadButton))
        self.notepadButton.bind("<Button-3>", self.notepadButton.color_popup)
        self.notepadButton.grid(column=0, columnspan=2, row=self.notepads[index].button_row, sticky=tk.N+tk.S+tk.E+tk.W, pady=(0, 10))
        self.notepads[index].set_button(self.notepadButton)
        self.notepads[index].titleLabel.configure(bg=self.notepads[index].corresponding_button.cget("bg"))
        self.note_count += 1
        self.notepads[index].closeOverride()

    # Deletes note and removes txt file with note details
    def delete_note(self, button):
        answer = askyesno(title="Confirm", message="Are you sure you want to delete this note? You will not be able to revert this decision.")
        if answer:
            path = self.notes_path + button.cget("text") + ".txt"
            os.remove(path)
            self.note_count -= 1
            self.toDelete = None
            button.grid_forget()
            for l in range(len(self.note_button_list)):
                if(self.note_button_list[l] == button):
                    self.toDelete = l
                    break
            del self.note_button_list[self.toDelete]
            del self.notepads[self.toDelete]
            for x in self.notepads[self.toDelete:]:
                x.titleLabel.row -= 1
                # subtract 1 from row number in text file
            for i in self.note_button_list[self.toDelete:]:
                i.grid(row=i.grid_info()["row"] - 1)
                i.configure(command=lambda idx=self.toDelete: self.notepads[idx].openOverride())
                print(i.grid_info()["row"])
                self.toDelete += 1
            for x in self.notepads:
                x.saveFile()
        if(len(self.notepads) == 0):
            self.no_note_cover.pack()
            self.root.update()

    # For editing positions of notes in list on dock
    def set_editable(self, button):
        if(len(self.note_button_list) > 0 and self.editable == False):
            button.configure(bg="Lime Green")
            for i in range(len(self.note_button_list)):
                self.note_button_list[i].configure(command=lambda idx=i: self.first_selection(self.note_button_list[idx]))
            self.editable = True
        elif(len(self.note_button_list) > 0 and self.editable == True):
            button.configure(bg="White")
            for i in range(len(self.note_button_list)):
                if(self.note_button_list[i].selected == True):
                    self.note_button_list[i].selected = False
                self.note_button_list[i].configure(command=lambda idx=i: self.notepads[idx].openOverride())
            self.editable = False
        else:
            self.editable = False

    # First selection for swapping note position
    def first_selection(self, target1):
        target1.selected = True
        for i in range(len(self.note_button_list)):
            self.note_button_list[i].configure(command=lambda idx=i: self.swap(target1, self.note_button_list[idx]))
        while(target1.selected == True):
            self.root.update()
            self.root.after(600, target1.configure(bg="royal blue"))
            self.root.update()
            self.root.after(700, target1.configure(bg=target1.bgcolor))
            self.root.update()

    # Swaps two note positions
    def swap(self, target1, target2):
        target1.selected = False
        secondOriginalColor = target2.cget("bg")
        row1 = target1.grid_info()["row"]
        row2 = target2.grid_info()["row"]
        target1.grid(row=row2)
        target1.configure(bg=target1.bgcolor)
        target1.selected = False
        target2.grid(row=row1)
        target2.configure(bg=secondOriginalColor)
        target2.selected = False
        for i in range(len(self.note_button_list)):
            self.note_button_list[i].configure(command=lambda idx=i: self.first_selection(self.note_button_list[idx]))

    # Next three functions are for capturing the whole window for scrollbar of note and reminder lists
    def mousewheel_bound(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def mousewheel_unbound(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # *******************************
    # *          REMINDERS          *
    # *******************************

    # For creating a new reminder, reminder set up page is displayed.
    def define_reminder(self):
        self.reminderList.pack_forget()
        self.hours.delete(0, "end")
        self.minutes.delete(0, "end")
        self.clicker.set("AM")
        self.cal.selection_set(datetime.now())

        self.title.delete(0, "end")
        self.title.configure(fg="gray79")
        self.title.insert(0, "Title...")

        self.description.delete(1.0, "end")
        self.description.configure(fg="gray79")
        self.description.insert(1.0, "Description...")

        self.hours.configure(bg="white")
        self.minutes.configure(bg="white")
        self.title.configure(bg="white")

        self.edit_reminder.place_forget()
        self.delete_reminder_button.place_forget()
        self.reminder_confirm.place(x=25, y=135)
        self.reminderFrame.pack()
        self.reminderFrame.configure(bg="gray39")
        self.hours.focus_set()

    # Creates a new reminder and a new button for each reminder for viewing reminder details
    def create_reminder(self):
        if(len(self.reminders) == 0):
            self.t1.pack_forget()

        proceed = self.entry_check()
        if(proceed == False):
            pass
        else:
            self.reminderFrame.pack_forget()
            self.reminderList.pack()
            uniqueID = random.randint(1000, 9999)
            roach = reminder.Reminder(self, uniqueID, False, self.hours.get(), self.minutes.get(), self.clicker.get(), self.cal.get_date(), self.title.get(), self.description.get(1.0, "end-1c"), self.reminder_count)
            self.reminders.append(roach)
            self.reminderFrame.configure(bg="gray39")
            if(len(self.reminders[self.reminder_count].title) > 15):
                tempTitle = self.reminders[self.reminder_count].title[0:15] + "..."
            else:
                tempTitle = self.reminders[self.reminder_count].title
            button_text = tempTitle + " -- " + self.reminders[self.reminder_count].date + " - " + str(self.reminders[self.reminder_count].displayhours) + ":" + str(self.reminders[self.reminder_count].min) + " " + self.reminders[self.reminder_count].ampm

            if(roach.expired == False):
                self.reminderButton = custom_button.custom_button(self.RL_scrollable_frame, text=button_text, width=36, command=lambda: self.open_reminder(roach), bg="seagreen1")
            else:
                self.reminderButton = custom_button.custom_button(self.RL_scrollable_frame, text=button_text, width=36, command=lambda: self.open_reminder(roach), bg="tomato")
            
            self.reminderButton.grid(column=0, columnspan=2, row=self.reminder_count, sticky=tk.N+tk.S+tk.E+tk.W, pady=(0, 10))
            self.remind_button_list.append(self.reminderButton)
            roach.saveToFile()
            self.reminder_count += 1
    
    # For opening a reminder and filling in related details to that reminder
    def open_reminder(self, reminder):
        self.selected_reminder = reminder.row
        self.reminderList.pack_forget()
        self.reminderFrame.pack()
        self.reminder_confirm.place_forget()

        self.edit_reminder.place(x=25, y=135)
        self.delete_reminder_button.place(x=160, y=135)

        if(self.reminders[self.selected_reminder].title == "Title..."):
            self.title.configure(fg="gray79")
        else:
            self.title.configure(fg="black")
        if(self.reminders[self.selected_reminder].desc == "Description..."):
            self.description.configure(fg="gray79")
        else:
            self.description.configure(fg="black")

        reminder.open(self.cal, self.hours, self.minutes, self.clicker, self.title, self.description)
        self.cal.focus_set()

    # Updates reminder with any changes made. Stops old thread and starts new with updated values
    def update_reminder(self):
        proceed = self.entry_check()
        if(proceed == True):
            self.reminderFrame.pack_forget()
            self.reminderList.pack()
            self.reminders[self.selected_reminder].date = self.cal.get_date()
            self.reminders[self.selected_reminder].hours = self.hours.get()
            self.reminders[self.selected_reminder].min = self.minutes.get()
            self.reminders[self.selected_reminder].ampm = self.clicker.get()
            if(self.reminders[self.selected_reminder].title != self.title.get()):
                os.remove(self.reminders_path + self.reminders[self.selected_reminder].title + "_" + str(self.reminders[self.selected_reminder].uniqueID) + ".txt")
            self.reminders[self.selected_reminder].title = self.title.get()
            self.reminders[self.selected_reminder].desc = self.description.get(1.0, "end-1c")
            self.reminders[self.selected_reminder].displayhours = self.hours.get()

            if(len(self.reminders[self.selected_reminder].title) > 15):
                    tempTitle = self.reminders[self.selected_reminder].title[0:15] + "..."
            else:
                    tempTitle = self.reminders[self.selected_reminder].title
            
            buttonText = tempTitle + " -- " + self.reminders[self.selected_reminder].date + " - " + str(self.reminders[self.selected_reminder].displayhours) + ":" + str(self.reminders[self.selected_reminder].min) + " " + self.reminders[self.selected_reminder].ampm
            self.remind_button_list[self.selected_reminder].configure(text=buttonText)
            self.remind_button_list[self.selected_reminder].configure(bg="seagreen1")
            self.reminders[self.selected_reminder].check_expire()
            if(self.reminders[self.selected_reminder].expired == True):
                self.remind_button_list[self.selected_reminder].configure(bg="tomato")
            else:
                self.remind_button_list[self.selected_reminder].configure(bg="seagreen1")
            self.reminders[self.selected_reminder].update()
            self.reminders[self.selected_reminder].saveToFile()
        else:
            pass

    # Stopping thread and deleting reminder
    def delete_reminder(self):
        self.reminderFrame.pack_forget()

        # Delete reminder file
        path = self.reminders_path + self.reminders[self.selected_reminder].title + "_" + str(self.reminders[self.selected_reminder].uniqueID) + ".txt"
        os.remove(path)

        # Stops running thread
        self.reminders[self.selected_reminder].expired = True
        self.reminders[self.selected_reminder].update()

        if(self.selected_reminder == self.reminder_count - 1):
            self.remind_button_list[self.selected_reminder].grid_forget()
        else:
            for x in self.remind_button_list[(self.selected_reminder + 1):]:
                x.grid(row = x.grid_info()["row"] - 1)
                self.remind_button_list[self.selected_reminder].grid_forget()
            for i in self.reminders[self.selected_reminder:]:
                i.row -= 1

        self.reminder_count -= 1
        del self.reminders[self.selected_reminder]
        del self.remind_button_list[self.selected_reminder]
        self.reminderList.pack()
        if(len(self.reminders) == 0):
            self.t1.pack()

        self.root.update()

    def read_reminder(self, file):
        f = open(file, 'r')
        Lines = f.readlines()
        f.close()

        # Compare date in file to current date to determine if reminder expired
        current_date = date.today()
        current_date.strftime("%m/%d/%Y")
        reminder_date = datetime.strptime(Lines[5].rstrip('\n'), "%m/%d/%Y").date()
        current_time = datetime.now().strftime("%H:%M")
        reminder_time = Lines[1].rstrip('\n') + ":" + Lines[2].rstrip('\n')
        self.expired_bool = None

        if((current_date > reminder_date)):
            self.expired_bool = True
        elif((current_date == reminder_date) and (current_time >= reminder_time)):
            self.expired_bool = True
        else:
            self.expired_bool = False

        # Gets multi-line description and combines the list items into single string
        description_string = ""
        for i in Lines[7:]:
            description_string = description_string + str(i)
        
        roach = reminder.Reminder(self, Lines[0].rstrip('\n'), self.expired_bool, Lines[2].rstrip('\n'), Lines[3].rstrip('\n'), Lines[4].rstrip('\n'), Lines[5].rstrip('\n'), Lines[6].rstrip('\n'), description_string.rstrip('\n'), self.reminder_count)
        self.reminders.append(roach)

        self.reminderFrame.configure(bg="gray39")
        self.t1.pack_forget()

        if(len(self.reminders[self.reminder_count].title) > 15):
            tempTitle = self.reminders[self.reminder_count].title[0:15] + "..."
        else:
            tempTitle = self.reminders[self.reminder_count].title

        button_text = tempTitle + " -- " + self.reminders[self.reminder_count].date + " - " + str(self.reminders[self.reminder_count].displayhours) + ":" + str(self.reminders[self.reminder_count].min) + " " + self.reminders[self.reminder_count].ampm
        if(roach.expired == False):
            self.reminderButton = custom_button.custom_button(self.RL_scrollable_frame, text=button_text, width=36, command=lambda: self.open_reminder(roach), bg="seagreen1")
        else:
            self.reminderButton = custom_button.custom_button(self.RL_scrollable_frame, text=button_text, width=36, command=lambda: self.open_reminder(roach), bg="tomato")

        self.reminderButton.grid(column=0, columnspan=2, row=self.reminder_count, sticky=tk.N+tk.S+tk.E+tk.W, pady=(0, 10))
        self.remind_button_list.append(self.reminderButton)
        roach.saveToFile()
        self.reminder_count += 1

    # When the cursor enters an entry for a reminder it clears the existing text and sets bckgrnd color to white
    def entry_clear(self, e):
        e.widget.delete(0, "end")
        e.widget.configure(bg="white")

    # Checks for valid input for reminder details
    def entry_check(self):
        total = 0
        if(len(self.hours.get()) == 0 or int(self.hours.get()) > 23):
            self.hours.configure(bg="salmon")
            total += 1
        if(len(self.minutes.get()) < 2 or int(self.minutes.get()) > 59):
            self.minutes.configure(bg="salmon")
            total += 1
        if(self.title.get() == "Title..." or len(self.title.get()) == 0):
            self.title.configure(bg="salmon")
            total += 1
        if(total == 0):
            return True
        else:
            return False

    # Hour and minute checks are functions for only checking that specific entry for reminders
    def hour_check(self, e):
        if(not(len(self.hours.get()) == 0 or 0 < int(self.hours.get()) < 24)):
            self.hours.configure(bg="salmon")

    def minute_check(self, e):
        if(not(len(self.minutes.get()) == 0 or 0 <= int(self.minutes.get()) < 60)):
            self.minutes.configure(bg="salmon")

    # Sets hour and minute entries to only allow integers to be entered and a max character count of 2 for each entry
    def charLimit(self, text):
        if(text.get().isdigit() == False):
            text.set(text.get()[:-1])

        if(len(text.get()) > 2 ):
            text.set(text.get()[-1])
            text.set(text.get()[0:2])

        focused_entry = self.root.focus_get()
        if((self.root.focus_get() == focused_entry) and len(text.get()) == 2):
            self.minutes.focus()
        
        if((self.root.focus_get() == focused_entry) and (len(text.get()) == 2)):
            self.drop.focus()

    # Back out of the reminder creation screen to the reminder list
    def goback(self):
        self.reminderFrame.pack_forget()
        self.reminderList.pack()

    # The following functions are for inputting placeholders for the title and description entries.
    # When the cursor enters either entry, the placeholder is removed for input. These placeholders
    # are for the user to know which entry is which.
    def title_placeholder(self, e):
        if(self.title.get() == "Title..."):
            self.title.delete(0, "end")
            self.title.configure(bg="white", fg="black")

    def title_place_reinsert(self, e):
        if(self.title.get() == ""):
            self.title.configure(fg="gray79")
            self.title.insert(0, "Title...")

    def desc_placeholder(self, e):
        if(self.description.get(1.0, "end-1c") == "Description..."):
            self.description.delete(1.0, "end")
            self.description.configure(fg="black")

    def desc_place_insert(self, e):
        if(self.description.get(1.0, "end-1c") == ""):
            self.description.configure(fg="gray79")
            self.description.insert(1.0, "Description...")