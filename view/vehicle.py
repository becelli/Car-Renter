from tkinter import *
from tkinter import ttk
import controller.controller as c
import model.classes.vehicle as vehicle


def insert_imported(list):
    print(list)


def insert_imported_gui(root):
    gui = Toplevel(root)
    gui.title("Cadastro de Veículo")
    gui.geometry("480x270")
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
    entries = {}
    for field in fields:
        label = ttk.Label(gui, text=field, width=20)
        label.grid(row=fields.index(field), column=0, sticky=W)
        entries[field] = ttk.Entry(gui, width=30)
        entries[field].grid(row=fields.index(field), column=1, sticky=W)
    ttk.Button(
        gui,
        text="Cadastrar",
        command=lambda: c.insert_vehicle(
            vehicle.Imported(
                entries["Placa"].get(),
                entries["Modelo"].get(),
                entries["Fabricante"].get(),
                entries["Ano"].get(),
                entries["Ano do Modelo"].get(),
                entries["Categoria"].get(),
                entries["Valor na FIPE"].get(),
                entries["Valor da Diária"].get(),
                entries["Disponível"].get(),
                entries["Imposto Estadual"].get(),
                entries["Imposto Federal"].get(),
            )
        ),
    ).grid(row=10, column=1, sticky=W, pady=10)
