from asyncio.windows_events import NULL
from cProfile import label
from ctypes import sizeof
import re
from textwrap import fill
import tkinter as tk
import tkinter.ttk as ttk
#from tkinter import *
from tkinter import E, N, NE, NW, TOP, messagebox
from tkinter.scrolledtext import ScrolledText
import pickle
from tkinter import filedialog, simpledialog
from turtle import width
from venv import create

class Notepad:

    def __init__(self):
        # the root widget
        self.root = tk.Tk()
        self.root.geometry("325x325")
        self.root.eval("tk::PlaceWindow  .   center")
        self.root.title("Notepad")
        self.root.configure(bg="seashell2")
        self.root.resizable(width=True, height=True)

        # Creating label
        self.label = create_label(self.root, text="Title", bg="light blue", font=("Times 20 italic bold"))
        self.label.pack(side="top", fill="x")

        # Padding text within the main text box (left, top, right, bottom)
        ttk.Style().configure("pad.TEntry", padding="5 1 5 1")

        # Creating scrollable notepad window
        self.notepad = ScrolledText(self.root, font=("Bold", 15), bg="seashell2", relief="flat")
        self.notepad.configure(padx=12)
        self.notepad.pack(padx=1, pady=1)

        button1 = tk.Button(self.root, text="Foo", width=5, command=lambda: self.root.withdraw())
        button1.pack()

    def cmdSave(self):
        fd = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if fd!=None:
            data = self.notepad.get("1.0", tk.END)
        try:
            fd.write(data)
        except:
            messagebox.showerror(title="Error", message="Not able to save.")

class create_label(tk.Label):

    # Creating entry & setting input actions
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.entry = tk.Entry(self, bg="white", justify="center")
        self.bind("<Double-1>", self.edit_start)
        self.entry.bind("<Return>", self.edit_stop)
        self.entry.bind("<FocusOut>", self.edit_stop)
        self.entry.bind("<Escape>", self.edit_cancel)

        self.mytxt = ""
        self.row = 0

    def edit_start(self, event=None):
        self.entry.place(relx=.5, rely=.5, relwidth=1.0, relheight=1.0, anchor="center")
        info = self.grid_info()
        if(self.row != NULL):
            self.row = info["row"]
        self.entry.focus_set()

    def edit_stop(self, event=None):
        self.mytxt = self.entry.get()
        self.configure(text=self.entry.get())
        Dock.getNote(0)
        self.entry.place_forget()

    def edit_cancel(self, event=None):
        self.entry.delete(0, "end")
        self.entry.place_forget()

    def getTxt(self):
        return self.mytxt

class Dock:

    def __init__(self):

        # Creating dock widget
        self.root = tk.Tk()
        self.pads = []
        self.labels = []
        # Getting screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Original GUI size is 325x500
        w = 325
        h = 500
        self.count = 0
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

        close = tk.Button(titleFrame, text="X", width=6, bg="firebrick1", command=lambda: self.root.destroy(), relief="flat")
        close.place(x=273)

        settingsBut = tk.Button(titleFrame, text="O", width=6, bg="turquoise1", command=lambda: self.root.destroy(), relief="flat")
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

        newNote = tk.Button(buttonFrame, text="+", width=5, command=lambda: self.new_note(folderFrame), relief="flat")
        newNote.grid(column=1, row=0, sticky=tk.W, pady=(15,0))

        delNote = tk.Button(buttonFrame, text="-", width=5, command=lambda: print(self.pads[0].withdraw()), relief="flat")
        delNote.grid(column=1, row=0, sticky=tk.E, pady=(15,0))

        delNote2 = tk.Button(buttonFrame, text="=", width=5, command=lambda: print(self.pads[0].deiconify()), relief="flat")
        delNote2.grid(column=1, row=0, sticky=tk.N, pady=(15,0))

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

    def new_note(self, frame):
        label = tk.Button(frame, text="New label #%d" % (self.count), width=75)
        label.grid(column=2, row=self.count, sticky=tk.N, pady=(0, 10))
        self.labels.append(label)
        self.count += 1
        self.pads.append(Notepad())

    def testfunc(self):
        for x in self.pads:
            print(x)

app=Dock()