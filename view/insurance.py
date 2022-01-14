from sqlite3 import dbapi2
import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import ttk
import controller.controller as c
import model.classes.insurance as ins
import model.classes.random as rand
import view.classes.objects as obj


class Insurance:
    def __init__(self, root, db: str = "app.db"):
        self.database_name = db
        self.c = c.Controller(db)
        self.root = root

    def insert_insurance_gui(self):
        gui = tk.Toplevel(self.root)
        gui.title("Cadastro de Seguros")
        gui.geometry("350x150")
        obj.center(gui)
        fields = (
            "Nome",
            "Tipo",
            "Descrição",
            "Valor",
        )
        [
            name,
            model,
            description,
            value,
        ] = rand.ClassesData(self.database_name).insurance_info()
        placeholders = (
            name,
            model,
            description,
            value,
        )
        self.entries = {}
        # add a padding in the top
        space = tk.Frame(gui, height=15)
        space.grid(row=1, column=0)

        # fields
        for field in fields:
            tk.Label(gui, text=field, anchor="w").grid(
                row=fields.index(field) + 2, column=0
            )
            self.entries[field] = ttk.Entry(gui, width=35)
            self.entries[field].grid(
                row=(fields.index(field) + 2), column=1, sticky=tk.W
            )
            self.entries[field].insert(0, placeholders[fields.index(field)])
            if fields.index(field) == 0:
                self.entries[field].focus()
            ttk.Button(
                gui,
                text="Cadastrar",
                command=lambda: self.try_insert(),
            ).grid(row=len(fields) + 3, column=1, sticky=tk.W, pady=10)

    def validate_insurance_entries(self):
        errors = []
        name = self.entries["Nome"].get()
        model = self.entries["Tipo"].get()
        description = self.entries["Descrição"].get()
        value = self.entries["Valor"].get()

        if name == "":
            errors.append("Nome não pode ser vazio")
        if len(name) < 3:
            errors.append("Nome deve conter pelo menos 3 caracteres")
        if model == "":
            errors.append("Tipo não pode ser vazio")
        if len(model) < 3:
            errors.append("Tipo deve conter pelo menos 3 caracteres")
        if description == "":
            errors.append("Descrição não pode ser vazia")
        if len(description) < 3:
            errors.append("Descrição deve conter pelo menos 3 caracteres")
        if value == "":
            errors.append("Valor não pode ser vazio")
        for i in value:
            if i not in "0123456789.":
                errors.append("Valor deve conter apenas números")

        return errors

    def try_insert(self):
        errors = self.validate_insurance_entries()
        if len(errors) > 0:
            for i in errors:
                tkmb.showerror("Erro", i)
        else:
            c.Controller(self.database_name).insert_insurance(
                ins.Insurance(
                    self.entries["Nome"].get(),
                    self.entries["Tipo"].get(),
                    self.entries["Descrição"].get(),
                    float(self.entries["Valor"].get()),
                )
            )
            tkmb.showinfo("Sucesso", "Seguro cadastrado com sucesso")
