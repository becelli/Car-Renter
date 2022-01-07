from view.gui import init as init_gui
import model.functions.database as db
from model.classes import insurance, vehicle, rent, user
from datetime import datetime


def init_database():
    db.init_tables()

    n = 5
    if db.is_empty("user"):
        db.populate_user(n)
    if db.is_empty("vehicle"):
        db.populate_vehicle(n)
    # if db.is_empty("rent"):
    #     db.populate_rent(n)
    # if db.is_empty("insurance"):
    #     db.populate_insurance(n)


def show_gui():
    init_gui()


##### SELECTS

# VEHICLE


def insert_vehicle(vehicle: vehicle.Vehicle):
    return db.insert_vehicle(vehicle)


def update_vehicle(vehicle: vehicle.Vehicle):
    return db.update_vehicle(vehicle)


def delete_vehicle(plate: str):
    return db.delete_vehicle(plate)


def select_all_vehicles():
    return db.select_all_vehicles()


def select_all_imported_vehicles():
    return db.select_all_imported_vehicles()


def select_all_national_vehicles():
    return db.select_all_national_vehicles()


def select_available_vehicles():
    return db.select_available_vehicles()


def select_rented_vehicles():
    return db.select_rented_vehicles()


def select_not_returned_vehicles():
    return db.select_not_returned_vehicles()


def select_rented_vehicles_by_client_id():
    return db.select_rented_vehicles_by_client_id()


#  USERS


def insert_user(user: user.User):
    return db.insert_user(user)


def update_user(user: user.User):
    return db.update_user(user)


def delete_user(user_id: int):
    return db.delete_user(user_id)


def select_all_imported_insurances():
    return db.select_all_imported_insurances()


def select_all_employees():
    return db.select_all_employees()


def select_employee_of_month():
    return db.select_employee_of_month()


def select_all_clients():
    return db.select_all_clients()


def select_client_late_rents():
    return db.select_client_late_rents()


# RENT


def insert_rent(rent: rent.Rent):
    return db.insert_rent(rent)


def update_rent(rent: rent.Rent):
    return db.update_rent(rent)


def delete_rent(rent_id: int):
    return db.delete_rent(rent_id)


def select_all_rents():
    return db.select_all_rents()


def select_all_finished_rents():
    return db.select_all_finished_rents()


def select_all_ongoing_rents():
    return db.select_all_ongoing_rents()


def select_all_expired_rents():
    return db.select_all_late_rents()


def select_monthly_rents(date: datetime):
    return db.select_monthly_rents(date)


# INSURANCE


def insert_insurance(insurance: insurance.Insurance):
    return db.insert_insurance(insurance)


def update_insurance(insurance: insurance.Insurance):
    return db.update_insurance(insurance)


def delete_insurance(insurance_id: int):
    return db.delete_insurance(insurance_id)


def select_all_insurances():
    return db.select_all_insurances()
