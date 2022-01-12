import tkinter as tk


class PlaceholderEntry(tk.Entry):
    def __init__(
        self,
        master=None,
        placeholder="",
        cnf={},
        fg="black",
        fg_placeholder="grey50",
        *args,
        **kw
    ):
        super().__init__(
            master=master, placeholder=placeholder, cnf={}, bg="white", *args, **kw
        )
        self.fg = fg
        self.fg_placeholder = fg_placeholder
        self.placeholder = placeholder
        self.bind("<FocusOut>", lambda event: self.fill_placeholder())
        self.bind("<FocusIn>", lambda event: self.clear_box())
        self.fill_placeholder()

    def clear_box(self):
        if not self.get() and super().get():
            self.config(fg=self.fg)
            self.delete(0, tk.END)

    def fill_placeholder(self):
        if not super().get():
            self.config(fg=self.fg_placeholder)
            self.insert(0, self.placeholder)

    def get(self):
        content = super().get()
        if content == self.placeholder:
            return ""
        return content


def center(window):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    window.update_idletasks()
    width = window.winfo_width()
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + 2 * frm_width
    height = window.winfo_height()
    titlebar_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = window.winfo_screenwidth() // 2 - win_width // 2
    y = window.winfo_screenheight() // 2 - win_height // 2
    window.geometry("{}x{}+{}+{}".format(width, height, x, y))
    window.deiconify()


def append_label(root, row=0, column=0, width=20, text=""):
    tk.Label(root, text=text, width=width, anchor="w").grid(row=row, column=column)
