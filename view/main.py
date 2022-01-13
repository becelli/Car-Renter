import tkinter as tk
import controller.controller as controller
import view.classes.objects as obj
import view.classes.widgets as widgets
import view.vehicle as vehg
import view.user as userg
import view.rent as rentg
import view.insurance as insg


class Menubar:
    def __init__(self, window, db: str = "app.db"):
        self.c = controller.Controller(db)
        self.root = window
        bar = tk.Menu(self.root, tearoff=0)
        self.root.config(menu=bar)
        vehicle_menu = tk.Menu(bar, tearoff=0)
        bar.add_cascade(label="Veículos", menu=vehicle_menu)
        self.vehicle_menu_options(vehicle_menu, db)
        self.textbox = widgets.TextOutput(self.root)

        user_menu = tk.Menu(bar, tearoff=0)
        bar.add_cascade(label="Usuários", menu=user_menu)
        self.user_menu_options(user_menu, db)

        rents_menu = tk.Menu(bar, tearoff=0)
        bar.add_cascade(label="Locações", menu=rents_menu)
        self.rents_menu_options(rents_menu, db)

        insurance_menu = tk.Menu(bar, tearoff=0)
        bar.add_cascade(label="Seguros", menu=insurance_menu)
        self.insurance_menu_options(insurance_menu, db)

    def vehicle_menu_options(self, menu, db: str = "app.db"):
        # Reports
        # TODO pass as parameter to vehicle view
        vehicles_reports = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Consultar", menu=vehicles_reports)
        vehicles_reports.add_command(
            label="Geral",
            command=lambda: self.textbox.display(lambda: self.c.select_all_vehicles()),
        )
        vehicles_reports.add_command(
            label="Nacionais",
            command=lambda: print(self.c.select_all_national_vehicles()),
        )
        vehicles_reports.add_command(
            label="Importados",
            command=lambda: print(self.c.select_all_imported_vehicles()),
        )
        vehicles_reports.add_command(
            label="Disponíveis",
            command=lambda: print(self.c.select_available_vehicles()),
        )
        vehicles_reports.add_command(
            label="Alugados", command=lambda: print(self.c.select_rented_vehicles())
        )
        vehicles_reports.add_command(
            label="Não Devolvidos",
            command=lambda: print(self.c.select_not_returned_vehicles()),
        )
        # TODO Listar todos os Veículos já locados por um Cliente em específico.
        vehicles_reports.add_command(
            label="Locados por Cliente",
            command=lambda: vehg.select_rented_vehicles_by_client_id(),
        )

        vehicle_options = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Cadastrar", menu=vehicle_options)

        vehicle_options.add_command(
            label="Nacional", command=lambda: vehg.insert_national_gui(menu, db)
        )
        vehicle_options.add_command(
            label="Importado", command=lambda: vehg.insert_imported_gui(menu, db)
        )
        # TODO menu.add_command(label="Alterar", command=lambda: vehg.update_vehicle(menu))
        # TODO menu.add_command(label="Excluir", command=lambda: vehg.delete_vehicle(menu))

    def user_menu_options(self, menu, db: str = "app.db"):
        # Employee submenu
        employees = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Funcionários", menu=employees)

        employees_reports = tk.Menu(employees, tearoff=0)
        employees.add_cascade(label="Consultar", menu=employees_reports)

        employees_reports.add_command(
            label="Todos", command=lambda: print(self.c.select_all_employees())
        )
        employees_reports.add_command(
            label="Funcionário do mês",
            command=lambda: self.c.select_employee_of_month(),
        )
        employees.add_command(
            label="Cadastrar", command=lambda: userg.insert_employee_gui(menu, db)
        )
        # TODO employees.add_command(label="Alterar", command=lambda: userg.update_employee())
        # TODO employees.add_command(label="Excluir", command=lambda: userg.delete_employee())

        # Clients Submenu
        clients = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Clientes", menu=clients)
        clients_reports = tk.Menu(clients, tearoff=0)
        clients.add_cascade(label="Consultar", menu=clients_reports)

        clients_reports.add_command(
            label="Todos", command=lambda: print(self.c.select_all_clients())
        )
        clients_reports.add_command(
            label="Histórico de locações", command=lambda: userg.select_client_rents()
        )
        clients_reports.add_command(
            label="Locações em atraso",
            command=lambda: self.c.select_client_expired_rents(),
        )

        # Other options
        clients.add_command(
            label="Cadastrar", command=lambda: userg.insert_client_gui(menu, db)
        )
        # TODO clients.add_command(label="Alterar", command=lambda: userg.update_client())
        # TODO clients.add_command(label="Excluir", command=lambda: userg.delete_client())

    def rents_menu_options(self, menu, db: str = "app.db"):
        rents_reports = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Consultar", menu=rents_reports)

        rents_reports.add_command(
            label="Todas", command=lambda: print(self.c.select_all_rents())
        )
        rents_reports.add_command(
            label="Finalizadas",
            command=lambda: print(self.c.select_all_finished_rents()),
        )
        rents_reports.add_command(
            label="Em andamento",
            command=lambda: print(self.c.select_all_ongoing_rents()),
        )
        rents_reports.add_command(
            label="Em atraso", command=lambda: print(self.c.select_all_expired_rents())
        )
        rents_reports.add_command(
            label="Realizadas no mês", command=lambda: rentg.select_monthly_rents()
        )
        menu.add_command(
            label="Cadastrar", command=lambda: rentg.insert_rent_gui(menu, db)
        )
        # TODO menu.add_command(label="Alterar", command=lambda: rentg.update_rent())

    def insurance_menu_options(self, menu, db: str = "app.db"):
        menu.add_command(
            label="Consultar", command=lambda: print(self.c.select_all_insurances())
        )
        menu.add_command(
            label="Cadastrar", command=lambda: insg.insert_insurance_gui(menu, db)
        )
        # TODO menu.add_command(label="Alterar", command=lambda: insg.update_insurance())
        # TODO menu.add_command(label="Excluir", command=lambda: insg.delete_insurance())


class Application(tk.Frame):
    def __init__(self, master=None, db: str = "app.db"):
        self.root = master
        super().__init__(master, borderwidth=0, relief=tk.RAISED)

        self.root.title("Renterio - Sistema de Locações de Veículos")
        self.root.geometry("600x400")
        obj.center(self.root)
        self.pack_propagate(False)
        self.pack()
        Menubar(self.root, db)


def main(db):
    root = tk.Tk()
    app = Application(root, db)
    app.root.mainloop()
