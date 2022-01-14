from os import write
import tkinter as tk
from view.classes.objects import center as CenterWindow


class TextOutput:
    def __init__(self, root):
        self.root = root

    def display(self, text, title="Texto"):
        self.text = text
        self.toplevel = tk.Toplevel(self.root)
        self.toplevel.title(title)
        self.toplevel.geometry("700x360")
        self.toplevel.resizable(False, False)
        CenterWindow(self.toplevel)

        self.text_box_gui(self.toplevel)

    def text_box_gui(self, root):
        tex = tk.Text(master=root)
        tex.pack(side=tk.RIGHT)
        bop = tk.Frame(master=root)
        bop.pack(side=tk.LEFT)
        tk.Button(bop, text="Mostrar", command=self.cbc(self.text, tex)).pack()
        tk.Button(bop, text="Fechar", command=root.destroy).pack()

    def cbc(self, text, tex):
        return lambda: self.callback(text, tex)

    def callback(self, text, tex):
        s = "Nada a mostrar"
        if isinstance(text, str):
            s = str(text)
        elif isinstance(text, list):
            s = ""
            for i in text:
                s += str(i) + "\n"

        tex.insert(tk.END, s)
        tex.see(tk.END)
