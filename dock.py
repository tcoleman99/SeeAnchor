from asyncio.windows_events import NULL
from http.client import NOT_ACCEPTABLE
from mimetypes import common_types
from time import sleep
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import E, N, NE, NW, TOP, W, Toplevel
from tkinter.scrolledtext import ScrolledText
import random
from functools import partial

class Dock(object):

    def __init__(self):

        # Creating dock widget
        self.root = tk.Tk()
        self.pads = []
        self.notepad_list = []
        self.count = 0
        self.editable = False

        # Getting screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Original GUI size is 325x500
        w = 325
        h = 500

        # Setting position of GUI on start up (subtract 40 for the taskbar)
        x = screen_width - w
        y = screen_height - h - 40

        # For getting size of current window?
        self.root.update_idletasks()

        # Setting up frames for root window, title, buttons, and notepad list
        self.root.overrideredirect(True)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
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
        self.folderFrame = tk.Frame(self.root, width=280, height=400, bg="blue") # w=280, h=400
        self.canvas = tk.Canvas(self.folderFrame, width=265, height=365, bg="blue")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        scrollbar = ttk.Scrollbar(self.folderFrame, orient="vertical", command=self.canvas.yview)
        scrollable_frame = tk.Frame(self.canvas, width=265, height=365, bg="grey69")
        scrollable_frame.columnconfigure(0, weight=1)

        scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.folderFrame.pack() # padx=(20, 20)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Button creation
        minimize = tk.Button(self.titleFrame, text="\/", width=31, command=lambda: self.min_but(screen_width, screen_height, maximize, self.titleFrame, self.buttonFrame, self.folderFrame), relief="flat")
        minimize.pack(side=tk.TOP)

        close = tk.Button(self.titleFrame, text="X", width=6, bg="firebrick1", command=lambda: self.close_help(), relief="flat")
        close.place(x=273)

        settingsBut = tk.Button(self.titleFrame, text="O", width=6, bg="turquoise1", command=lambda: self.close_help(), relief="flat")
        settingsBut.place(x=0)

        maximize = tk.Button(self.root, text="/\\",command=lambda: self.max_but(w, h, x, y, maximize, self.titleFrame, self.buttonFrame, self.folderFrame), relief="flat")

        newNote = tk.Button(self.buttonFrame, text="+", width=5, command=lambda: self.new_note(scrollable_frame, self.count), relief="flat")
        newNote.grid(column=1, row=0, sticky=W, pady=(15,0))

        delNote = tk.Button(self.buttonFrame, text="Edit", width=5, command=lambda: self.set_editable(), relief="flat")
        delNote.grid(column=1, row=0, sticky=E, pady=(15,0))

        # Sets the app to always be in foreground and runs
        self.root.attributes("-topmost", True)
        self.root.update()
        self.root.mainloop()
    
    # ============================FUNCTIONS=============================
    # ----------Title Frame-----------
    # Minimize button
    def min_but(self, scw, sch, maxb, tf, bf, ff):
        self.root.geometry('%dx%d+%d+%d' % (25, 25, (scw - 50), (sch - 65)))
        self.root.overrideredirect(True)
        tf.pack_forget()
        bf.pack_forget()
        ff.pack_forget()
        for x in self.pads:
            x.closeOverride()
        
        maxb.pack(side="top", fill='x')
        self.root.update_idletasks()

    # Maximize button
    def max_but(self, wi, hi, xi, yi, maxb, tf, bf, ff):
        self.root.overrideredirect(True)
        self.root.geometry('%dx%d+%d+%d' % (wi, hi, xi, yi))
        maxb.pack_forget()
        tf.pack(side="top")
        bf.pack()
        ff.pack(padx=(22.5, 22.5))
        self.root.update_idletasks()

    # Saves and destroys all notes when closing dock
    def close_help(self):
        for x in self.pads:
            x.top.destroy()
        self.pads.clear()
        self.notepad_list.clear()
        self.root.destroy()

    # ----------Button Frame----------
    # Create a new note, makes new entries in lists, makes button draggable if edit is enabled
    def new_note(self, frame, index):   # Have to pass self.count as index or else self.pads[self.count] does not accept input
        self.pads.append(Notepad(self, self.count))
        # testframe = tk.Frame(frame, width=265, height=25, bg="red")
        # testframe.pack_propagate(False) # Pack_propagate works but grid_propagate doesn't when using grid to display frame??
        # testframe.grid(column=0, row=self.count, sticky=tk.E, pady=(0, 10))
        self.label = tk.Button(frame, text="New label #%d" % (index), width=36, command=lambda: [self.pads[index].openOverride(), ], relief="flat")
        self.label.grid(column=0, columnspan=2, row=self.count, sticky=tk.N+tk.S+tk.E+tk.W, pady=(0, 10))
        if(self.editable == True):
            self.label["state"] = "disabled"
            #Dock.make_draggable(self.label)
        self.notepad_list.append(self.label)
        self.count += 1

    # ----------Drag & Drop-----------
    # For drag and drop of labels in dock

    def set_editable(self):
        if(len(self.notepad_list) > 0 and self.editable == False):
            for i in range(len(self.notepad_list)):
                self.notepad_list[i].configure(command=lambda idx=i: self.set_select(self.notepad_list[idx]))
                # if(i==0):
                #     self.notepad_list[0].configure(command=lambda: Dock._selected(self.notepad_list[0]))
                #self.notepad_list[i].configure(command=lambda: Dock._selected(self.notepad_list[i]))
                #print(self.notepad_list[i].cget("text"))
                #Dock._selected(self.notepad_list[i])
                # self.label.configure(command=lambda: Dock._selected(self.label))
            # for x in self.notepad_list:
            #     x["state"] = "disabled"
            #     Dock.make_draggable(x)
            self.editable = True
        elif(len(self.notepad_list) > 0 and self.editable == True):
            # for x in self.notepad_list:
            #     Dock.make_undraggable(x)
            #     x["state"] = "normal"
            for i in range(len(self.notepad_list)):
                self.notepad_list[i].configure(command=lambda idx=i: self.pads[idx].openOverride())
            self.editable = False
        else:
            self.editable = False
    # Sets all other button     
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def set_select(self, target):
        target.configure(bg="Yellow")
        for i in range(len(self.notepad_list)):
            self.notepad_list[i].configure(command=lambda idx=i: self.switch(self.notepad_list[idx]))

    def switch(self, target):
        target.configure(bg="Green")
        for i in self.notepad_list:
            if(i.cget("bg") == "Yellow"):
                first_target = i
            if(i.cget("bg") == "Green"):
                second_target = i
            else:
                print("*")
        row1 = first_target.grid_info()["row"]
        row2 = second_target.grid_info()["row"]
        first_target.grid(row=row2)
        second_target.grid(row=row1)
        for i in range(len(self.notepad_list)):
            self.notepad_list[i].configure(bg="white")
            self.notepad_list[i].configure(command=lambda idx=i: self.set_select(self.notepad_list[idx]))
        
        
    # def make_draggable(widget):
    #     widget.bind("<Button-1>", Dock.on_drag_start)
    #     widget.bind("<B1-Motion>", Dock.on_drag_motion)
    #     widget.bind("<ButtonRelease-1>", Dock.snap)
    #     widget.configure(width=30) # 273
    #     print(widget.grid_info())

    # def make_undraggable(widget):
    #     widget.unbind("<Button-1>")
    #     widget.unbind("<B1-Motion>")

    # def on_drag_start(event):
    #     widget = event.widget
    #     widget.grid
    #     widget.lift()
    #     widget._drag_start_y = event.y

    # def on_drag_motion(event):
    #     widget = event.widget
    #     y = widget.winfo_y() - widget._drag_start_y + event.y
    #     if(y < 0):
    #         widget.place(y=0)
    #     else:
    #         widget.place(y=y)
    #     print(y)

    # def snap(event):
    #     widget = event.widget
    #     boundary_one = (widget.winfo_y() // 35) * 35
    #     print("B1: " + str(boundary_one))
    #     boundary_two = boundary_one + 35
    #     print("B2: " + str(boundary_two))
    #     if((boundary_one <= widget.winfo_y() <= boundary_two)):
    #         #widget.place(y=boundary_one)
    #         widget.grid(column=0, columnspan=2, row=(widget.winfo_y() // 35), sticky=tk.N+tk.S+tk.E+tk.W, pady=(0, 10))
    #     Dock.func(widget)

    # def rearrange(self):
    #     for i in range(len(self.notepad_list)):
    #         for x in range(len(self.notepad_list)):
    #             if(i == x):
    #                 pass
    #             elif(self.notepad_list[i] == self.notepad_list[x]):
    #                 self.notepad_list[x] = max(self.notepad_list) + 1
    #             else:
    #                 print("k")
    #             self.notepad_list.sort()
    #             print(self.notepad_list)

class Notepad(Dock):

    def __init__(self, parent, position):
        # the root widget
        self.top = Toplevel()
        self.top.geometry("325x325")
        #self.top.eval("tk::PlaceWindow  .   center")
        self.top.title("Notepad")
        self.top.configure(bg="seashell2")
        self.top.resizable(width=True, height=True)
        self.top.protocol("WM_DELETE_WINDOW", self.closeOverride)
        self.top.resizable(0,0)
        self.position = position

        self.filename = "file_" + str(random.randrange(10000, 50000))

        # Creating label
        self.label = create_label(self.top, text="Title", bg="light blue", font=("Times 20 italic bold"))
        self.label.newParent = parent    # To set the main application as the parent of create_label
        self.label.row = self.position
        self.label.pack(side="top", fill="x")

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
        self.saveFile()
        self.top.deiconify()

    def saveFile(self):
        print(" ")
        # file1 = open(self.filename + ".txt", "w")
        # file1.write(str(self.label.position) + "\n")
        # file1.write(self.label.getTitle(self) + "\n")
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
        # info = self.grid_info()
        # if(self.row != NULL):
        #     self.row = info["row"]
        self.entry.focus_set()

    def edit_stop(self, event=None):
        self.configure(text=self.entry.get())
        self.entry.place_forget()
        self.newParent.notepad_list[self.row].configure(text=self.entry.get())

    def edit_cancel(self, event=None):
        self.entry.delete(0, "end")
        self.entry.place_forget()
        self.newParent.notepad_list[self.row].configure(text=self.entry.get())