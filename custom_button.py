import tkinter as tk
from tkinter.colorchooser import askcolor
from functools import partial

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