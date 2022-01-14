import tkinter as tk
import tkinter.messagebox as tkmb
import tkinter.ttk as ttk
import controller.controller as c
import model.classes.vehicle as vehicle
import model.classes.random as rand
import view.classes.objects as obj
from datetime import datetime


def insert_imported_gui(root, db: str = "app.db"):
    gui = tk.Toplevel(root)
    gui.title("Cadastro de Veículo Importado")
    gui.geometry("420x280")
    obj.center(gui)
    fields = (
        "Placa",
        "Modelo",
        "Fabricante",
        "Ano",
        "Ano do Modelo",
        "Categoria",
        "Valor na FIPE",
        "Valor da Diária",
        "Disponível [S/N]",
        "Imposto Estadual",
        "Imposto Federal",
    )
    [
        model,
        manufacturer,
        fabrication_year,
        model_year,
        plate_number,
        category,
        price,
        rent_price,
        is_available,
        state_taxes,
        federal_taxes,
    ] = rand.ClassesData(db).vehicle_info()
    placeholders = (
        plate_number,
        model,
        manufacturer,
        fabrication_year,
        model_year,
        category,
        price,
        rent_price,
        "S" if is_available else "N",
        state_taxes,
        federal_taxes,
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
            if try_insert(entries, "imported", db) == "success"
            else (tkmb.showerror("Erro", try_insert(entries, "imported", db))),
        ).grid(row=len(fields) + 3, column=1, sticky=tk.W, pady=10)


def insert_national_gui(root, db: str = "app.db"):
    gui = tk.Toplevel(root)
    gui.title("Cadastro de Veículo Nacional")
    gui.geometry("420x260")
    obj.center(gui)
    fields = (
        "Placa",
        "Modelo",
        "Fabricante",
        "Ano",
        "Ano do Modelo",
        "Categoria",
        "Valor na FIPE",
        "Valor da Diária",
        "Disponível [S/N]",
        "Imposto Estadual",
    )
    [
        model,
        manufacturer,
        fabrication_year,
        model_year,
        plate_number,
        category,
        price,
        rent_price,
        is_available,
        state_taxes,
        _,
    ] = rand.ClassesData(db).vehicle_info()
    placeholders = (
        plate_number,
        model,
        manufacturer,
        fabrication_year,
        model_year,
        category,
        price,
        rent_price,
        "S",
        state_taxes,
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
            if try_insert(entries, "national", db) == "success"
            else tkmb.showerror("Erro", try_insert(entries, "national", db)),
        ).grid(row=len(fields) + 3, column=1, sticky=tk.W, pady=10)


def validate_vehicle_input(input, type):
    errors = []

    plate = input["Placa"].get()
    model = input["Modelo"].get()
    manufacturer = input["Fabricante"].get()
    fabrication_year = input["Ano"].get()
    model_year = input["Ano do Modelo"].get()
    category = input["Categoria"].get()
    fipe_value = input["Valor na FIPE"].get()
    rent_value = input["Valor da Diária"].get()
    is_available = input["Disponível [S/N]"].get()
    state_taxes = input["Imposto Estadual"].get()

    # Plate
    if len(plate) != 8:
        errors.append("Placas devem conter 8 dígitos, no formato ABC-1234")
    for i in range(len(plate)):
        if (i < 3 and plate[i].isdigit()) or (i >= 4 and plate[i].isalpha()):
            errors.append("Placas devem conter 8 dígitos, no formato ABC-1234")
    # Model, Manufacturer
    if len(model) < 3:
        errors.append("Modelo deve conter no mínimo 3 caracteres")
    if len(manufacturer) < 3:
        errors.append("Fabricante deve conter no mínimo 3 caracteres")
    # Fabrication Year
    if fabrication_year.isdigit():
        if int(fabrication_year) < 1900 or int(fabrication_year) > datetime.now().year:
            errors.append("Ano de fabricação inválido")
    # Model Year
    if model_year.isdigit():
        if int(model_year) < 1900 or int(model_year) > datetime.now().year:
            errors.append("Ano do modelo inválido")
    # Category
    categories = ["CARRO", "MOTOCICLETA", "CAMINHAO", "ONIBUS", "VAN", "BICICLETA"]
    if category.upper() not in categories:
        errors.append(
            "Categoria inválida. Escolha uma das opções: " + ", ".join(categories)
        )
    # FIPE Value
    if fipe_value.isdigit():
        if int(fipe_value) < 0:
            errors.append("Valor na FIPE inválido")
    # Rent Value
    if rent_value.isdigit():
        if int(rent_value) < 0:
            errors.append("Valor da diária inválido")
    # Is Available
    if is_available.upper() not in ["S", "N"]:
        errors.append("Disponibilidade inválida. Escolha S ou N")

    # State Taxes
    if state_taxes.isdigit():
        if float(state_taxes) < 0 or float(state_taxes) >= 1:
            errors.append("Imposto Estadual inválido")
    if type == "imported":
        federal_taxes = input["Imposto Federal"].get()
        if federal_taxes.isdigit():
            if float(federal_taxes) < 0 or float(federal_taxes) >= 1:
                errors.append("Imposto Federal inválido")
    if len(errors) > 0:
        return "\n".join(errors)
    return "success"


def try_insert(entries, type: str, db: str = "app.db"):
    validate = validate_vehicle_input(entries, type)
    if validate == "success":
        if type == "imported":
            c.Controller(db).insert_vehicle(
                vehicle.Imported(
                    entries["Placa"].get(),
                    entries["Modelo"].get(),
                    entries["Fabricante"].get(),
                    entries["Ano"].get(),
                    entries["Ano do Modelo"].get(),
                    entries["Categoria"].get(),
                    entries["Valor na FIPE"].get(),
                    entries["Valor da Diária"].get(),
                    entries["Disponível [S/N]"].get(),
                    entries["Imposto Estadual"].get(),
                    entries["Imposto Federal"].get(),
                )
            ),
            return "success"
        elif type == "national":
            c.Controller(db).insert_vehicle(
                vehicle.National(
                    entries["Placa"].get(),
                    entries["Modelo"].get(),
                    entries["Fabricante"].get(),
                    entries["Ano"].get(),
                    entries["Ano do Modelo"].get(),
                    entries["Categoria"].get(),
                    entries["Valor na FIPE"].get(),
                    entries["Valor da Diária"].get(),
                    entries["Disponível [S/N]"].get(),
                    entries["Imposto Estadual"].get(),
                )
            ),
            return "success"
    else:
        return validate
