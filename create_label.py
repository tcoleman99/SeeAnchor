import tkinter as tk

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

    # These three functions are for the title on each note. This allows for double clicking to enter input
    # into the entry and determines how the input is passed by either canceling the input (clicking out of the entry)
    # or pressing "Enter" to confirm input
    def edit_start(self, event=None):

        self.entry.place(relx=.5, rely=.5, relwidth=1.0, relheight=1.0, anchor="center")
        self.entry.focus_set()

    def edit_stop(self, event=None):
        self.configure(text=self.entry.get())
        self.entry.place_forget()
        self.newParent.note_button_list[self.row].configure(text=self.entry.get())

    def edit_cancel(self, event=None):
        self.entry.delete(0, "end")
        self.entry.place_forget()
        self.newParent.note_button_list[self.row].configure(text=self.entry.get())