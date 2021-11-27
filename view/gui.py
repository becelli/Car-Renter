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
    menu_bar.add_cascade(label="Vehicles", menu=vehicle_menu)
    vehicle_menu_options(vehicle_menu)
    user_menu = Menu(menu_bar)
    rental_menu = Menu(menu_bar)
    menu_bar.add_cascade(label="Users", menu=user_menu)
    menu_bar.add_cascade(label="Rentals", menu=rental_menu)


def vehicle_menu_options(menu):
    # Reports
    # TODO pass as parameter to vehicle view
    vehicles_reports = Menu(menu)
    menu.add_cascade(label="Consultar", menu=vehicles_reports)
    vehicles_reports.add_command(
        label="Geral", command=lambda: print(c.select_all_vehicles())
    )
    vehicles_reports.add_command(
        label="Nacionais", command=lambda: c.select_all_national_vehicles()
    )
    vehicles_reports.add_command(
        label="Importados", command=lambda: c.select_all_imported_vehicles()
    )

    # Other options
    menu.add_command(label="Cadastrar", command=lambda: v.create_vehicle())
    menu.add_command(label="Alterar", command=lambda: v.update_vehicle())
    menu.add_command(label="Excluir", command=lambda: v.delete_vehicle())
