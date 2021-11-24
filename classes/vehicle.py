import sqlite3 as sql3
import functions.database as db

sql = sql3.connect("./db/application.db")
cursor = sql.cursor()

from abc import ABC, abstractmethod


class Vehicle(ABC):
    def __init__(
        self,
        model: str,
        manufacturer: str,
        fabrication_year: int,
        model_year: int,
        plate: str,
        category: str,
        fipe_value: float,
        rent_value: float,
        is_available: bool,
    ):

        aux = cursor.execute("SELECT * FROM vehicle ORDER BY id DESC LIMIT 1")
        aux = aux.fetchall()
        last_id = 0 if not isinstance(aux, int) else aux + 1
        self.vehicle_id = last_id + 1
        self.set_model(model)
        self.set_manufacturer(manufacturer)
        self.set_fabrication_year(fabrication_year)
        self.set_model_year(model_year)
        self.set_plate(plate)
        self.set_category(category)
        self.set_fipe_value(fipe_value)
        self.set_rent_value(rent_value)
        self.set_is_available(is_available)

    @abstractmethod
    def save(self):
        return db.insert_vehicle(self)

    @abstractmethod
    def calculate_daily_rent_value(self):
        return self.rent_value

    def rent(self):
        self.is_available = False

    def return_vehicle(self):
        self.is_available = True

    def __str__(self):
        return (
            f"vehicle ID: {self.get_vehicle_id()}\n"
            f"Model: {self.get_model()}\n"
            f"Manufacturer: {self.get_manufacturer()}\n"
            f"Fabrication Year: {self.get_fabrication_year()}\n"
            f"Model Year: {self.get_model_year()}\n"
            f"Plate: {self.get_plate()}\n"
            f"Category: {self.get_category()}\n"
            f"Fipe Value: {self.get_fipe_value()}\n"
            f"Rent Value: {self.get_rent_value()}\n"
            f"Is Available: {self.get_is_available()}\n"
        )

    # *************************************************************************
    # Getters and Setters
    # *************************************************************************
    def get_vehicle_id(self):
        return self.vehicle_id

    def get_model(self):
        return self.model

    def get_manufacturer(self):
        return self.manufacturer

    def get_fabrication_year(self):
        return self.fabrication_year

    def get_model_year(self):
        return self.model_year

    def get_plate(self):
        return self.plate

    def get_category(self):
        return self.category

    def get_fipe_value(self):
        return self.fipe_value

    def get_rent_value(self):
        return self.rent_value

    def get_is_available(self):
        return self.is_available

    def set_model(self, model: str):
        if type(model) is not str:
            raise TypeError("model must be a string")
        self.model = model

    def set_manufacturer(self, manufacturer: str):
        if type(manufacturer) is not str:
            raise TypeError("manufacturer must be a string")
        self.manufacturer = manufacturer

    def set_fabrication_year(self, fabrication_year: int):
        if type(fabrication_year) is not int:
            raise TypeError("fabrication_year must be an integer")

        if len(str(fabrication_year)) != 4:
            raise ValueError("fabrication_year must be 4 digits")
        self.fabrication_year = fabrication_year

    def set_model_year(self, model_year: int):
        if type(model_year) is not int:
            raise TypeError("model_year must be an integer")
        if len(str(model_year)) != 4:
            raise ValueError("model_year must be 4 digits")
        if self.get_fabrication_year() > model_year + 1:
            raise ValueError("fabrication_year must be less than model_year + 1")
        self.model_year = model_year

    def set_plate(self, plate: str):
        if type(plate) is not str:
            raise TypeError("plate must be a string")
        if len(plate) != 8:
            raise ValueError("plate must be 7 digits")
        for i in range(len(plate)):
            if (i < 3 and plate[i].isdigit()) or (i >= 4 and plate[i].isalpha()):
                raise ValueError("plate must be a valid plate")
        self.plate = plate.upper()

    def set_category(self, category: str):
        if type(category) is not str:
            raise TypeError("category must be a string")
        self.category = category

    def set_fipe_value(self, fipe_value: float):
        if type(fipe_value) is not float:
            raise TypeError("fipe_value must be a float")
        self.fipe_value = fipe_value

    def set_rent_value(self, rent_value: float):
        if type(rent_value) is not float:
            raise TypeError("rent_value must be a float")
        self.rent_value = rent_value

    def set_is_available(self, is_available: bool):
        if type(is_available) is not bool:
            raise TypeError("is_available must be a boolean")
        self.is_available = is_available


class National(Vehicle):
    def __init__(
        self,
        model: str,
        manufacturer: str,
        fabrication_year: int,
        model_year: int,
        plate: str,
        category: str,
        fipe_value: float,
        rent_value: float,
        is_available: bool,
        state_taxes: float,
    ):
        super().__init__(
            model,
            manufacturer,
            fabrication_year,
            model_year,
            plate,
            category,
            fipe_value,
            rent_value,
            is_available,
        )
        if type(state_taxes) is not float:
            raise TypeError("State taxes must be a float")
        if state_taxes > 1 or state_taxes < 0:
            raise ValueError("State taxes must be between 0 and 1")
        self.state_taxes = state_taxes

    def calculate_daily_rent_value(self):
        return self.rent_value * (1 + self.get_state_taxes())

    def __str__(self):
        return super().__str__() + f"\nState Taxes: {self.get_state_taxes()}"

    def save(self):
        return db.insert_vehicle(self)

    # *************************************************************************
    # Getters and Setters
    # *************************************************************************
    def get_state_taxes(self):
        return self.state_taxes

    def set_state_taxes(self, state_taxes: float):
        self.state_taxes = state_taxes


class International(Vehicle):
    def __init__(
        self,
        model: str,
        manufacturer: str,
        fabrication_year: int,
        model_year: int,
        plate: str,
        category: str,
        fipe_value: float,
        rent_value: float,
        is_available: bool,
        state_taxes: float,
        federal_taxes: float,
    ):
        super().__init__(
            model,
            manufacturer,
            fabrication_year,
            model_year,
            plate,
            category,
            fipe_value,
            rent_value,
            is_available,
        )
        if type(state_taxes) is not float:
            raise TypeError("State taxes must be a float")
        if type(federal_taxes) is not float:
            raise TypeError("Federal taxes must be a float")
        if state_taxes > 1 or state_taxes < 0:
            raise ValueError("State taxes must be between 0 and 1")
        if federal_taxes > 1 or state_taxes < 0:
            raise ValueError("Federal taxes must be between 0 and 1")
        self.state_taxes = state_taxes
        self.federal_taxes = federal_taxes

    def save(self):
        return db.insert_vehicle(self)

    def calculate_daily_rent_value(self):
        return self.get_rent_value() * (
            1 + self.get_state_taxes() + self.get_federal_taxes()
        )

    def __str__(self):
        return (
            super().__str__()
            + f"State Taxes: {self.get_state_taxes()} \n"
            + f"Federal Taxes: {self.get_federal_taxes()} \n"
        )

    # *****************************************************************************************
    # Getters and Setters
    # *****************************************************************************************
    def get_state_taxes(self):
        return self.state_taxes

    def get_federal_taxes(self):
        return self.federal_taxes

    def set_state_taxes(self, state_taxes: float):
        self.state_taxes = state_taxes

    def set_federal_taxes(self, federal_taxes: float):
        self.federal_taxes = federal_taxes
