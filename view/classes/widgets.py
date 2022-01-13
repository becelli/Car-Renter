import tkinter as tk
from types import new_class


class TextOutput:
    def __init__(self, root):
        self.root = root

    def display(self, text):
        self.text = text
        self.toplevel = tk.Toplevel(self.root)
        self.text_box_gui(self.toplevel)

    def text_box_gui(self, root):
        tex = tk.Text(master=root).pack()  # text output on the right
        # display text
        self.cbc(self.text, tex)

    def cbc(self, text, tex):
        return lambda: self.callback(text, tex)

    def callback(self, text, tex):
        tex.insert(tk.END, new_text)
        tex.see(tk.END)  # Scroll if necessary
