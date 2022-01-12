from tkinter import *
from tkinter import ttk
import controller.controller as c
import model.classes.vehicle as vehicle
import model.classes.random as rand
import view.classes.objects as obj


def insert_insurance_gui(root):
    gui = Toplevel(root)
    gui.title("Cadastro de Seguros")
    gui.geometry("600x400")
    obj.center(gui)
    fields = (
        "ID",
        "Nome",
        "Tipo",
        "Descrição",
        "Valor",
    )
    [
        id,
        name,
        model,
        description,
        value,
    ] = rand.insurance_info()
    placeholders = (
        id,
        name,
        model,
        description,
        value,
    )
    entries = {}
    # add a padding in the top
    space = Frame(gui, height=15)
    space.grid(row=1, column=0)

    # fields
    for field in fields:
        Label(gui, text=field, width=20, anchor="w").grid(
            row=fields.index(field) + 2, column=0
        )
        entries[field] = ttk.Entry(gui, width=30)
        entries[field].grid(row=(fields.index(field) + 2), column=1, sticky=W)
        entries[field].insert(0, placeholders[fields.index(field)])
        if fields.index(field) == 0:
            entries[field].focus()
        ttk.Button(
            gui,
            text="Cadastrar",
            command=lambda: gui.destroy()
            if try_insert(entries) == "success"
            else obj.append_label(
                gui,
                row=len(fields) + 4,
                column=0,
                text=try_insert(entries),
            ),
        ).grid(row=len(fields) + 3, column=1, sticky=W, pady=10)


def validate_insurance_input(input):
    errors = []
    return "success"


def try_insert(entries):
    validate = validate_insurance_input(entries)
    if validate == "success":
        c.insert_insurance(
            entries["ID"].get(),
            entries["Nome"].get(),
            entries["Tipo"].get(),
            entries["Descrição"].get(),
            entries["Valor"].get(),
        )
        return "success"
    else:
        return validate
