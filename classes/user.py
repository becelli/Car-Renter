import sys
from abc import ABC, abstractmethod
from datetime import datetime as dt
import sqlite3 as sql3

# sys.path.append("..")
import functions.database as db

sql = sql3.connect("./db/application.db")
cursor = sql.cursor()


class User(ABC):
    def __init__(
        self,
        name: str,
        cpf: str,
        rg: str,
        birth_date: str,
        address: str,
        zip_code: str,
        email: str,
    ):
        self.set_name(name)
        self.set_cpf(cpf)
        self.set_rg(rg)
        self.set_birth_date(birth_date)
        self.set_address(address)
        self.set_zip_code(zip_code)
        self.set_email(email)

    def validate_email(self, email: str):
        if email is None:
            raise ValueError("Email cannot be empty")
        if "@" not in email:
            raise ValueError("Email must contain @")
        if "." not in email:
            raise ValueError("Email must contain .")
        if email.count("@") > 1:
            raise ValueError("Email must contain only one @")

    def validate_birth_date(self, birth_date: str):
        if birth_date is None:
            raise ValueError("Birth date cannot be empty")
        if len(birth_date) != 10:
            raise ValueError("Birth date must be 10 digits")
        if birth_date[4] != "-" or birth_date[7] != "-":
            raise ValueError("Birth date must be in format YYYY-MM-DD")
        try:
            dt.strptime(birth_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Birth date must be in format YYYY-MM-DD")

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

    @abstractmethod
    def save(self):
        return db.insert_user(self)

    # *************************************************************************
    # Getters and setters
    # *************************************************************************
    def get_name(self):
        return self.name

    def get_cpf(self):
        return self.cpf

    def get_rg(self):
        return self.rg

    def get_birth_date(self):
        return self.birth_date

    def get_address(self):
        return self.address

    def get_zip_code(self):
        return self.zip_code

    def get_email(self):
        return self.email

    def set_name(self, name: str):
        if type(name) is not str:
            raise TypeError("Name must be a string")
        self.name = name

    def set_cpf(self, cpf: str):
        if type(cpf) is not str:
            raise TypeError("CPF must be a string")
        self.cpf = cpf

    def set_rg(self, rg: str):
        if type(rg) is not str:
            raise TypeError("RG must be a string")
        self.rg = rg

    def set_birth_date(self, birth_date: str):
        if type(birth_date) is not str:
            raise TypeError("Birth date must be a string")
        self.validate_birth_date(birth_date)
        self.birth_date = dt.strptime(birth_date, "%Y-%m-%d")

    def set_address(self, address: str):
        if type(address) is not str:
            raise TypeError("Address must be a string")
        self.address = address

    def set_zip_code(self, zip_code: str):
        if type(zip_code) is not str:
            raise TypeError("Zip code must be an string")
        if len(zip_code) != 9:
            raise ValueError("Zip code must be 9 digits")
        if zip_code[5] != "-":
            raise ValueError("Zip code must be in format XXXXX-XXX")
        self.zip_code = zip_code

    def set_email(self, email: str):
        if type(email) is not str:
            raise TypeError("Email must be a string")
        self.validate_email(email)
        self.email = email


class Employee(User):
    def __init__(
        self,
        name: str,
        cpf: str,
        rg: str,
        birth_date: str,
        address: str,
        zip_code: str,
        email: str,
        salary: float,
        pis: str,
        admission_date: str,
    ):
        super().__init__(name, cpf, rg, birth_date, address, zip_code, email)
        self.set_salary(salary)
        self.set_pis(pis)
        self.set_admission_date(admission_date)

    def save(self):
        return db.insert_user(self)

    def __str__(self):
        return (
            super().__str__()
            + f"Salary: {self.get_salary()}\n"
            + f"Government ID: {self.get_pis()}\n"
            + f"Admission Date: {self.get_admission_date()}\n"
        )

    def validate_admission_date(self, admission_date):
        if len(admission_date) != 10:
            raise ValueError("Invalid date expression")
        aux = dt.strptime(admission_date, "%Y-%m-%d")
        if aux > dt.now():
            raise ValueError("admission date must be in the past")

    # *****************************************************************************************
    # Getters and Setters
    # *****************************************************************************************
    def get_salary(self):
        return self.salary

    def get_pis(self):
        return self.pis

    def get_admission_date(self):
        return self.admission_date

    def set_salary(self, salary: float):
        if type(salary) is not float:
            raise TypeError("Salary must be a float")
        if salary < 0:
            raise ValueError("Salary must be a positive number")
        self.salary = salary

    def set_pis(self, pis):
        if type(pis) is not str:
            raise TypeError("Government ID must be a string")
        self.pis = pis

    def set_admission_date(self, admission_date):
        self.validate_admission_date(admission_date)
        self.admission_date = admission_date


class Client(User):
    def __init__(
        self,
        name: str,
        cpf: str,
        rg: str,
        birth_date: str,
        address: str,
        zip_code: str,
        email: str,
        permission_category: str,
        permission_number: str,
        permission_expiration: str,
        is_golden_client: bool,
    ):
        super().__init__(name, cpf, rg, birth_date, address, zip_code, email)
        self.set_permission_category(permission_category)
        self.set_permission_number(permission_number)
        self.set_permission_expiration(permission_expiration)
        self.set_is_golden_client(is_golden_client)

    def save(self):
        return db.insert_user(self)

    def validate_permission_expiration(self, permission_expiration):
        if len(permission_expiration) != 7:
            raise ValueError("Invalid date expression")
        aux = dt.strptime(permission_expiration, "%Y-%m")
        if aux < dt.now():
            raise ValueError("Permission expiration date is in the past")

    def __str__(self):
        return (
            super().__str__()
            + f"Permission Category: {self.get_permission_category()}\n"
            + f"Permission Number: {self.get_permission_number()}\n"
            + f"Permission Expiration: {self.get_permission_expiration()}\n"
            + f"Is Golden Client: {self.get_is_golden_client()}\n"
        )

    # *****************************************************************************************
    # Getters and Setters
    # *****************************************************************************************
    def get_permission_category(self):
        return self.permission_category

    def get_permission_number(self):
        return self.permission_number

    def get_permission_expiration(self):
        return self.permission_expiration

    def get_is_golden_client(self):
        return self.is_golden_client

    def set_permission_category(self, permission_category):
        if permission_category not in ["A", "B", "C", "D", "E"]:
            raise ValueError("Invalid permission category")
        self.permission_category = permission_category

    def set_permission_number(self, permission_number):
        if len(permission_number) != 10:
            raise ValueError("Invalid permission number")
        self.permission_number = permission_number

    def set_permission_expiration(self, permission_expiration):
        self.validate_permission_expiration(permission_expiration)
        self.permission_expiration = permission_expiration

    def set_is_golden_client(self, is_golden_client):
        if is_golden_client not in [True, False]:
            raise ValueError("Invalid golden client value")
        self.is_golden_client = is_golden_client
