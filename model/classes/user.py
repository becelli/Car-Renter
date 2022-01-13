from abc import ABC, abstractmethod
from datetime import date
import model.classes.database as database


class User(ABC):
    def __init__(
        self,
        name: str,
        cpf: str,
        rg: str,
        birth_date: date,
        address: str,
        zip_code: str,
        email: str,
    ):
        self._name = name
        self._cpf = cpf
        self._rg = rg
        self._birth_date = birth_date
        self._address = address
        self._zip_code = zip_code
        self._email = email

    def save(self, db: str = "app.db"):
        database.Database(db).insert_user(self)

    @abstractmethod
    def __str__(self):
        return (
            f"Name: {self.get_name()}\n"
            f"Personal ID: {self.get_cpf()}\n"
            f"General ID: {self.get_rg()}\n"
            f"Birth date: {self.get_birth_date()}\n"
            f"Address: {self.get_address()}\n"
            f"Zip code: {self.get_zip_code()}\n"
            f"Email: {self.get_email()}\n"
        )

    def get_name(self):
        return self._name

    def get_cpf(self):
        return self._cpf

    def get_rg(self):
        return self._rg

    def get_birth_date(self):
        return self._birth_date

    def get_address(self):
        return self._address

    def get_zip_code(self):
        return self._zip_code

    def get_email(self):
        return self._email

    def set_name(self, name: str):
        self._name = name

    def set_cpf(self, cpf: str):
        self._cpf = cpf

    def set_rg(self, rg: str):
        self._rg = rg

    def set_birth_date(self, birth_date: date):
        self._birth_date = birth_date

    def set_address(self, address: str):
        self._address = address

    def set_zip_code(self, zip_code: str):
        self._zip_code = zip_code

    def set_email(self, email: str):
        self._email = email


class Employee(User):
    def __init__(
        self,
        name: str,
        cpf: str,
        rg: str,
        birth_date: date,
        address: str,
        zip_code: str,
        email: str,
        salary: float,
        pis: str,
        admission_date: date,
    ):
        super().__init__(name, cpf, rg, birth_date, address, zip_code, email)
        self._salary = salary
        self._pis = pis
        self._admission_date = admission_date

    def __str__(self):
        return (
            super().__str__()
            + f"Salary: {self.get_salary()}\n"
            + f"Government ID: {self.get_pis()}\n"
            + f"Admission Date: {self.get_admission_date()}\n"
        )

    def get_salary(self):
        return self._salary

    def get_pis(self):
        return self._pis

    def get_admission_date(self):
        return self._admission_date

    def set_salary(self, salary: float):
        self._salary = salary

    def set_pis(self, pis):
        self._pis = pis

    def set_admission_date(self, admission_date):
        self._admission_date = admission_date


class Client(User):
    def __init__(
        self,
        name: str,
        cpf: str,
        rg: str,
        birth_date: date,
        address: str,
        zip_code: str,
        email: str,
        permission_category,
        permission_number,
        permission_expiration,
        is_golden_client,
    ):
        super().__init__(name, cpf, rg, birth_date, address, zip_code, email)
        self._permission_category = permission_category
        self._permission_number = permission_number
        self._permission_expiration = permission_expiration
        self._is_golden_client = is_golden_client

    def __str__(self):
        return (
            super().__str__()
            + f"Permission Category: {self.get_permission_category()}\n"
            + f"Permission Number: {self.get_permission_number()}\n"
            + f"Permission Expiration: {self.get_permission_expiration()}\n"
            + f"Is Golden Client: {True if self.get_is_golden_client() else False}\n"
        )

    def get_permission_category(self):
        return self._permission_category

    def get_permission_number(self):
        return self._permission_number

    def get_permission_expiration(self):
        return self._permission_expiration

    def get_is_golden_client(self):
        return self._is_golden_client

    def set_permission_category(self, permission_category: str):
        self._permission_category = permission_category

    def set_permission_number(self, permission_number: str):
        self._permission_number = permission_number

    def set_permission_expiration(self, permission_expiration: str):
        self._permission_expiration = permission_expiration

    def set_is_golden_client(self, is_golden_client: bool):
        self._is_golden_client = is_golden_client
