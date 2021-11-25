from dataclasses import dataclass
import model.functions.database as db
from model.classes.payment import payment
from datetime import date


@dataclass
class Rent:
    _employee_id: int
    _vehicle_id: int
    _start_date: date
    _end_date: date
    _total_value: float
    _payment_method: payment
    _insurance: list
    _is_returned: bool
    _client_id: int = -1

    def save(self):
        db.insert_rent(self)

    def calculate_total_value(self):
        pass

    # **********************************************************************************************************************
    # Getters and Setters
    # **********************************************************************************************************************
    def get_client_id(self):
        return self._client_id

    def get_employee_id(self):
        return self._employee_id

    def get_vehicle_id(self):
        return self._vehicle_id

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

    def set_client_id(self, client_id: int):

        self._client_id = client_id

    def set_employee_id(self, employee_id: int):

        self._employee_id = employee_id

    def set_vehicle_id(self, vehicle_id: int):

        self._vehicle_id = vehicle_id

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
