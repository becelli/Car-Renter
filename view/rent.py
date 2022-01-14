from datetime import datetime, timedelta
from functools import total_ordering
import random as rd
import tkinter as tk
import tkinter.messagebox as tkmb
import controller.controller as controller
from model.classes.insurance import Insurance
import view.classes.objects as obj


class ViewRent:
    def __init__(self, root, db):
        self.root = root
        self.c = controller.Controller(db)

    def insert_rent_gui(self):
        self.gui1 = tk.Toplevel(self.root)
        self.gui1.title("Cadastro de Locações")
        self.gui1.geometry("500x180")
        obj.center(self.gui1)

        self.plate_input(self.gui1)
        self.client_input(self.gui1)
        self.employee_input(self.gui1)
        self.start_date_input(self.gui1)
        self.end_date_input(self.gui1)
        btn = tk.Button(
            self.gui1,
            text="Cadastrar",
            command=lambda: self.validate_and_insurances(),
            width=20,
            height=2,
        )
        btn.grid(row=5, column=1)

    def validate_and_insurances(self):
        entries = {
            "Placa": self.plate.get()[0:8],
            "CPF": self.client.get()[0:11],
            "CPF_Funcionário": self.employee.get()[0:11],
            "Data_Início": self.start_date.get()[0:10],
            "Data_Devolução": self.end_date.get()[0:10],
        }
        validate = self.validate_rent_input(entries)
        if validate == "success":
            self.choose_insurance()

    def validate_rent_input(self, input):
        errors = []
        if input["Placa"] == "":
            errors.append("Placa não pode ser vazia")
        if len(input["Placa"]) > 0 and len(input["Placa"]) != 8:
            errors.append("Placa deve conter 8 caracteres")
        for i in range(len(input["Placa"])):
            if i < 3:
                if not input["Placa"][i].isalpha():
                    errors.append("Placa deve estar no formato ABC-1234")
                    break
            elif i == 3:
                if not input["Placa"][i] == "-":
                    errors.append("Placa deve estar no formato ABC-1234")
                    break
            else:
                if not input["Placa"][i].isdigit():
                    errors.append("Placa deve estar no formato ABC-1234")
                    break
        if input["CPF"] == "":
            errors.append("CPF não pode ser vazio")
        if len(input["CPF"]) > 0 and len(input["CPF"]) != 11:
            errors.append("CPF deve conter 11 caracteres")
        for i in range(len(input["CPF"])):
            if not input["CPF"][i].isdigit():
                errors.append("CPF deve conter apenas números")
                break
        if input["CPF_Funcionário"] == "":
            errors.append("CPF não pode ser vazio")
        if len(input["CPF_Funcionário"]) > 0 and len(input["CPF_Funcionário"]) != 11:
            errors.append("CPF deve conter 11 caracteres")
        for i in range(len(input["CPF_Funcionário"])):
            if not input["CPF_Funcionário"][i].isdigit():
                errors.append("CPF deve conter apenas números")
                break
        if input["Data_Início"] == "":
            errors.append("Data de Início não pode ser vazia")
        if input["Data_Início"] != "":
            try:
                datetime.strptime(input["Data_Início"], "%Y-%m-%d")
            except ValueError:
                errors.append("Data de Início inválida")
        if input["Data_Devolução"] == "":
            errors.append("Data de Devolução não pode ser vazia")
        if input["Data_Devolução"] != "":
            try:
                datetime.strptime(input["Data_Devolução"], "%Y-%m-%d")
            except ValueError:
                errors.append("Data de Devolução inválida")
        if input["Data_Início"] != "" and input["Data_Devolução"] != "":
            try:
                if datetime.strptime(
                    input["Data_Início"], "%Y-%m-%d"
                ) > datetime.strptime(input["Data_Devolução"], "%Y-%m-%d"):
                    errors.append(
                        "Data de Início não pode ser maior que Data de Devolução"
                    )
            except ValueError:
                pass

        if len(errors) > 0:
            for error in errors:
                tkmb.showerror("Erro", error)
            return "error"
        return "success"

    def choose_insurance(self):
        gui = tk.Toplevel(self.root)
        gui.title("Escolha de Seguros")
        gui.geometry("500x300")
        obj.center(gui)
        insurances = self.c.select_all_insurances()

        l = tk.Label(gui, text="Seguros disponíveis:", anchor="w")
        l.config(pady=10, font=("Helvetica Bold", 12))
        l.pack()
        self.checked = []
        for i in range(len(insurances)):
            self.checked.append(tk.IntVar())
            c1 = tk.Checkbutton(
                gui,
                text=f"{insurances[i].get_name()} - {insurances[i].get_description()} - {insurances[i].get_value()}",
                variable=self.checked[i],
                onvalue=1,
                offvalue=0,
            )
            c1.config(anchor="w", pady=5)
            c1.pack()

        btn = tk.Button(
            gui,
            text="Confirmar",
            command=lambda: self.payment_gui(),
            width=20,
            height=2,
        )
        btn.pack()

    def payment_gui(self):
        # Get the real values of the checkboxes
        for i in range(len(self.checked)):
            self.checked[i] = self.checked[i].get()
        gui = tk.Toplevel(self.root)
        gui.title("Pagamento")
        gui.geometry("500x160")
        obj.center(gui)
        l = tk.Label(gui, text="Escolha o método de pagamento:", anchor="w")
        l.config(pady=10, font=("Helvetica Bold", 12))
        l.pack()

        vehicle = self.c.select_vehicle(self.plate.get()[0:8])
        total_value = (
            vehicle.calculate_daily_rent_value()
            * (
                datetime.strptime(self.end_date.get()[0:10], "%Y-%m-%d")
                - datetime.strptime(self.start_date.get()[0:10], "%Y-%m-%d")
            ).days
        )

        insurances = self.c.select_all_insurances()
        import model.classes.insurance as insurance

        for i in insurances:
            i: insurance.Insurance = i
            if self.checked[insurances.index(i)] == 1:
                total_value += i.get_value()
        self.total_value = round(total_value, 2)

        l = tk.Label(gui, text="Valor total: R$" + str(self.total_value), anchor="w")
        l.pack()
        ccbtn = tk.Button(
            gui,
            text="Cartão de Crédito",
            command=lambda: self.credit_card_gui(),
            width=20,
            height=2,
        )
        ccbtn.pack()
        ccb = tk.Button(
            gui,
            text="Dinheiro",
            command=lambda: self.cash_gui(),
            width=20,
            height=2,
        )
        ccb.pack()

    def display_options(self, payment_method):
        if payment_method == "Cartão de Crédito":
            self.credit_card_gui()
        elif payment_method == "Dinheiro":
            self.cash_gui()

    def credit_card_gui(self):
        gui = tk.Toplevel(self.root)
        gui.title("Cartão de Crédito")
        gui.geometry("350x275")
        obj.center(gui)
        import model.classes.random as random

        l = tk.Label(gui, text="Nome do Titular:", anchor="w")
        l.config(pady=10)
        l.pack()
        self.card_name = tk.Entry(gui, width=30)
        self.card_name.insert(
            0, self.c.select_client(self.client.get()[0:11]).get_name()
        )
        self.card_name.pack()

        l = tk.Label(gui, text="Número do Cartão:", anchor="w")
        l.config(pady=10)
        l.pack()

        self.card_num = tk.Entry(gui, width=30)
        card_info = random.Formats().nsize_num_as_str(16)
        self.card_num.insert(0, card_info)
        self.card_num.pack()

        l = tk.Label(gui, text="Bandeira do Cartão:", anchor="w")
        l.config(pady=10)
        l.pack()

        self.card_flag = tk.Entry(gui, width=30)
        flag = random.BasicData().card_flag()
        self.card_flag.insert(0, flag)
        self.card_flag.pack()

        btn = tk.Button(
            gui,
            text="Confirmar",
            command=lambda: self.try_insert("card"),
            width=20,
            height=2,
            pady=10,
        )
        btn.pack()

    def cash_gui(self):
        gui = tk.Toplevel(self.root)
        gui.title("Dinheiro")
        gui.geometry("500x150")
        obj.center(gui)

        l = tk.Label(gui, text="Pagar com dinheiro", anchor="w")
        l.config(pady=10)
        l.pack()

        btn = tk.Button(
            gui,
            text="Confirmar",
            command=lambda: self.try_insert("cash"),
            width=20,
            height=2,
        )
        btn.pack()

    def try_insert(self, payment_method):
        import model.classes.rent as rent
        import model.classes.payment as payment

        if payment_method == "card":
            self.payment = payment.Card(
                self.card_name.get(),
                self.card_num.get(),
                self.card_flag.get(),
            )
        elif payment_method == "cash":
            self.payment = payment.Cash("Dinheiro")
        new_rent = rent.Rent(
            self.plate.get()[0:8],
            self.client.get()[0:11],
            self.employee.get()[0:11],
            datetime.strptime(self.start_date.get()[0:10], "%Y-%m-%d"),
            datetime.strptime(self.end_date.get()[0:10], "%Y-%m-%d"),
            self.total_value,
            self.payment,
            self.checked,
        )
        self.c.insert_payment(self.payment)
        self.c.insert_rent(new_rent)
        tkmb.showinfo("Pagamento", "Pagamento confirmado")

    def plate_input(self, root) -> str:
        label = tk.Label(root, text="Placa do veículo:", anchor="w")
        label.grid(row=0, column=0)
        self.plate = tk.StringVar(root)
        available_vehicles = self.c.select_all_available_vehicles()
        self.plate.set(
            f"{available_vehicles[0].get_plate()} - {available_vehicles[0].get_model()} - Diária: {available_vehicles[0].calculate_daily_rent_value()}"
        )
        op = tk.OptionMenu(
            root,
            self.plate,
            *[
                f"{v.get_plate()} - {v.get_model()} - Diária: {v.calculate_daily_rent_value()}"
                for v in available_vehicles
            ],
        )
        op.config(width=30)
        op.grid(row=0, column=1)

    def client_input(self, root) -> str:
        label = tk.Label(root, text="CPF do Cliente:", anchor="w")
        label.grid(row=1, column=0)
        self.client = tk.StringVar(root)
        clients = self.c.select_all_clients()
        self.client.set(f"{clients[0].get_cpf()} - {clients[0].get_name()}")
        op = tk.OptionMenu(
            root,
            self.client,
            *[f"{c.get_cpf()} - {c.get_name()}" for c in clients],
        )
        op.config(width=30)
        op.grid(row=1, column=1)

    def employee_input(self, root) -> str:
        label = tk.Label(root, text="CPF do Funcionário:", anchor="w")
        label.grid(row=2, column=0)
        self.employee = tk.StringVar(root)
        employees = self.c.select_all_employees()
        self.employee.set(f"{employees[0].get_cpf()} - {employees[0].get_name()}")
        op = tk.OptionMenu(
            root,
            self.employee,
            *[f"{e.get_cpf()} - {e.get_name()}" for e in employees],
        )
        op.config(width=30)
        op.grid(row=2, column=1)

    def start_date_input(self, root):
        label = tk.Label(root, text="Data de Início: (AAAA-MM-DD)", anchor="w")
        label.grid(row=3, column=0)
        self.start_date = tk.StringVar(root)
        self.start_date.set(datetime.today().strftime("%Y-%m-%d"))
        op = tk.Entry(root, textvariable=self.start_date)
        op.config(width=30)
        op.grid(row=3, column=1)

    def end_date_input(self, root):
        label = tk.Label(root, text="Data da Devolução: (AAAA-MM-DD)", anchor="w")
        label.grid(row=4, column=0)
        self.end_date = tk.StringVar(root)
        self.end_date.set(
            (datetime.today() + timedelta(days=rd.randint(1, 14))).strftime("%Y-%m-%d")
        )
        op = tk.Entry(root, textvariable=self.end_date, width=30)
        op.config(width=30)
        op.grid(row=4, column=1)

    # RETURN

    def return_vehicle_gui(self):
        import model.classes.rent as rent
        import model.classes.user as user

        r_late = self.c.select_all_expired_rents()
        r_ongoing = self.c.select_all_ongoing_rents()
        all_rents = r_late + r_ongoing
        listing = []
        for i in range(len(r_late)):
            r: rent.Rent = r_late[i]
            u: user.Client = self.c.select_client(r.get_client_cpf())
            listing.append(
                f"ATRASADA - {r.get_vehicle_plate()} - {u.get_name()} - Vencido desde: {str(r.get_end_date())[0:10]}"
            )
        for i in range(len(r_ongoing)):
            r: rent.Rent = r_ongoing[i]
            u: user.Client = self.c.select_client(r.get_client_cpf())
            listing.append(
                f"{r.get_vehicle_plate()} - {u.get_name()} - Até: {str(r.get_end_date())[0:10]}"
            )
        if len(listing) > 0:
            gui = tk.Toplevel(self.root)
            gui.title("Devolução de Veículos")
            gui.geometry("650x150")
            obj.center(gui)

            tk.Label(gui, text="Veículo:").pack(pady=10)
            variable = tk.StringVar(gui)
            variable.set(str(listing[0]))
            w = tk.OptionMenu(gui, variable, *listing)
            w.config(padx=5, font=("Helvetica", 10))
            w.pack(pady=10)
            tk.Button(
                gui,
                text="Devolver",
                command=lambda: self.return_vehicle(gui, all_rents, listing, variable),
            ).pack(pady=10)

    def return_vehicle(
        self,
        root,
        rents: list,
        r_listing: list,
        option: str,
    ):
        for i in r_listing:
            if str(i) == str(option.get()):
                import model.classes.rent as rent

                index = r_listing.index(i)
                r: rent.Rent = rents[index]
                self.c.return_vehicle(r.get_id())
                root.destroy()
