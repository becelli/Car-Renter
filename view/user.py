import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import ttk
import controller.controller as c
import model.classes.random as rand
import view.classes.objects as obj


def insert_employee_gui(root, db: str = "app.db"):
    gui = tk.Toplevel(root)
    gui.title("Cadastro de Funcionário")
    gui.geometry("420x280")
    obj.center(gui)
    fields = (
        "Nome",
        "CPF",
        "RG",
        "Data de Nascimento",
        "Endereço",
        "CEP",
        "Email",
        "Salário",
        "PIS",
        "Data de Admissão",
    )
    [
        name,
        cpf,
        rg,
        birth_date,
        address,
        zip_code,
        email,
        _,
        _,
        _,
        _,
        salary,
        pis,
        admission_date,
    ] = rand.ClassesData(db).user_info()
    placeholders = (
        name,
        cpf,
        rg,
        birth_date,
        address,
        zip_code,
        email,
        salary,
        pis,
        admission_date,
    )
    entries = {}
    # add a padding in the top
    space = tk.Frame(gui, height=15)
    space.grid(row=1, column=0)

    # fields
    for field in fields:
        tk.Label(gui, text=field, width=20, anchor="w").grid(
            row=fields.index(field) + 2, column=0
        )
        entries[field] = ttk.Entry(gui, width=30)
        entries[field].grid(row=(fields.index(field) + 2), column=1, sticky=tk.W)
        entries[field].insert(0, placeholders[fields.index(field)])
        if fields.index(field) == 0:
            entries[field].focus()
        ttk.Button(
            gui,
            text="Cadastrar",
            command=lambda: gui.destroy()
            if try_insert(entries, "employee", db) == "success"
            else tkmb.showerror("Erro", try_insert(entries, "employee", db)),
        ).grid(row=len(fields) + 3, column=1, sticky=tk.W, pady=10)


def insert_client_gui(root, db: str = "app.db"):
    gui = tk.Toplevel(root)
    gui.title("Cadastro de Cliente")
    gui.geometry("600x400")
    obj.center(gui)
    fields = (
        "Nome",
        "CPF",
        "RG",
        "Data de Nascimento",
        "Endereço",
        "CEP",
        "Email",
        "Carta [A/B/C/D/E]",
        "Nº da CNH",
        "Expiração da CNH",
        "Cliente Ouro [S/N]",
    )
    [
        name,
        cpf,
        rg,
        birth_date,
        address,
        zip_code,
        email,
        permission_category,
        permission_number,
        permission_date,
        is_golden_client,
        _,
        _,
        _,
    ] = rand.ClassesData(db).user_info()
    placeholders = (
        name,
        cpf,
        rg,
        birth_date,
        address,
        zip_code,
        email,
        permission_category,
        permission_number,
        permission_date,
        "S" if is_golden_client else "N",
    )
    entries = {}
    # add a padding in the top
    space = tk.Frame(gui, height=15)
    space.grid(row=1, column=0)

    # fields
    for field in fields:
        tk.Label(gui, text=field, width=20, anchor="w").grid(
            row=fields.index(field) + 2, column=0
        )
        entries[field] = ttk.Entry(gui, width=30)
        entries[field].grid(row=(fields.index(field) + 2), column=1, sticky=tk.W)
        entries[field].insert(0, placeholders[fields.index(field)])
        if fields.index(field) == 0:
            entries[field].focus()
        ttk.Button(
            gui,
            text="Cadastrar",
            command=lambda: gui.destroy()
            if try_insert(entries, "client", db) == "success"
            else tkmb.showerror("Erro", try_insert(entries, "client", db)),
        ).grid(row=len(fields) + 3, column=1, sticky=tk.W, pady=10)


def validate_user_input(input, type):
    errors = []
    name = input["Nome"]
    cpf = input["CPF"]
    rg = input["RG"]
    birth_date = input["Data de Nascimento"]
    address = input["Endereço"]
    zip_code = input["CEP"]
    email = input["Email"]
    if type == "employee":
        salary = input["Salário"]
        pis = input["PIS"]
        admission_date = input["Data de Admissão"]
    if type == "client":
        permission_category = input["Carta [A/B/C/D/E]"]
        permission_number = input["Nº da CNH"]
        permission_date = input["Expiração da CNH"]
        is_golden_client = input["Cliente Ouro [S/N]"]

    # def validate_permission_expiration(self, permission_expiration):
    #     if len(permission_expiration) != 7:
    #         raise ValueError("Invalid date expression")
    #     aux = dt.strptime(permission_expiration, "%Y-%m")
    #     if aux < dt.now():
    #         raise ValueError("Permission expiration date is in the past")
    return "success"


def try_insert(entries, type: str, db: str = "app.db"):
    validate = validate_user_input(entries, type)
    if validate == "success":
        if type == "imported":
            c.Controller(db).insert_employee(
                entries["Nome"].get(),
                entries["CPF"].get(),
                entries["RG"].get(),
                entries["Data de Nascimento"].get(),
                entries["Endereço"].get(),
                entries["CEP"].get(),
                entries["Email"].get(),
                entries["Salário"].get(),
                entries["PIS"].get(),
                entries["Data de Admissão"].get(),
            ),

            return "success"
        elif type == "client":
            c.Controller(db).insert_client(
                entries["Nome"].get(),
                entries["CPF"].get(),
                entries["RG"].get(),
                entries["Data de Nascimento"].get(),
                entries["Endereço"].get(),
                entries["CEP"].get(),
                entries["Email"].get(),
                entries["Carta [A/B/C/D/E]"].get(),
                entries["Nº da CNH"].get(),
                entries["Expiração da CNH"].get(),
                entries["Cliente Ouro [S/N]"].get(),
            )
            return "success"
    else:
        return validate
