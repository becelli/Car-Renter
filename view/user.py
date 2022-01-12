import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import ttk
import controller.controller as c
import model.classes.random as rand
import view.classes.objects as obj
from datetime import datetime


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
    for i in range(len(name)):
        if i.isdigit():
            errors.append("Nome não pode conter números")
            break
    if len(name) < 3:
        errors.append("Nome deve conter no mínimo 3 caracteres")

    cpf = input["CPF"]
    if len(cpf) != 11:
        errors.append("CPF deve conter 11 caracteres")
    for i in range(len(cpf)):
        if not cpf[i].isdigit():
            errors.append("CPF deve conter apenas números")
            break
    rg = input["RG"]
    if len(rg) != 9:
        errors.append("RG deve conter 9 caracteres")
    for i in range(len(rg)):
        if not rg[i].isdigit():
            errors.append("RG deve conter apenas números")
            break

    birth_date = input["Data de Nascimento"]
    if birth_date is None:
        errors.append("Data de Nascimento não pode ser vazia")
    if len(birth_date) != 10:
        errors.append("Data de Nascimento deve conter 10 caracteres")
    if birth_date[4] != "-" or birth_date[7] != "-":
        errors.append("Data de Nascimento deve estar no formato AAAA-MM-DD")

    address = input["Endereço"]
    if len(address) < 5:
        errors.append("Endereço deve conter no mínimo 5 caracteres")

    zip_code = input["CEP"]
    if len(zip_code) != 8:
        errors.append("CEP deve conter 8 caracteres")

    email = input["Email"]
    if email is None:
        errors.append("Email cannot be empty")
    if "@" not in email:
        errors.append("Email must contain @")
    if "." not in email:
        errors.append("Email must contain .")
    if email.count("@") > 1:
        errors.append("Email must contain only one @")

    if type == "employee":

        salary = input["Salário"]
        if salary is None:
            errors.append("Salário não pode ser vazio")
        if len(salary) < 3:
            errors.append("Salário deve conter no mínimo 3 caracteres")
        for i in range(len(salary)):
            if not salary[i].isdigit() and salary[i] != "." and salary[i] != ",":
                errors.append("Salário deve conter apenas números")
                break
        if salary[-1] == "." or salary[-1] == ",":
            errors.append("Salário deve conter apenas números")

        pis = input["PIS"]
        if len(pis) != 11:
            errors.append("PIS deve conter 11 caracteres")

        admission_date = input["Data de Admissão"]
        if len(admission_date) != 10:
            errors.append("Data de Admissão deve conter 10 caracteres")
        aux = datetime.strptime(admission_date, "%Y-%m-%d")
        if aux > datetime.now():
            errors.append("Data de Admissão não pode ser maior que a data atual")
    if type == "client":
        permission_category = input["Carta [A/B/C/D/E]"]
        if permission_category is None:
            errors.append("Carta não pode ser vazia")
        if len(permission_category) != 1:
            errors.append("Carta deve conter apenas um caractere")
        if permission_category not in ["A", "B", "C", "D", "E"]:
            errors.append("Carta deve ser A, B, C, D ou E")

        permission_number = input["Nº da CNH"]
        if len(permission_number) != 10:
            errors.append("Nº da CNH deve conter 10 caracteres")
        for i in range(len(permission_number)):
            if not permission_number[i].isdigit():
                errors.append("Nº da CNH deve conter apenas números")
                break
        permission_date = input["Expiração da CNH"]
        if len(permission_date) != 10:
            errors.append("Expiração da CNH deve conter 10 caracteres")
        is_golden_client = input["Cliente Ouro [S/N]"]

    # def validate_permission_expiration(self, permission_expiration):
    #     if len(permission_expiration) != 7:
    #         errors.append("Invalid date expression")
    #     aux = dt.strptime(permission_expiration, "%Y-%m")
    #     if aux < dt.now():
    #         errors.append("Permission expiration date is in the past")
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
