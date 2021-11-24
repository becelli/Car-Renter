import functions.database as db
from classes.payment import payment
from datetime import date


class Rent:
    def __init__(
        self,
        client_id: int,
        employee_id: int,
        vehicle_id: int,
        start_date: date,
        end_date: date,
        total_value: float,
        payment_method: payment,
        insurance: list,
        ended: bool,
        data=None,
    ):
        if data is not None:
            self.client_id = data[0]
            self.employee_id = data[1]
            self.vehicle_id = data[2]
            self.start_date = data[3]
            self.end_date = data[4]
            self.total_value = data[5]
            self.payment_method = data[6]
            self.insurance = data[7]
            self.ended = data[8]
        else:
            self.set_client_id(client_id)
            self.set_employee_id(employee_id)
            self.set_vehicle_id(vehicle_id)
            self.set_start_date(start_date)
            self.set_end_date(end_date)
            self.set_total_value(total_value)
            self.set_payment_method(payment_method)
            self.set_insurance(insurance)
            self.set_ended(ended)

    def save(self):
        db.insert_rent(self)

    def calculate_total_value(self):
        pass

    # **********************************************************************************************************************
    # Getters and Setters
    # **********************************************************************************************************************
    def get_client_id(self):
        return self.client_id

    def get_employee_id(self):
        return self.employee_id

    def get_vehicle_id(self):
        return self.vehicle_id

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_total_value(self):
        return self.total_value

    def get_payment_method(self):
        return self.payment_method

    def get_insurance(self):
        return self.insurance

    def get_ended(self):
        return self.ended

    def set_client_id(self, client_id: int):
        if client_id is not int:
            raise TypeError("Client ID must be an integer.")
        self.client_id = client_id

    def set_employee_id(self, employee_id: int):
        if employee_id is not int:
            raise TypeError("Employee ID must be an integer.")
        self.employee_id = employee_id

    def set_vehicle_id(self, vehicle_id: int):
        if vehicle_id is not int:
            raise TypeError("vehicle ID must be an integer.")
        self.vehicle_id = vehicle_id

    def set_start_date(self, start_date: date):
        if start_date is not date:
            raise TypeError("Start date must be a date.")
        self.start_date = start_date

    def set_end_date(self, end_date: date):
        if end_date is not date:
            raise TypeError("End date must be a date.")
        self.end_date = end_date

    def set_total_value(self, total_value: float):
        if total_value is not float:
            raise TypeError("Total value must be a float.")
        self.total_value = total_value

    def set_payment_method(self, payment_method: payment):
        if payment_method is not payment:
            raise TypeError("Payment method must be valid.")
        self.payment_method = payment_method

    def set_insurance(self, insurance: list):
        if insurance is not list:
            raise TypeError("Insurance must be a list.")
        self.insurance = insurance

    def set_ended(self, ended: bool):
        if ended is not bool:
            raise TypeError("Ended must be a boolean.")
        if ended:
            self.end_date = date.now()
        self.ended = ended
