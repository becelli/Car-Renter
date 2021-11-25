from abc import ABC, abstractmethod
from dataclasses import dataclass
import model.functions.database as db


@dataclass
class Payment(ABC):
    _name: str

    @abstractmethod
    def __str__(self):
        return f"Payment method: {self.get_name()}"

    @abstractmethod
    def save(self):
        pass

    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name


@dataclass
class Cash(Payment):
    def __str__(self):
        return super().__str__()

    def save(self):
        db.insert_payment(self)


@dataclass
class Card(Payment):
    _card_holder: str
    _card_number: str
    _card_flag: str

    def save(self):
        db.insert_payment(self)

    def __str__(self):
        return (
            super().__str__() + f"\nCard Holder: {self.get_card_holder()}"
            f"\nCard Number: {self.get_card_number()}"
            f"\nCard Flag: {self.get_card_flag()}"
        )

    # **********************************************************************************************************************
    # Getters and Setters
    # **********************************************************************************************************************
    def get_card_holder(self):
        return self._card_holder

    def get_card_number(self):
        return self._card_number

    def get_card_flag(self):
        return self._card_flag

    def set_card_holder(self, card_holder: str):
        self._card_holder = card_holder

    def set_card_number(self, card_number: str):
        self._card_number = card_number

    def set_card_flag(self, card_holder: str):
        self._card_holder = card_holder
