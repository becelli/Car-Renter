import tkinter as tk
import controller.controller as controller
import view.classes.objects as obj
import view.classes.widgets as widgets
import view.vehicle as vg
import view.user as ugui
import view.rent as rgui
import view.insurance as insg
from PIL import ImageTk, Image


class Menubar:
    def __init__(self, window, db: str = "app.db"):
        self.c = controller.Controller(db)
        self.root = window
        self.user_gui = ugui.User(window, db)
        self.vehicle_gui = vg.Vehicle(window, db)
        self.rent_gui = rgui.Rent(window, db)
        self.insurance_gui = insg.Insurance(window, db)

        bar = tk.Menu(self.root, tearoff=0)
        self.root.config(menu=bar)
        vehicle_menu = tk.Menu(bar, tearoff=0)
        bar.add_cascade(label="Veículos", menu=vehicle_menu)
        self.vehicle_menu_options(vehicle_menu)
        self.textbox = widgets.TextOutput(self.root)

        user_menu = tk.Menu(bar, tearoff=0)
        bar.add_cascade(label="Usuários", menu=user_menu)
        self.user_menu_options(user_menu)

        rents_menu = tk.Menu(bar, tearoff=0)
        bar.add_cascade(label="Locações", menu=rents_menu)
        self.rents_menu_options(rents_menu)

        insurance_menu = tk.Menu(bar, tearoff=0)
        bar.add_cascade(label="Seguros", menu=insurance_menu)
        self.insurance_menu_options(insurance_menu)

    def vehicle_menu_options(self, menu):
        # Reports
        # TODO pass as parameter to vehicle view
        vehicles_reports = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Consultar", menu=vehicles_reports)
        vehicles_reports.add_command(
            label="Geral",
            command=lambda: self.textbox.display(
                self.c.select_all_vehicles(), "Todos os Veículos"
            ),
        )
        vehicles_reports.add_command(
            label="Nacionais",
            command=lambda: self.textbox.display(
                self.c.select_all_national_vehicles(), "Veículos Nacionais"
            ),
        )
        vehicles_reports.add_command(
            label="Importados",
            command=lambda: self.textbox.display(
                self.c.select_all_imported_vehicles(), "Veículos Importados"
            ),
        )
        vehicles_reports.add_command(
            label="Disponíveis",
            command=lambda: self.textbox.display(
                self.c.select_available_vehicles(), "Veículos Disponíveis"
            ),
        )
        vehicles_reports.add_command(
            label="Alugados",
            command=lambda: self.textbox.display(
                self.c.select_rented_vehicles(), "Veículos Alugados"
            ),
        )
        vehicles_reports.add_command(
            label="Não Devolvidos",
            command=lambda: self.textbox.display(
                self.c.select_not_returned_vehicles(), "Veículos Não Devolvidos"
            ),
        )
        # TODO Listar todos os Veículos já locados por um Cliente em específico.
        vehicles_reports.add_command(
            label="Locados por Cliente",
            command=lambda: self.vehicle_gui.select_rented_vehicles_by_client_id(),
        )

        vehicle_options = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Cadastrar", menu=vehicle_options)

        vehicle_options.add_command(
            label="Nacional",
            command=lambda: self.vehicle_gui.insert_national_gui(),
        )
        vehicle_options.add_command(
            label="Importado",
            command=lambda: self.vehicle_gui.insert_imported_gui(),
        )
        # TODO menu.add_command(label="Alterar", command=lambda: self.vehicle_gui.update_vehicle(menu))
        # TODO menu.add_command(label="Excluir", command=lambda: self.vehicle_gui.delete_vehicle(menu))

    def user_menu_options(self, menu):
        # Employee submenu
        employees = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Funcionários", menu=employees)

        employees_reports = tk.Menu(employees, tearoff=0)
        employees.add_cascade(label="Consultar", menu=employees_reports)

        employees_reports.add_command(
            label="Todos",
            command=lambda: self.textbox.display(
                self.c.select_all_employees(), "Todos os Funcionários"
            ),
        )
        employees_reports.add_command(
            label="Funcionário do mês",
            command=lambda: self.user_gui.select_employee_of_the_month(),
        )
        employees.add_command(
            label="Cadastrar",
            command=lambda: self.user_gui.insert_employee_gui(),
        )
        # TODO employees.add_command(label="Alterar", command=lambda: userg.update_employee())
        # TODO employees.add_command(label="Excluir", command=lambda: userg.delete_employee())

        # Clients Submenu
        clients = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Clientes", menu=clients)
        clients_reports = tk.Menu(clients, tearoff=0)
        clients.add_cascade(label="Consultar", menu=clients_reports)

        clients_reports.add_command(
            label="Todos",
            command=lambda: self.textbox.display(self.c.select_all_clients()),
        )
        clients_reports.add_command(
            label="Histórico de locações",
            command=lambda: self.user_gui.select_client_rent_history(),
        )
        clients_reports.add_command(
            label="Locações em atraso",
            command=lambda: self.user_gui.select_expired_rents_of_client(),
        )

        # Other options
        clients.add_command(
            label="Cadastrar", command=lambda: self.user_gui.insert_client_gui()
        )
        # TODO clients.add_command(label="Alterar", command=lambda: userg.update_client())
        # TODO clients.add_command(label="Excluir", command=lambda: userg.delete_client())

    def rents_menu_options(self, menu):
        rents_reports = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Consultar", menu=rents_reports)

        rents_reports.add_command(
            label="Todas",
            command=lambda: self.textbox.display(
                self.c.select_all_rents(), "Todas as Locações"
            ),
        )
        rents_reports.add_command(
            label="Finalizadas",
            command=lambda: self.textbox.display(
                self.c.select_all_finished_rents(), "Locações Finalizadas"
            ),
        )
        rents_reports.add_command(
            label="Em andamento",
            command=lambda: self.textbox.display(
                self.c.select_all_ongoing_rents(), "Locações em Andamento"
            ),
        )
        rents_reports.add_command(
            label="Em atraso",
            command=lambda: self.textbox.display(
                self.c.select_all_expired_rents(), "Locações em Atraso"
            ),
        )
        rents_reports.add_command(
            label="Realizadas no mês",
            command=lambda: self.rent_gui.select_monthly_rents(),
        )
        menu.add_command(
            label="Devolver",
            command=lambda: self.rent_gui.return_vehicle_gui(),
        )
        menu.add_command(
            label="Cadastrar",
            command=lambda: self.rent_gui.insert_rent_gui(),
        )
        # TODO menu.add_command(label="Alterar", command=lambda: rentg.update_rent())

    def insurance_menu_options(self, menu):
        menu.add_command(
            label="Consultar",
            command=lambda: self.textbox.display(
                self.c.select_all_insurances(), "Todos os Seguros"
            ),
        )
        menu.add_command(
            label="Cadastrar", command=lambda: self.insurance_gui.insert_insurance_gui()
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

    img = ImageTk.PhotoImage(
        Image.open("./view/assets/logo.png").resize((350, 350), Image.ANTIALIAS)
    )

    panel = tk.Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")

    app = Application(root, db)
    app.root.mainloop()
