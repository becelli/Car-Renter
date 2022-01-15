import tkinter as tk
import view.classes.objects as obj
import controller.controller as controller
import view.main as gui


class Start(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        obj.center(self.root)
        self.root.title("Nome do Banco de Dados")
        self.root.geometry("300x110")
        self.root.resizable(False, False)

        tk.Label(
            self.root,
            text="Insira o nome do banco:",
        ).pack(pady=5)
        self.entry = tk.Entry(self.root)
        self.entry.insert(0, "app.db")
        self.entry.pack(pady=5)
        tk.Button(
            self.root, text="  OK  ", command=lambda: self.main(self.entry.get())
        ).pack(pady=5, padx=5)
        self.root.mainloop()

    def main(self, db: str = "app.db"):
        self.root.destroy()
        db = "app.db" if db == "" else db
        c = controller.Controller(db=db)
        c.init_database(35)
        gui.main(db)
