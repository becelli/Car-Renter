import model.classes.database as database
from model.classes import insurance, vehicle, rent, user
from datetime import datetime


class Controller:
    def __init__(self, db: str = "app.db"):
        self.db = database.Database(db)

    def init_database(self):
        self.db.init_tables()

        n = 5
        if self.db.is_empty("user"):
            self.db.populate_user(n)
        if self.db.is_empty("vehicle"):
            self.db.populate_vehicle(n)
        if self.db.is_empty("insurance"):
            self.db.populate_insurance(n)
        if self.db.is_empty("payment"):
            self.db.populate_payment(n)
        # if self.db.is_empty("rent"):
        #     self.db.populate_rent(n)

    ##### SELECTS

    # VEHICLE

    def insert_vehicle(self, vehicle: vehicle.Vehicle):
        return self.db.insert_vehicle(vehicle)

    def update_vehicle(self, vehicle: vehicle.Vehicle):
        return self.db.update_vehicle(vehicle)

    def delete_vehicle(self, plate: str):
        return self.db.delete_vehicle(plate)

    def select_all_vehicles(self):
        return self.db.select_all_vehicles()

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

    def update_vehicle(self, vehicle: vehicle.Vehicle):
        return self.db.update_vehicle(vehicle)

    def delete_vehicle(self, plate: str):
        return self.db.delete_vehicle(plate)

    def select_all_vehicles(self):
        return self.db.select_all_vehicles()

    def select_rented_vehicles(self):
        return self.db.select_rented_vehicles()

    def select_not_returned_vehicles(self):
        return self.db.select_not_returned_vehicles()

    def select_rented_vehicles_by_client_id(self):
        return self.db.select_rented_vehicles_by_client_id()

    #  USERS

    def insert_user(self, user: user.User):
        return self.db.insert_user(user)

    def update_user(self, user: user.User):
        return self.db.update_user(user)

    def delete_user(self, user_id: int):
        return self.db.delete_user(user_id)

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

    def insert_rent(self, rent: rent.Rent):
        return self.db.insert_rent(rent)

    def update_rent(self, rent: rent.Rent):
        return self.db.update_rent(rent)

    def delete_rent(self, rent_id: int):
        return self.db.delete_rent(rent_id)

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

    # INSURANCE

    def insert_insurance(self, insurance: insurance.Insurance):
        return self.db.insert_insurance(insurance)

    def update_insurance(self, insurance: insurance.Insurance):
        return self.db.update_insurance(insurance)

    def delete_insurance(self, insurance_id: int):
        return self.db.delete_insurance(insurance_id)

    def select_all_insurances(self):
        return self.db.select_all_insurances()
