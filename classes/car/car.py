from abc import ABC, abstractmethod


class Car(ABC):
    def __init__(
        self,
        car_id,
        model,
        manufacturer,
        fabrication_year,
        model_year,
        plate,
        category,
        fipe_value,
        rent_value,
        is_available,
    ):
        self.car_id = car_id
        self.model = model
        self.manufacturer = manufacturer
        self.fabrication_year = fabrication_year
        self.model_year = model_year
        self.plate = plate
        self.category = category
        self.fipe_value = fipe_value
        self.rent_value = rent_value
        self.is_available = is_available

    @abstractmethod
    def calculate_daily_rent_value(self):
        return self.rent_value

    def rent(self):
        self.is_available = False

    def return_car(self):
        self.is_available = True

    def __str__(self):
        return (
            f"Car ID: {self.get_car_id()}\n"
            f"Model: {self.get_model()}\n"
            f"Manufacturer: {self.get_manufacturer()}\n"
            f"Fabrication Year: {self.get_fabricationYear()}\n"
            f"Model Year: {self.get_modelYear()}\n"
            f"Plate: {self.get_plate()}\n"
            f"Category: {self.get_category()}\n"
            f"Fipe Value: {self.get_fipe_value()}\n"
            f"Rent Value: {self.get_rent_Value()}\n"
            f"Is Available: {self.get_is_available()}\n"
        )

    # *************************************************************************
    # Getters and Setters
    # *************************************************************************
    def get_car_id(self):
        return self.car_id

    def get_model(self):
        return self.model

    def get_manufacturer(self):
        return self.manufacturer

    def get_fabricationYear(self):
        return self.fabrication_year

    def get_modelYear(self):
        return self.model_year

    def get_plate(self):
        return self.plate

    def get_category(self):
        return self.category

    def get_fipe_value(self):
        return self.fipe_value

    def get_rent_Value(self):
        return self.rent_value

    def get_is_available(self):
        return self.is_available

    def set_car_id(self, car_id):
        self.car_id = car_id

    def set_model(self, model):
        self.model = model

    def set_manufacturer(self, manufacturer):
        self.manufacturer = manufacturer

    def set_fabricationYear(self, fabrication_year):
        self.fabrication_year = fabrication_year

    def set_modelYear(self, model_year):
        self.model_year = model_year

    def set_plate(self, plate):
        self.plate = plate

    def set_category(self, category):
        self.category = category

    def set_fipe_value(self, fipe_value):
        self.fipe_value = fipe_value

    def set_rent_value(self, rent_value):
        self.rent_value = rent_value

    def set_is_available(self, isAvailable):
        self.isAvailable = isAvailable
