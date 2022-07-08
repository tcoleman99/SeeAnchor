import tkinter as tk
import tkinter.ttk as ttk
from tkinter.colorchooser import askcolor
from tkinter import CENTER, E, N, NE, NW, TOP, W, Menu, Toplevel
from tkinter.scrolledtext import ScrolledText
import random
from functools import partial
from plyer import notification
from datetime import datetime

class Dock(object):

    def __init__(self):

        # Creating dock widget
        self.root = tk.Tk()
        self.notepads = []
        self.button_list = []
        self.count = 0
        self.editable = False

        # Getting screen size
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Original GUI size is 325x500
        self.w = 325
        self.h = 500

        # Setting position of GUI on start up (subtract 40 for the taskbar)
        self.x = self.screen_width - self.w
        self.y = self.screen_height - self.h - 40

        # For getting size of current window?
        self.root.update_idletasks()

        # Setting up frames for root window, title, buttons, and notepad list
        self.root.overrideredirect(True)
        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        self.root.configure(bg="gray36")
        self.root.resizable(width=False, height=False)

        self.titleFrame = tk.Frame(self.root, width=325, height=25, bg="gray36")
        self.titleFrame.pack_propagate(False)
        self.titleFrame.pack(side=tk.TOP)
        self.titleFrame.columnconfigure(0, weight=1)
        self.titleFrame.columnconfigure(1, weight=3)
        self.titleFrame.columnconfigure(2, weight=1)

        self.buttonFrame = tk.Frame(self.root, width=325, height=55, bg="grey36")
        self.buttonFrame.grid_propagate(False)
        self.buttonFrame.pack()
        self.buttonFrame.columnconfigure(0, weight=2)
        self.buttonFrame.columnconfigure(1, weight=2)
        self.buttonFrame.columnconfigure(2, weight=2)

        # Creating scrollable canvas for note buttons to reside on
        self.folderFrame = tk.Frame(self.root, width=280, height=400, bg="grey69")
        self.canvas = tk.Canvas(self.folderFrame, width=269, height=365, bg="grey69")
        # self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        scrollbar = ttk.Scrollbar(self.folderFrame, orient="vertical", command=self.canvas.yview, )
        self.scrollable_frame = tk.Frame(self.canvas, width=265, height=365, bg="grey69")
        self.scrollable_frame.columnconfigure(0, weight=1)

        self.scrollable_frame.bind("<Enter>", self.mousewheel_bound)
        self.scrollable_frame.bind("<Leave>", self.mousewheel_unbound)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.folderFrame.pack() # padx=(20, 20)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Button creation
        minimize = tk.Button(self.titleFrame, text="\/", width=31, command=lambda: self.min_but(), bg="medium spring green", relief="flat")
        minimize.pack(side=tk.TOP)

        close = tk.Button(self.titleFrame, text="X", width=6, bg="firebrick1", command=lambda: self.close_help(), relief="flat")
        close.place(x=273)

        settingsBut = tk.Button(self.titleFrame, text="O", width=6, bg="turquoise1", command=lambda: self.testfun(), relief="flat")
        settingsBut.place(x=0)

        self.maximize = custom_button(self.root, text="/\\",command=lambda: self.max_but(), bg="medium spring green", relief="flat")
        self.maximize.menu.add_command(label="Color", command=partial(self.maximize.change_color, self.maximize))
        self.maximize.menu.add_command(label="Font Color", command=partial(self.maximize.font_color, self.maximize))
        self.maximize.menu.add_separator()
        self.maximize.menu.add_command(label="Unlock", command=partial(self.maximize.anchor_unlock, self.maximize, self.root, self.maximize.x_location))
        self.maximize.bind("<Button-3>", self.maximize.color_popup)

        newNote = tk.Button(self.buttonFrame, text="+", width=5, command=lambda: self.new_note(self.count), relief="flat")
        newNote.grid(column=1, row=0, sticky=W, pady=(15,0))

        delNote = tk.Button(self.buttonFrame, text="Trash", width=5, command=lambda: self.delete_note(), relief="flat")
        delNote.grid(column=1, row=0, sticky=N, pady=(15, 0))

        edit = tk.Button(self.buttonFrame, text="Edit", width=5, command=lambda: self.set_editable(edit), relief="flat")
        edit.grid(column=1, row=0, sticky=E, pady=(15,0))

        # self.reminder()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time)
        if(current_time == "15:10:00"):
            self.reminder()


        # Sets the app to always be in foreground and runs
        self.root.attributes("-topmost", True)
        self.root.update()
        self.root.mainloop()
    
    # ============================FUNCTIONS=============================
    # ----------Title Frame-----------
    # Minimize button
    def min_but(self):
        self.root.geometry('%dx%d+%d+%d' % (self.screen_width - self.maximize.winfo_x(), 25, self.maximize.winfo_x(), (self.screen_height - 65)))
        self.root.configure(bg="#add123")
        self.maximize.place(x=self.maximize.x_location, y=0, width=27)
        self.root.geometry('%dx%d+%d+%d' % (self.screen_width - self.maximize.x_location, 25, self.maximize.x_location, (self.screen_height - 65)))
        self.maximize.place(x=0)
        self.root.wm_attributes("-transparentcolor", "#add123")
        self.root.overrideredirect(True)
        self.titleFrame.pack_forget()
        self.buttonFrame.pack_forget()
        self.folderFrame.pack_forget()
        for x in self.notepads:
            x.closeOverride()  
        self.root.update_idletasks()

    # Maximize button
    def max_but(self):
        self.root.overrideredirect(True)
        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        self.root.configure(bg="gray36")
        self.maximize.place_forget()
        self.titleFrame.pack(side="top")
        self.buttonFrame.pack()
        self.folderFrame.pack()
        self.root.update_idletasks()

    # Saves and destroys all notes when closing dock
    def close_help(self):
        for notepad in self.notepads:
            notepad.top.destroy()
        self.notepads.clear()
        self.button_list.clear()
        self.root.destroy()

    # ----------Button Frame----------
    # Create a new note, makes new entries in lists, makes button draggable if edit is enabled
    def new_note(self, index):   # Have to pass self.count as index or else self.notepads[self.count] does not accept input
        self.notepads.append(Notepad(self, self.count))
        self.notepads[index].closeOverride()
        self.notepadButton = custom_button(self.scrollable_frame, text="New label #%d" % (index), width=37, command=lambda: [self.notepads[index].openOverride()], relief="flat")
        self.notepadButton.menu.add_command(label="Background Color", command=partial(self.notepadButton.change_color, self.notepadButton))
        self.notepadButton.menu.add_command(label="Font Color", command=partial(self.notepadButton.font_color, self.notepadButton))
        self.notepadButton.menu.add_separator()
        self.notepadButton.menu.add_command(label="Delete", command=partial(self.delete_note, self.notepadButton))
        self.notepadButton.grid(column=0, columnspan=2, row=self.count+1, sticky=tk.N+tk.S+tk.E+tk.W, pady=(0, 10))
        self.notepadButton.bind("<Button-3>", self.notepadButton.color_popup)
        self.button_list.append(self.notepadButton)
        self.count += 1
        if(self.editable == True):
            for note in self.button_list:
                if(note.selected == True):
                    selectedBut = note  # Using note seems to only use the last index in list instead of note with selected == True
                    self.notepadButton.configure(command=lambda: self.swap(selectedBut, self.notepadButton))

    def delete_note(self, button):
        # win = tk.Toplevel()
        # win.wm_title("Delete Note")
        # warning = tk.Label(win, text="Are you sure you want to delete this note? You will not be able to retrieve this note.", fg="Red")
        # warning.pack(side="top")
        # yesButton = tk.Button(win, text="Yes")
        # yesButton.pack(side="left")
        # noButton = tk.Button(win, text="No")
        # noButton.pack(side="right")
        self.count -= 1
        self.toDelete = None
        button.grid_forget()
        for l in range(len(self.button_list)):
            if(self.button_list[l] == button):
                self.toDelete = l
        del self.button_list[self.toDelete]
        del self.notepads[self.toDelete]
        for x in self.notepads[self.toDelete:]:
            x.titleLabel.row -= 1
        for i in self.button_list[self.toDelete:]:
            i.grid(row=i.grid_info()["row"] - 1)
            i.configure(command=lambda idx=self.toDelete: self.notepads[idx].openOverride())
            self.toDelete += 1
        self.root.update()

    # ----------Edit Note List Order-----------
    # For editing positions of notes in list on dock
    def set_editable(self, button):
        if(len(self.button_list) > 0 and self.editable == False):
            button.configure(bg="Lime Green")
            for i in range(len(self.button_list)):
                self.button_list[i].configure(command=lambda idx=i: self.first_selection(self.button_list[idx]))
            self.editable = True
        elif(len(self.button_list) > 0 and self.editable == True):
            button.configure(bg="White")
            for i in range(len(self.button_list)):
                if(self.button_list[i].selected == True):
                    self.button_list[i].selected = False
                self.button_list[i].configure(command=lambda idx=i: self.notepads[idx].openOverride())
            self.editable = False
        else:
            self.editable = False

    # First selection for swapping note position
    def first_selection(self, target1):
        target1.selected = True
        for i in range(len(self.button_list)):
            self.button_list[i].configure(command=lambda idx=i: self.swap(target1, self.button_list[idx]))
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
        for i in range(len(self.button_list)):
            self.button_list[i].configure(command=lambda idx=i: self.first_selection(self.button_list[idx]))

    # Captures the whole window for scrollbar of note list
    def mousewheel_bound(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def mousewheel_unbound(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def testfun(self):
        for i in self.button_list:
            if(i.selected == True):
                print(i.cget("text") + " is selected")
            else:
                print(i.cget("text") + " is NOT")
        print("---------")
        for i in self.notepads:
            print(i.titleLabel.cget("text"))

    def reminder(self):
        notification.notify(title="Break", message="take a break", timeout=1)

class Notepad(Dock):

    def __init__(self, parent, position):
        # the root widget
        self.top = Toplevel()
        self.starting_x = 1260
        self.starting_y = 600
        self.top.geometry("325x325+%d+%d" % (self.starting_x, self.starting_y))
        self.top.title("Notepad")
        self.top.configure(bg="seashell2")
        self.top.resizable(width=True, height=True)
        self.top.protocol("WM_DELETE_WINDOW", self.closeOverride)
        # self.top.resizable(0,0)
        self.parent = parent

        self.filename = "file_" + str(random.randrange(10000, 50000))

        # Creating label
        self.titleLabel = create_label(self.top, text="Title %d" % (position), bg="light blue", font=("Times 20 italic bold"))
        self.titleLabel.newParent = parent    # To set the main application as the parent of create_label
        self.titleLabel.row = position
        self.titleLabel.pack(side="top", fill="x")

        # Padding text within the main text box (left, top, right, bottom)
        ttk.Style().configure("pad.TEntry", padding="5 1 5 1")

        # Creating scrollable notepad window
        self.notepad = ScrolledText(self.top, font=("Bold", 15), bg="seashell2", relief="flat")
        self.notepad.configure(padx=12)
        self.notepad.pack(padx=1, pady=1)

    def closeOverride(self):
        self.saveFile()
        self.top.withdraw()

    def openOverride(self):
        self.titleLabel.configure(bg=self.parent.button_list[self.titleLabel.row].cget("bg"))
        self.saveFile()
        self.top.deiconify()

    def saveFile(self):
        pass
        # file1 = open(self.filename + ".txt", "w")
        # file1.write(str(self.titleLabel.position) + "\n")
        # file1.write(self.titleLabel.getTitle(self) + "\n")
        # file1.write(self.notepad.get("1.0","end-1c"))
        # file1.close()

class create_label(tk.Label):

    # Creating entry & setting input actions
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.entry = tk.Entry(self, bg="white", justify="center")
        self.bind("<Double-1>", self.edit_start)
        self.entry.bind("<Return>", self.edit_stop)
        self.entry.bind("<FocusOut>", self.edit_stop)
        self.entry.bind("<Escape>", self.edit_cancel)
        self.newParent = None
        self.row = None 

    def edit_start(self, event=None):
        self.entry.place(relx=.5, rely=.5, relwidth=1.0, relheight=1.0, anchor="center")
        self.entry.focus_set()

    def edit_stop(self, event=None):
        self.configure(text=self.entry.get())
        self.entry.place_forget()
        self.newParent.button_list[self.row].configure(text=self.entry.get())

    def edit_cancel(self, event=None):
        self.entry.delete(0, "end")
        self.entry.place_forget()
        self.newParent.button_list[self.row].configure(text=self.entry.get())

class custom_button(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.menu = tk.Menu(self, tearoff=0)

        self.x_location = 1750
        self.locked = True
        self.selected = False
        self.bgcolor = self.cget("bg")
        self.configure(bg=self.bgcolor)


    def change_color(self, button):
        colors = askcolor(title="Background Color")
        self.bgcolor = colors[1]
        button.configure(bg=self.bgcolor)

    def font_color(self, button):
        colors = askcolor(title="Font Color")
        button.configure(fg=colors[1])

    def anchor_unlock(self, button, window, location):
        button.locked = False
        window.geometry('%dx%d+%d+%d' % (window.winfo_screenwidth(), 25, 0, window.winfo_screenheight() - 65))
        button.place(x=location)
        button["state"] = "disabled"
        button.menu.delete("Unlock")
        button.menu.delete("Color")
        button.menu.delete("Font Color")
        button.menu.delete(0)   # Removes the separator line from the right click menu
        button.menu.add_command(label="Lock", command=partial(button.anchor_lock, button, window))
        custom_button.make_draggable(button)

    def anchor_lock(self, button, window):
        button.locked = True
        button.x_location = button.winfo_x()
        tmp_x = button.x_location
        window.geometry("%dx%d+%d+%d" % (window.winfo_screenwidth() - int(button.x_location), 25, int(button.x_location), window.winfo_screenheight() - 65))
        button.place(x=0)
        button["state"] = "normal"
        button.menu.delete("Lock")
        button.menu.add_command(label="Color", command=partial(button.change_color, button))
        button.menu.add_command(label="Font Color", command=partial(button.font_color, button))
        button.menu.add_separator()
        button.menu.add_command(label="Unlock", command=partial(button.anchor_unlock, button, window, tmp_x))
        custom_button.make_undraggable(button)

    def make_draggable(widget):
        widget.bind("<Button-1>", custom_button.on_drag_start)
        widget.bind("<B1-Motion>", custom_button.on_drag_motion)

    def make_undraggable(widget):
        widget.unbind("<Button-1>")
        widget.unbind("<B1-Motion>")

    def on_drag_start(event):
        widget = event.widget
        widget.grid
        widget.lift()
        widget._drag_start_x = event.x

    def on_drag_motion(event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        if(x < 0):
            widget.place(x=0)
        elif(x > (event.widget.master.winfo_screenwidth() - 25)):
            widget.place(x=(event.widget.master.winfo_screenwidth() - 25))
        else:
            widget.place(x=x)

    def color_popup(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()