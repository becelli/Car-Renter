from abc import ABC, abstractmethod
import model.classes.database as db


class Vehicle(ABC):
    def __init__(
        self,
        plate: str,
        model: str,
        manufacturer: str,
        fabrication_year: int,
        model_year: int,
        category: str,
        fipe_value: float,
        rent_value: float,
        is_available: bool,
    ):
        self._plate = plate
        self._model = model
        self._manufacturer = manufacturer
        self._fabrication_year = fabrication_year
        self._model_year = model_year
        self._category = category
        self._fipe_value = fipe_value
        self._rent_value = rent_value
        self._is_available = is_available

    def save(self, database: str = "app.db"):
        db.Database(database).insert_vehicle(self)

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
        self._plate = plate.upper()

    def set_category(self, category: str):
        self._category = category

    def set_fipe_value(self, fipe_value: float):
        self._fipe_value = fipe_value

    def set_rent_value(self, rent_value: float):
        self._rent_value = rent_value

    def set_is_available(self, is_available: bool):
        self._is_available = is_available


class National(Vehicle):
    def __init__(
        self,
        plate: str,
        model: str,
        manufacturer: str,
        fabrication_year: int,
        model_year: int,
        category: str,
        fipe_value: float,
        rent_value: float,
        is_available: bool,
        state_taxes: float,
    ):
        super().__init__(
            plate,
            model,
            manufacturer,
            fabrication_year,
            model_year,
            category,
            fipe_value,
            rent_value,
            is_available,
        )
        self._state_taxes = state_taxes

    def calculate_daily_rent_value(self):
        return self._rent_value * (1 + self.get_state_taxes())

    def __str__(self):
        return super().__str__() + f"State Taxes: {self.get_state_taxes()}\n"

    def get_state_taxes(self):
        return self._state_taxes

    def set_state_taxes(self, state_taxes: float):
        self._state_taxes = state_taxes


class Imported(Vehicle):
    def __init__(
        self,
        plate: str,
        model: str,
        manufacturer: str,
        fabrication_year: int,
        model_year: int,
        category: str,
        fipe_value: float,
        rent_value: float,
        is_available: bool,
        state_taxes: float,
        federal_taxes: float,
    ):
        super().__init__(
            plate,
            model,
            manufacturer,
            fabrication_year,
            model_year,
            category,
            fipe_value,
            rent_value,
            is_available,
        )
        self._state_taxes = state_taxes
        self._federal_taxes = federal_taxes

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

    def get_state_taxes(self):
        return self._state_taxes

    def get_federal_taxes(self):
        return self._federal_taxes

    def set_state_taxes(self, state_taxes: float):
        self._state_taxes = state_taxes

    def set_federal_taxes(self, federal_taxes: float):
        self._federal_taxes = federal_taxes
