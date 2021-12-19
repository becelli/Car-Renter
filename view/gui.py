from tkinter import *
from tkinter import ttk
import controller.controller as c
import view.vehicle as v


def __main__():
    init()


def init():
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    root.geometry("1280x720")
    root.title("Renterio - Sistema de Locações de Veículos")
    # stgrt from here
    create_menu_bar(root)

    # show gui
    root.mainloop()


def create_menu_bar(root):
    # create menu bar
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    # create menu bar entries
    vehicle_menu = Menu(menu_bar)
    menu_bar.add_cascade(label="Veículos", menu=vehicle_menu)
    vehicle_menu_options(vehicle_menu)

    user_menu = Menu(menu_bar)
    menu_bar.add_cascade(label="Usuários", menu=user_menu)
    user_menu_options(user_menu)

    rental_menu = Menu(menu_bar)
    menu_bar.add_cascade(label="Locações", menu=rental_menu)
    rental_menu_options(rental_menu)

    insurance_menu = Menu(menu_bar)
    menu_bar.add_cascade(label="Seguros", menu=insurance_menu)
    insurance_menu_options(insurance_menu)


def vehicle_menu_options(menu):
    # Reports
    # TODO pass as parameter to vehicle view
    vehicles_reports = Menu(menu)
    menu.add_cascade(label="Consultar", menu=vehicles_reports)
    vehicles_reports.add_command(
        label="Geral", command=lambda: print(c.select_all_vehicles())
    )
    # vehicles_reports.add_command(
    #     label="Nacionais", command=lambda: print(c.select_all_national_vehicles())
    # )
    # vehicles_reports.add_command(
    #     label="Importados", command=lambda: print(c.select_all_imported_vehicles())
    # )
    # vehicles_reports.add_command(
    #     label="Disponíveis", command=lambda: print(c.select_all_available_vehicles())
    # )
    # vehicles_reports.add_command(
    #     label="Alugados", command=lambda: print(c.select_all_rented_vehicles())
    # )
    # vehicles_reports.add_command(
    #     label="Não Devolvidos",
    #     command=lambda: print(c.select_all_not_returned_vehicles()),
    # )
    # TODO Listar todos os Veículos já locados por um Cliente em específico.
    vehicles_reports.add_command(
        label="Locados por Cliente",
        command=lambda: c.select_all_rented_vehicles_by_client_id(),
    )
    # Other options
    menu.add_command(label="Cadastrar", command=lambda: v.create_vehicle())
    menu.add_command(label="Alterar", command=lambda: v.update_vehicle())
    menu.add_command(label="Excluir", command=lambda: v.delete_vehicle())


def user_menu_options(menu):
    # Employee submenu
    employees = Menu(menu)
    menu.add_cascade(label="Funcionários", menu=employees)

    employees_reports = Menu(employees)
    employees.add_cascade(label="Consultar", menu=employees_reports)

    employees_reports.add_command(
        label="Todos", command=lambda: print(c.select_all_employees())
    )
    employees_reports.add_command(
        label="Funcionário do mês", command=lambda: c.select_employee_of_month()
    )
    employees.add_command(label="Cadastrar", command=lambda: v.create_user())
    employees.add_command(label="Alterar", command=lambda: v.update_user())
    employees.add_command(label="Excluir", command=lambda: v.delete_user())

    # Clients Submenu
    clients = Menu(menu)
    menu.add_cascade(label="Clientes", menu=clients)
    clients_reports = Menu(clients)
    clients.add_cascade(label="Consultar", menu=clients_reports)

    clients_reports.add_command(
        label="Todos", command=lambda: print(c.select_all_clients())
    )
    clients_reports.add_command(
        label="Histórico de locações", command=lambda: c.select_client_rentals()
    )
    clients_reports.add_command(
        label="Locações em atraso", command=lambda: c.select_client_late_rentals()
    )

    # Other options
    clients.add_command(label="Cadastrar", command=lambda: v.create_user())
    clients.add_command(label="Alterar", command=lambda: v.update_user())
    clients.add_command(label="Excluir", command=lambda: v.delete_user())


def rental_menu_options(menu):
    rentals_reports = Menu(menu)
    menu.add_cascade(label="Consultar", menu=rentals_reports)

    rentals_reports.add_command(
        label="Todas", command=lambda: print(c.select_all_rentals())
    )
    rentals_reports.add_command(
        label="Finalizadas", command=lambda: c.select_all_finished_rentals()
    )
    rentals_reports.add_command(
        label="Em andamento", command=lambda: c.select_all_ongoing_rentals()
    )
    rentals_reports.add_command(
        label="Em atraso", command=lambda: c.select_late_rentals()
    )
    rentals_reports.add_command(
        label="Realizadas no mês", command=lambda: c.select_monthly_rentals()
    )
    menu.add_command(label="Cadastrar", command=lambda: v.create_rental())
    menu.add_command(label="Alterar", command=lambda: v.update_rental())


def insurance_menu_options(menu):
    menu.add_command(
        label="Consultar", command=lambda: print(c.select_all_insurances())
    )
    menu.add_command(label="Cadastrar", command=lambda: v.create_insurance())
    menu.add_command(label="Alterar", command=lambda: v.update_insurance())
    menu.add_command(label="Excluir", command=lambda: v.delete_insurance())
