from abc import ABC, abstractmethod
from datetime import date
import model.classes.database as db


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
        id: int = None,
    ):
        self._name = name
        self._cpf = cpf
        self._rg = rg
        self._birth_date = birth_date
        self._address = address
        self._zip_code = zip_code
        self._email = email
        self._id = id

    def save(self, database: str = "app.db"):
        ret = db.Database(database).insert_user(self)
        if ret is not None:
            self._id = ret

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

    # TODO: Remove these alidation
    # def validate_email(self, email: str):
    #     if email is None:
    #         raise ValueError("Email cannot be empty")
    #     if "@" not in email:
    #         raise ValueError("Email must contain @")
    #     if "." not in email:
    #         raise ValueError("Email must contain .")
    #     if email.count("@") > 1:
    #         raise ValueError("Email must contain only one @")

    # def validate_birth_date(self, birth_date: str):
    #     if birth_date is None:
    #         raise ValueError("Birth date cannot be empty")
    #     if len(birth_date) != 10:
    #         raise ValueError("Birth date must be 10 digits")
    #     if birth_date[4] != "-" or birth_date[7] != "-":
    #         raise ValueError("Birth date must be in format YYYY-MM-DD")
    #     try:
    #         dt.strptime(birth_date, "%Y-%m-%d")
    #     except ValueError:
    #         raise ValueError("Birth date must be in format YYYY-MM-DD")

    # *************************************************************************
    # Getters and setters
    # *************************************************************************
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
        id: int = None,
    ):
        super().__init__(name, cpf, rg, birth_date, address, zip_code, email, id)
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

    # TODO Remove this validation
    # def validate_admission_date(self, admission_date):
    #     if len(admission_date) != 10:
    #         raise ValueError("Invalid date expression")
    #     aux = dt.strptime(admission_date, "%Y-%m-%d")
    #     if aux > dt.now():
    #         raise ValueError("admission date must be in the past")

    # *****************************************************************************************
    # Getters and Setters
    # *****************************************************************************************
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
        id: int = None,
    ):
        super().__init__(name, cpf, rg, birth_date, address, zip_code, email, id)
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

    # *****************************************************************************************
    # Getters and Setters
    # *****************************************************************************************
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
        # TODO: Remove this validation
        # if len(permission_number) != 10:
        #     raise ValueError("Invalid permission number")
        self._permission_number = permission_number

    def set_permission_expiration(self, permission_expiration: str):
        self._permission_expiration = permission_expiration

    def set_is_golden_client(self, is_golden_client: bool):
        self._is_golden_client = is_golden_client
