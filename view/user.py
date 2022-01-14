import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import ttk
import controller.controller as c
import model.classes.random as rand
import view.classes.objects as obj
from datetime import datetime
import model.classes.user as user
import view.classes.widgets as widgets


class User:
    def __init__(self, root, db: str = "app.db"):
        self.database_name = db
        self.c = c.Controller(db)
        self.root = root

    def insert_employee_gui(self):
        self.role = "employee"
        gui = tk.Toplevel(self.root)
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
            cpf,
            rg,
            name,
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
        ] = rand.ClassesData(self.database_name).user_info()
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
            btn = ttk.Button(gui, text="Cadastrar", command=lambda: self.try_insert())
            btn.grid(row=len(fields) + 3, column=1, sticky=tk.W, pady=10)

    def insert_client_gui(self):
        self.role = "client"
        gui = tk.Toplevel(self.root)
        gui.title("Cadastro de Cliente")
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
            "Carta [A/B/C/D/E]",
            "Nº da CNH",
            "Expiração da CNH",
            "Cliente Ouro [S/N]",
        )
        [
            cpf,
            rg,
            name,
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
        ] = rand.ClassesData(self.database_name).user_info()
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
            btn = ttk.Button(gui, text="Cadastrar", command=lambda: self.try_insert())
            btn.grid(row=len(fields) + 3, column=1, sticky=tk.W, pady=10)

    def validate_user_entries(self):
        errors = []
        name = self.entries["Nome"].get()
        for i in range(len(name)):
            if name[i].isdigit():
                errors.append("Nome não pode conter números")
                break
        if len(name) < 3:
            errors.append("Nome deve conter no mínimo 3 caracteres")

        cpf = self.entries["CPF"].get()
        if len(cpf) != 11:
            errors.append("CPF deve conter 11 caracteres")
        for i in range(len(cpf)):
            if not cpf[i].isdigit():
                errors.append("CPF deve conter apenas números")
                break
        rg = self.entries["RG"].get()
        if len(rg) != 9:
            errors.append("RG deve conter 9 caracteres")
        for i in range(len(rg)):
            if not rg[i].isdigit():
                errors.append("RG deve conter apenas números")
                break

        birth_date = self.entries["Data de Nascimento"].get()
        if birth_date is None:
            errors.append("Data de Nascimento não pode ser vazia")
        if len(birth_date) != 10:
            errors.append("Data de Nascimento deve conter 10 caracteres")
        if birth_date[4] != "-" or birth_date[7] != "-":
            errors.append("Data de Nascimento deve estar no formato AAAA-MM-DD")

        address = self.entries["Endereço"].get()
        if len(address) < 5:
            errors.append("Endereço deve conter no mínimo 5 caracteres")

        zip_code = self.entries["CEP"].get()
        if len(zip_code) != 9:
            errors.append("CEP deve conter 9 caracteres")

        email = self.entries["Email"].get()
        if email is None:
            errors.append("Email cannot be empty")
        if "@" not in email:
            errors.append("Email must contain @")
        if "." not in email:
            errors.append("Email must contain .")
        if email.count("@") > 1:
            errors.append("Email must contain only one @")

        if self.role == "employee":

            salary = self.entries["Salário"].get()
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

            pis = self.entries["PIS"].get()
            if len(pis) != 11:
                errors.append("PIS deve conter 11 caracteres")

            admission_date = self.entries["Data de Admissão"].get()
            if len(admission_date) != 10:
                errors.append("Data de Admissão deve conter 10 caracteres")
            try:
                aux = datetime.strptime(admission_date, "%Y-%m-%d")
                if aux > datetime.now():
                    errors.append(
                        "Data de Admissão não pode ser maior que a data atual"
                    )
            except:
                errors.append("Data de Admissão deve estar no formato AAAA-MM-DD")

        if self.role == "client":
            permission_category = self.entries["Carta [A/B/C/D/E]"].get()
            if permission_category is None:
                errors.append("Carta não pode ser vazia")
            if len(permission_category) != 1:
                errors.append("Carta deve conter apenas um caractere")
            if permission_category not in ["A", "B", "C", "D", "E"]:
                errors.append("Carta deve ser A, B, C, D ou E")

            permission_number = self.entries["Nº da CNH"].get()
            if len(permission_number) != 10:
                errors.append("Nº da CNH deve conter 10 caracteres")
            for i in range(len(permission_number)):
                if not permission_number[i].isdigit():
                    errors.append("Nº da CNH deve conter apenas números")
                    break
            permission_expiration = self.entries["Expiração da CNH"].get()
            if len(permission_expiration) != 7:
                errors.append("Expiração da CNH deve conter 7 caracteres")
            try:
                aux = datetime.strptime(permission_expiration, "%Y-%m")
                if aux < datetime.now():
                    errors.append(
                        "Expiração da CNH não pode ser menor que a data atual"
                    )
            except ValueError:
                errors.append("Expiração da CNH deve estar no formato AAAA-MM")

            is_golden_client = self.entries["Cliente Ouro [S/N]"].get()
            if is_golden_client is None:
                errors.append("Cliente Ouro não pode ser vazio")
            if len(is_golden_client) != 1:
                errors.append("Cliente Ouro deve conter apenas um caractere")
            if is_golden_client not in ["S", "N"]:
                errors.append("Cliente Ouro deve ser S ou N")
        return errors

    def try_insert(self):
        errors = self.validate_user_entries()
        if len(errors) > 0:
            for error in errors:
                tkmb.showerror("Erro", error)
        else:
            if self.role == "employee":
                self.c.insert_user(
                    user.Employee(
                        self.entries["Nome"].get(),
                        str(self.entries["CPF"].get()),
                        str(self.entries["RG"].get()),
                        datetime.strptime(
                            self.entries["Data de Nascimento"].get(), "%Y-%m-%d"
                        ),
                        self.entries["Endereço"].get(),
                        str(self.entries["CEP"].get()),
                        self.entries["Email"].get(),
                        float(self.entries["Salário"].get()),
                        str(self.entries["PIS"].get()),
                        datetime.strptime(
                            self.entries["Data de Admissão"].get(), "%Y-%m-%d"
                        ),
                    )
                )
            elif type == "client":
                self.c.insert_user(
                    user.Client(
                        self.entries["Nome"].get(),
                        str(self.entries["CPF"].get()),
                        str(self.entries["RG"].get()),
                        datetime.strptime(
                            self.entries["Data de Nascimento"].get(), "%Y-%m-%d"
                        ),
                        self.entries["Endereço"].get(),
                        str(self.entries["CEP"].get()),
                        self.entries["Email"].get(),
                        self.entries["Carta [A/B/C/D/E]"].get(),
                        str(self.entries["Nº da CNH"].get()),
                        datetime.strptime(
                            self.entries["Expiração da CNH"].get(), "%Y-%m"
                        ),
                        self.entries["Cliente Ouro [S/N]"].get() == "S",
                    )
                )
            tkmb.showinfo("Sucesso", "Usuário cadastrado com sucesso")

    def select_employee_of_the_month(self):
        gui = tk.Toplevel(self.root)
        gui.title("Relatório Mensal")
        gui.geometry("400x125")
        obj.center(gui)

        tk.Label(gui, text="Mês (AAAA-MM)").pack(pady=10)
        self.month = tk.Entry(gui, width=30)
        self.month.insert(0, datetime.today().strftime("%Y-%m"))
        self.month.pack()

        btn = tk.Button(
            gui,
            text="Gerar Relatório",
            command=lambda: self.show_employee(
                self.c.select_employee_of_the_month(
                    self.parse_date(self.month.get(), "%Y-%m")
                )
            ),
        )
        btn.pack(pady=10)

    def show_employee(self, cpf_and_sells):
        cpf = cpf_and_sells[0]
        sells = cpf_and_sells[1]
        widgets.TextOutput(self.root).display(
            str(self.c.select_employee(cpf)) + f"\nTotal de vendas: {sells}",
            "Funcionário do Mês",
        ),

    def parse_date(self, date: str, format: str) -> datetime:
        try:
            return datetime.strptime(date, format)
        except ValueError:
            tkmb.showerror("Erro", "Data inválida")

    def select_client_rent_history(self):
        gui = tk.Toplevel(self.root)
        gui.title("Relatório de Locações por Cliente")
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
            command=lambda: self.show_rent_history(self.client.get().split(" - ")[0]),
        )
        button.pack(pady=5)

    def show_rent_history(self, cpf: str):
        vehicles = self.c.select_rent_history_of(cpf)
        if len(vehicles) == 0:
            tkmb.showerror("Aviso", "Cliente não possui locações até o momento")
        else:
            widgets.TextOutput(self.root).display(
                vehicles,
                "Histórico de Locações",
            )

    def select_expired_rents_of_client(self):
        gui = tk.Toplevel(self.root)
        gui.title("Relatório de Locações em Atraso")
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
            command=lambda: self.show_expired_rents(self.client.get().split(" - ")[0]),
        )
        button.pack(pady=5)

    def show_expired_rents(self, cpf: str):
        vehicles = self.c.select_expired_rents_of(cpf)
        if len(vehicles) == 0:
            tkmb.showwarning("Aviso", "Cliente não possui locações em atraso")
        else:
            widgets.TextOutput(self.root).display(
                vehicles,
                "Histórico de Locações em Atraso",
            )
