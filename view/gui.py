from tkinter import *
from tkinter import ttk
import sys

# sys.path.append("../")
# import model.functions.database as db


def create_menu_bar():
    menu_bar = Menu(root)
    root.config(menu=menu_bar)
    vehicle_menu = Menu(menu_bar)
    user_menu = Menu(menu_bar)
    rental_menu = Menu(menu_bar)
    menu_bar.add_cascade(label="Vehicles", menu=vehicle_menu)
    menu_bar.add_cascade(label="Users", menu=user_menu)
    menu_bar.add_cascade(label="Rentals", menu=rental_menu)

    vehicles_reports = Menu(vehicle_menu)
    vehicle_menu.add_cascade(label="Consultar", menu=vehicles_reports)
    vehicle_menu.add_command(label="Cadastrar", command=lambda: print("Cadastrar"))
    vehicle_menu.add_command(label="Alterar", command=lambda: print("Editar"))
    vehicle_menu.add_command(label="Excluir", command=lambda: print("Excluir"))
    # vehicles_reports.add_command(
    #     # label="Geral", command=lambda: print(db.select_all_vehicles())
    # )
    vehicles_reports.add_command(label="Nacionais", command=lambda: print("Nacionais"))
    vehicles_reports.add_command(
        label="Importados", command=lambda: print("Importados")
    )


root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
root.geometry("1280x720")
root.title("Renterio - Sistema de Locações de Veículos")
create_menu_bar()
root.mainloop()
