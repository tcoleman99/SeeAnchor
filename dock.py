from asyncio.windows_events import NULL
from multiprocessing import parent_process
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import E, N, NE, NW, TOP, messagebox
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import random
from venv import create


class Dock(object):

    def __init__(self):

        # Creating dock widget
        self.root = tk.Tk()
        self.pads = []
        self.labels = []
        self.count = 0
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

        self.root.overrideredirect(True)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.title("Dock")
        self.root.configure(bg="gray36")
        self.root.resizable(width=False, height=False)

        titleFrame = tk.Frame(self.root, width=325, height=25, bg="gray36")
        titleFrame.pack_propagate(False)
        titleFrame.pack(side=tk.TOP)
        titleFrame.columnconfigure(0, weight=1)
        titleFrame.columnconfigure(1, weight=3)
        titleFrame.columnconfigure(2, weight=1)

        buttonFrame = tk.Frame(self.root, width=325, height=55, bg="grey36")
        buttonFrame.grid_propagate(False)
        buttonFrame.pack()
        buttonFrame.columnconfigure(0, weight=2)
        buttonFrame.columnconfigure(1, weight=2)
        buttonFrame.columnconfigure(2, weight=2)

        folderFrame = tk.Frame(self.root, width=280, height=400, bg="gray69")
        folderFrame.grid_propagate(False)
        folderFrame.pack(padx=(22.5, 22.5))
        folderFrame.columnconfigure(0, weight=1)
        folderFrame.columnconfigure(1, weight=2)
        folderFrame.columnconfigure(2, weight=1)

        # Button creation for max & min dock
        minimize = tk.Button(titleFrame, text="\/", width=31, command=lambda: self.min_but(screen_width, screen_height, maximize, titleFrame, buttonFrame, folderFrame), relief="flat")
        minimize.pack(side=tk.TOP)

        close = tk.Button(titleFrame, text="X", width=6, bg="firebrick1", command=lambda: self.close_help(), relief="flat")
        close.place(x=273)

        settingsBut = tk.Button(titleFrame, text="O", width=6, bg="turquoise1", command=lambda: self.close_help(), relief="flat")
        settingsBut.place(x=0)

        maximize = tk.Button(self.root, text="/\\",command=lambda: self.max_but(w, h, x, y, maximize, titleFrame, buttonFrame, folderFrame), relief="flat")

        # testLabel = tk.Label(folderFrame, text="New notepad", width=75)
        # testLabel.grid(column=2, row=0, sticky=tk.N, pady=(0, 10))

        # testLabel1 = tk.Label(folderFrame, text="New notepad", width=75)
        # testLabel1.grid(column=2, row=1, sticky=tk.N, pady=(0, 10))

        # testFolder = tk.Button(folderFrame, text='Folder', width=5, height=2, bg="blue")
        # testFolder.grid(column=0, row=0, sticky=tk.W, padx=(25, 0), pady=(15, 0))

        # testFolder1 = tk.Button(folderFrame, text='F', width=5, height=2, bg="blue")
        # testFolder1.grid(column=1, row=0, sticky=tk.W, padx=(25, 0), pady=(15, 0))

        # testFolder2 = tk.Button(folderFrame, text='F', width=5, height=2, bg="blue")
        # testFolder2.grid(column=2, row=0, sticky=tk.W, padx=(25, 0), pady=(15, 0))

        newNote = tk.Button(buttonFrame, text="+", width=5, command=lambda: self.new_note(folderFrame, self.count), relief="flat")
        newNote.grid(column=1, row=0, sticky=tk.W, pady=(15,0))

        delNote = tk.Button(buttonFrame, text="-", width=5, command=lambda: self.sync(), relief="flat")
        delNote.grid(column=1, row=0, sticky=tk.E, pady=(15,0))

        # Sets the app to always be in foreground
        self.root.attributes("-topmost", True)
        self.root.update()
        self.root.mainloop()
    
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

    # Create a new note
    def new_note(self, frame, index):   # Have to pass self.count as index or else self.pads[self.count] does not accept input
        self.pads.append(Notepad(self))
        self.label = tk.Button(frame, text="New label #%d" % (index), width=75, command=lambda: [self.pads[index].openOverride()], relief="flat")
        self.label.grid(column=2, row=self.count, sticky=tk.N, pady=(0, 10))
        self.labels.append(self.label)
        self.count += 1

    # Saves and destroys all notes when closing dock
    def close_help(self):
        for x in self.pads:
            x.root.destroy()

        self.pads.clear()
        self.labels.clear()
        self.root.destroy()

class Notepad(Dock):

    def __init__(self, parent):
        # the root widget
        self.root = tk.Tk()
        self.root.geometry("325x325")
        self.root.eval("tk::PlaceWindow  .   center")
        self.root.title("Notepad")
        self.root.configure(bg="seashell2")
        self.root.resizable(width=True, height=True)
        self.root.protocol("WM_DELETE_WINDOW", self.closeOverride)
        self.root.resizable(0,0)
        self.myparent = parent

        self.filename = "file_" + str(random.randrange(10000, 50000))

        # Creating label
        self.label = create_label(self.root, text="Title", bg="light blue", font=("Times 20 italic bold"))
        self.label.myparent = parent    # To set the main application as the parent of create_label
        self.label.pack(side="top", fill="x")

        # Padding text within the main text box (left, top, right, bottom)
        ttk.Style().configure("pad.TEntry", padding="5 1 5 1")

        # Creating scrollable notepad window
        self.notepad = ScrolledText(self.root, font=("Bold", 15), bg="seashell2", relief="flat")
        self.notepad.configure(padx=12)
        self.notepad.pack(padx=1, pady=1)

        print(parent.count)

    def closeOverride(self):
        self.saveFile()
        self.root.withdraw()

    def openOverride(self):
        self.saveFile()
        self.root.deiconify()

    def saveFile(self):
        print(self.filename)
        # file1 = open(self.filename + ".txt", "w")
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
        self.myparent = None

        self.row = 0

    def edit_start(self, event=None):
        self.entry.place(relx=.5, rely=.5, relwidth=1.0, relheight=1.0, anchor="center")
        info = self.grid_info()
        if(self.row != NULL):
            self.row = info["row"]
        self.entry.focus_set()

    def edit_stop(self, event=None):
        self.configure(text=self.entry.get())
        self.entry.place_forget()
        self.myparent.labels[0].configure(text=self.entry.get())

    def edit_cancel(self, event=None):
        self.entry.delete(0, "end")
        self.entry.place_forget()
        self.myparent.labels[0].configure(text=self.entry.get())