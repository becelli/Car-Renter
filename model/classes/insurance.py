from dataclasses import dataclass


@dataclass
class insurance:
    _name: str
    _model: str
    _description: str
    _value: float

    def __str__(self):
        return (
            f"ID: {self._get_id()} \n"
            f"Name: {self.get_name()} \n"
            f"Model: {self.get_model()} \n"
            f"Description: {self.get_description()} \n"
            f"Value: {self.get_value()} \n"
        )

    # *************************************************************************************************************************
    # Getters and Setters
    # *************************************************************************************************************************
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_model(self):
        return self._model

    def get_description(self):
        return self._description

    def get_value(self):
        return self._value

    def set_name(self, name: str):
        self._name = name

    def set_model(self, model: str):
        self._model = model

    def set_description(self, description: str):
        self._description = description

    def set_value(self, value: float):
        self._value = value
