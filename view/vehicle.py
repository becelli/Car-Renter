import tkinter as tk
import tkinter.messagebox as tkmb
import tkinter.ttk as ttk
import view.classes.widgets as widgets
import controller.controller as c
import model.classes.vehicle as vehicle
import model.classes.random as rand
import view.classes.objects as obj
from datetime import datetime


class Vehicle:
    def __init__(self, root, db: str = "app.db"):
        self.database_name = db
        self.c = c.Controller(db)
        self.root = root
        self.origin = None

    def insert_imported_gui(self):
        self.origin = "imported"
        gui = tk.Toplevel(self.root)
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
        ] = rand.ClassesData(self.database_name).vehicle_info()
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
        self.entries = {}
        # add a padding in the top
        space = tk.Frame(gui, height=15)
        space.grid(row=1, column=0)

        # fields
        for field in fields:
            tk.Label(gui, text=field, width=20, anchor="w").grid(
                row=fields.index(field) + 2, column=0
            )
            self.entries[field] = ttk.Entry(gui, width=30)
            self.entries[field].grid(
                row=(fields.index(field) + 2), column=1, sticky=tk.W
            )
            self.entries[field].insert(0, placeholders[fields.index(field)])
            if fields.index(field) == 0:
                self.entries[field].focus()
            ttk.Button(gui, text="Cadastrar", command=lambda: self.try_insert()).grid(
                row=len(fields) + 3, column=1, sticky=tk.W, pady=10
            )

    def insert_national_gui(self):
        self.origin = "national"
        gui = tk.Toplevel(self.root)
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
            _,
            state_taxes,
            _,
        ] = rand.ClassesData(self.database_name).vehicle_info()
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
        self.entries = {}
        # add a padding in the top
        space = tk.Frame(gui, height=15)
        space.grid(row=1, column=0)

        # fields
        for field in fields:
            tk.Label(gui, text=field, width=20, anchor="w").grid(
                row=fields.index(field) + 2, column=0
            )
            self.entries[field] = ttk.Entry(gui, width=30)
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

    def validate_vehicle_entries(self):
        errors = []

        plate = self.entries["Placa"].get()
        model = self.entries["Modelo"].get()
        manufacturer = self.entries["Fabricante"].get()
        fabrication_year = self.entries["Ano"].get()
        model_year = self.entries["Ano do Modelo"].get()
        category = self.entries["Categoria"].get()
        fipe_value = self.entries["Valor na FIPE"].get()
        rent_value = self.entries["Valor da Diária"].get()
        is_available = self.entries["Disponível [S/N]"].get()
        state_taxes = self.entries["Imposto Estadual"].get()

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
            if (
                int(fabrication_year) < 1900
                or int(fabrication_year) > datetime.now().year
            ):
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
        if self.origin == "imported":
            federal_taxes = self.entries["Imposto Federal"].get()
            if federal_taxes.isdigit():
                if float(federal_taxes) < 0 or float(federal_taxes) >= 1:
                    errors.append("Imposto Federal inválido")
        return errors

    def try_insert(self):
        errors = self.validate_vehicle_entries()
        if len(errors) > 0:
            for error in errors:
                tkmb.showerror("Erro", error)
        else:
            if self.origin == "imported":
                c.Controller(self.database_name).insert_vehicle(
                    vehicle.Imported(
                        self.entries["Placa"].get(),
                        self.entries["Modelo"].get(),
                        self.entries["Fabricante"].get(),
                        self.entries["Ano"].get(),
                        self.entries["Ano do Modelo"].get(),
                        self.entries["Categoria"].get(),
                        self.entries["Valor na FIPE"].get(),
                        self.entries["Valor da Diária"].get(),
                        self.entries["Disponível [S/N]"].get(),
                        self.entries["Imposto Estadual"].get(),
                        self.entries["Imposto Federal"].get(),
                    )
                ),
            else:
                c.Controller(self.database_name).insert_vehicle(
                    vehicle.National(
                        self.entries["Placa"].get(),
                        self.entries["Modelo"].get(),
                        self.entries["Fabricante"].get(),
                        self.entries["Ano"].get(),
                        self.entries["Ano do Modelo"].get(),
                        self.entries["Categoria"].get(),
                        self.entries["Valor na FIPE"].get(),
                        self.entries["Valor da Diária"].get(),
                        self.entries["Disponível [S/N]"].get(),
                        self.entries["Imposto Estadual"].get(),
                    )
                ),
            tkmb.showinfo("Sucesso", "Veículo cadastrado com sucesso!")

    def select_rented_vehicles_by_client_id(self):
        gui = tk.Toplevel(self.root)
        gui.title("Relatório de Veículos Alugados por Cliente")
        gui.geometry("420x125")
        obj.center(gui)

        label = tk.Label(gui, text="CPF do Cliente:", anchor="center")
        label.pack(pady=10)
        self.client = tk.StringVar(gui)
        clients = self.c.select_all_clients()
        self.client.set(f"{clients[0].get_cpf()} - {clients[0].get_name()}")
        op = tk.OptionMenu(
            gui,
            self.client,
            *[f"{c.get_cpf()} - {c.get_name()}" for c in clients],
        )
        op.config(width=30)
        op.pack()

        button = tk.Button(
            gui,
            text="Gerar Relatório",
            command=lambda: self.show_rented_vehicles(
                self.client.get().split(" - ")[0]
            ),
        )
        button.pack(pady=5)

    def show_rented_vehicles(self, cpf: str):
        vehicles = self.c.select_rented_vehicles_by_client(cpf)
        if len(vehicles) == 0:
            tkmb.showerror("Erro", "Cliente não possui veículos alugados")
        else:
            widgets.TextOutput(self.root).display(
                vehicles, "Veículos Alugados por Cliente"
            )
