import model.classes.payment as payment
import model.classes.database as database
import controller.controller as controller
from datetime import date


class Rent:
    def __init__(
        self,
        vehicle_plate: str,
        client_cpf: str,
        employee_cpf: str,
        start_date: date,
        end_date: date,
        total_value: float,
        payment: payment.Payment,
        insurance: list,
        is_returned: bool = False,
        id: int = None,
    ) -> None:
        self._vehicle_plate = vehicle_plate
        self._client_cpf = client_cpf
        self._employee_cpf = employee_cpf
        self._start_date = start_date
        self._end_date = end_date
        self._total_value = total_value
        self._payment = payment
        self._insurance = insurance
        self._is_returned = is_returned
        self._id = id

    def save(self, db: str = "app.db"):
        ret = controller.Controller(db).insert_rent(self)
        if ret is not None:
            self._id = ret

    def __str__(self):
        insurance_str = ""
        insurance = self.get_insurance()
        if insurance is list:
            for i in insurance:
                insurance_str += str(i)

        return (
            f"ID: {self.get_id()}\n"
            f"Placa: {self.get_vehicle_plate()}\n"
            f"CPF do Cliente: {self.get_client_cpf()}\n"
            f"CPF do Funcionário: {self.get_employee_cpf()}\n"
            f"Data de Início: {str(self.get_start_date())[0:10]}\n"
            f"Data de Devolução: {str(self.get_end_date())[0:10]}\n"
            f"Valor Total: {self.get_total_value()}\n"
            f"Pagamento: {self.get_payment()}\n"
            f"Seguros: {insurance_str}\n"
            f"Devolvido: {'S' if self.get_is_returned() else 'N'}\n"
        )

    # TODO
    def calculate_total_value(self):
        db = database.Database()
        vehicle = db.select_national_vehicle(self.get_vehicle_plate())

        days = (self.get_end_date() - self.get_start_date()).days
        total_value = days * vehicle.calculate_daily_rent_value()
        for insurance in self.get_insurance():
            total_value += insurance.get_value()
        return total_value

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

    def get_payment(self) -> payment.Payment:
        return self._payment

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

    def set_payment(self, payment: payment):

        self._payment = payment

    def set_insurance(self, insurance: list):

        self._insurance = insurance

    def set_is_returned(self, is_returned: bool):
        self._is_returned = is_returned
