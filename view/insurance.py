import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import ttk
import controller.controller as c
import model.classes.insurance as ins
import model.classes.random as rand
import view.classes.objects as obj


def insert_insurance_gui(root, db: str = "app.db"):
    gui = tk.Toplevel(root)
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
    ] = rand.ClassesData(db).insurance_info()
    placeholders = (
        name,
        model,
        description,
        value,
    )
    entries = {}
    # add a padding in the top
    space = tk.Frame(gui, height=15)
    space.grid(row=1, column=0)

    # fields
    for field in fields:
        tk.Label(gui, text=field, anchor="w").grid(
            row=fields.index(field) + 2, column=0
        )
        entries[field] = ttk.Entry(gui, width=35)
        entries[field].grid(row=(fields.index(field) + 2), column=1, sticky=tk.W)
        entries[field].insert(0, placeholders[fields.index(field)])
        if fields.index(field) == 0:
            entries[field].focus()
        ttk.Button(
            gui,
            text="Cadastrar",
            command=lambda: gui.destroy()
            if try_insert(entries, db) == "success"
            else None,
        ).grid(row=len(fields) + 3, column=1, sticky=tk.W, pady=10)


def validate_insurance_input(input):
    errors = []
    name = input["Nome"].get()
    model = input["Tipo"].get()
    description = input["Descrição"].get()
    value = input["Valor"].get()

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
    if len(errors) > 0:
        for error in errors:
            tkmb.showerror("Erro", error)
        return "error"
    return "success"


def try_insert(entries, db: str = "app.db"):
    validate = validate_insurance_input(entries)
    if validate == "success":
        c.Controller(db).insert_insurance(
            ins.Insurance(
                entries["Nome"].get(),
                entries["Tipo"].get(),
                entries["Descrição"].get(),
                float(entries["Valor"].get()),
            )
        )
        return "success"
    else:
        return validate
