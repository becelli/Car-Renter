from dataclasses import dataclass
from model.classes import payment
from model.functions import database as db
from datetime import date


@dataclass
class Rent:
    _vehicle_plate: str
    _client_cpf: str
    _employee_cpf: str
    _start_date: date
    _end_date: date
    _total_value: float
    _payment_method: payment
    _insurance: list
    _is_returned: bool
    _id: int = 0

    def save(self):
        db.insert_rent(self)

    # TODO
    def calculate_total_value(self):
        pass

    # **********************************************************************************************************************
    # Getters and Setters
    # **********************************************************************************************************************
    def get_id(self):
        return self._id

    def get_client_cpf(self):
        return self._client_cpf

    def get_employee_cpf(self):
        return self._employee_cpf

    def get_vehicle_plate(self):
        return self._vehicle_plate

    def get_start_date(self):
        return self._start_date

    def get_end_date(self):
        return self._end_date

    def get_total_value(self):
        return self._total_value

    def get_payment_method(self):
        return self._payment_method

    def get_insurance(self):
        return self._insurance

    def get_is_returned(self):
        return self._is_returned

    def set_id(self, id):
        self._id = id

    def set_client_cpf(self, client_cpf: str):

        self._client_cpf = client_cpf

    def set_employee_cpf(self, employee_cpf: str):

        self._employee_cpf = employee_cpf

    def set_vehicle_plate(self, vehicle_id: str):

        self._vehicle_plate = vehicle_id

    def set_start_date(self, start_date: date):

        self._start_date = start_date

    def set_end_date(self, end_date: date):

        self._end_date = end_date

    def set_total_value(self, total_value: float):

        self._total_value = total_value

    def set_payment_method(self, payment_method: payment):

        self._payment_method = payment_method

    def set_insurance(self, insurance: list):

        self._insurance = insurance

    def set_is_returned(self, is_returned: bool):
        self._is_returned = is_returned
