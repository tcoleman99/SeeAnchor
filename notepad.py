import tkinter.ttk as ttk
import create_label
import random
from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
import dock

class Notepad(dock.Dock):

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
        self.titleLabel = create_label.create_label(self.top, text="Title %d" % (position), bg="light blue", font=("Times 20 italic bold"))
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
        self.titleLabel.configure(fg=self.parent.button_list[self.titleLabel.row].cget("fg"))
        self.saveFile()
        self.top.deiconify()

    def saveFile(self):
        pass
        # file1 = open(self.filename + ".txt", "w")
        # file1.write(str(self.titleLabel.position) + "\n")
        # file1.write(self.titleLabel.getTitle(self) + "\n")
        # file1.write(self.notepad.get("1.0","end-1c"))
        # file1.close()