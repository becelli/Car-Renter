import model.classes.database as database
from model.classes import insurance, vehicle, rent, user, payment
from datetime import datetime


class Controller:
    def __init__(self, db: str = "app.db"):
        self.db = database.Database(db)

    def init_database(self, n: int = 10):
        self.db.init_tables()

        if self.db.is_empty("user"):
            self.db.populate_user(3 * n)
        if self.db.is_empty("vehicle"):
            self.db.populate_vehicle(2 * n)
        if self.db.is_empty("insurance"):
            self.db.populate_insurance()
        if self.db.is_empty("rent"):
            self.db.populate_rent(n)

    # USERS
    def insert_user(self, user: user.User):
        return self.db.insert_user(user)

    # VEHICLE

    def insert_vehicle(self, vehicle: vehicle.Vehicle):
        return self.db.insert_vehicle(vehicle)

    def select_vehicle(self, plate: str):
        return self.db.select_vehicle_by_plate(plate)

    def select_all_vehicles(self):
        return self.db.select_all_vehicles()

    def select_all_available_vehicles(self):
        return self.db.select_all_available_vehicles()

    def select_all_imported_vehicles(self):
        return self.db.select_all_imported_vehicles()

    def select_all_national_vehicles(self):
        return self.db.select_all_national_vehicles()

    def select_available_vehicles(self):
        return self.db.select_available_vehicles()

    ##### SELECTS

    # VEHICLE

    def insert_vehicle(self, vehicle: vehicle.Vehicle):
        return self.db.insert_vehicle(vehicle)

    def select_all_vehicles(self):
        return self.db.select_all_vehicles()

    def select_rented_vehicles(self):
        return self.db.select_rented_vehicles()

    def select_not_returned_vehicles(self):
        return self.db.select_not_returned_vehicles()

    def select_rented_vehicles_by_client(self, cpf: str):
        return self.db.select_rented_vehicles_by_client(cpf)

    def select_rent_history_of(self, cpf: str):
        return self.db.select_rent_history_of(cpf)

    def select_expired_rents_of(self, cpf: str):
        return self.db.select_expired_rents_of(cpf)

    #  USERS

    def insert_user(self, user: user.User):
        return self.db.insert_user(user)

    def select_client(self, cpf: str) -> user.User:
        return self.db.select_client(cpf)

    def select_employee(self, cpf: str) -> user.User:
        return self.db.select_employee(cpf)

    def select_all_imported_insurances(self):
        return self.db.select_all_imported_insurances()

    def select_all_employees(self):
        return self.db.select_all_employees()

    def select_employee_of_month(self):
        return self.db.select_employee_of_month()

    def select_all_clients(self):
        return self.db.select_all_clients()

    def select_client_late_rents(self):
        return self.db.select_client_late_rents()

    # RENT
    def insert_rent(self, rent: rent.Rent):
        return self.db.insert_rent(rent)

    def select_all_rents(self):
        return self.db.select_all_rents()

    def select_all_finished_rents(self):
        return self.db.select_all_finished_rents()

    def select_all_ongoing_rents(self):
        return self.db.select_all_ongoing_rents()

    def select_all_expired_rents(self):
        return self.db.select_all_expired_rents()

    def select_monthly_rents(self, date: datetime):
        return self.db.select_monthly_rents(date)

    def return_vehicle(self, rent_id: int):
        return self.db.return_vehicle(rent_id)

    # INSURANCE

    def insert_insurance(self, insurance: insurance.Insurance):
        return self.db.insert_insurance(insurance)

    def select_all_insurances(self):
        return self.db.select_all_insurances()

    def select_insurance(self, id):
        return self.db.select_insurance(id)

    def insert_payment(self, payment: payment.Payment):
        return self.db.insert_payment(payment)

    def select_rents_monthly(self, month: datetime):
        return self.db.select_rents_monthly(month)

    def select_employee_of_the_month(self, month: datetime):
        return self.db.select_employee_of_the_month(month)
