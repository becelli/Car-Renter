from dataclasses import dataclass
from abc import ABC, abstractmethod
import model.functions.database as db


@dataclass
class Vehicle(ABC):
    _model: str
    _manufacturer: str
    _fabrication_year: int
    _model_year: int
    _plate: str
    _category: str
    _fipe_value: float
    _rent_value: float
    _is_available: bool

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def calculate_daily_rent_value(self):
        return self._rent_value

    def rent(self):
        self._is_available = False

    def return_vehicle(self):
        self._is_available = True

    @abstractmethod
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
        return self._vehicle_id

    def get_model(self):
        return self._model

    def get_manufacturer(self):
        return self._manufacturer

    def get_fabrication_year(self):
        return self._fabrication_year

    def get_model_year(self):
        return self._model_year

    def get_plate(self):
        return self._plate

    def get_category(self):
        return self._category

    def get_fipe_value(self):
        return self._fipe_value

    def get_rent_value(self):
        return self._rent_value

    def get_is_available(self):
        return self._is_available

    def set_model(self, model: str):
        self._model = model

    def set_manufacturer(self, manufacturer: str):
        self._manufacturer = manufacturer

    def set_fabrication_year(self, fabrication_year: int):
        self._fabrication_year = fabrication_year

    def set_model_year(self, model_year: int):
        self._model_year = model_year

    def set_plate(self, plate: str):
        # TODO: Move logic to front-end
        # if len(plate) != 8:
        #     raise ValueError("plate must be 7 digits")
        # for i in range(len(plate)):
        #     if (i < 3 and plate[i].isdigit()) or (i >= 4 and plate[i].isalpha()):
        #         raise ValueError("plate must be a valid plate")
        self._plate = plate.upper()

    def set_category(self, category: str):
        self._category = category

    def set_fipe_value(self, fipe_value: float):
        self._fipe_value = fipe_value

    def set_rent_value(self, rent_value: float):
        self._rent_value = rent_value

    def set_is_available(self, is_available: bool):
        self._is_available = is_available


@dataclass
class National(Vehicle):
    _state_taxes: float

    def calculate_daily_rent_value(self):
        return self._rent_value * (1 + self.get_state_taxes())

    def __str__(self):
        return super().__str__() + f"\nState Taxes: {self.get_state_taxes()}"

    def save(self):
        return db.insert_vehicle(self)

    # *************************************************************************
    # Getters and Setters
    # *************************************************************************
    def get_state_taxes(self):
        return self._state_taxes

    def set_state_taxes(self, state_taxes: float):
        self._state_taxes = state_taxes


@dataclass
class Imported(Vehicle):
    _state_taxes: float
    _federal_taxes: float

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
        return self._state_taxes

    def get_federal_taxes(self):
        return self._federal_taxes

    def set_state_taxes(self, state_taxes: float):
        self._state_taxes = state_taxes

    def set_federal_taxes(self, federal_taxes: float):
        self._federal_taxes = federal_taxes
