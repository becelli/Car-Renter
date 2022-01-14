from abc import ABC, abstractmethod
import model.classes.database as database


class Payment(ABC):
    def __init__(self, name: str, id: int = None) -> None:
        self._name: str = name
        self._id: int = id

    @abstractmethod
    def __str__(self):
        return f"{self.get_name()}"

    def save(self, db: str = "app.db"):
        ret = database.Database(db).insert_payment(self)
        if ret is not None:
            self._id = ret

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def set_name(self, name: str):
        self._name = name

    def set_id(self, id: int):
        self._id = id


class Cash(Payment):
    def __init__(self, name: str = "Dinheiro", id: int = None) -> None:
        self._name = name
        self._id = id

    def __str__(self):
        return f"{self.get_name()}"

    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name


class Card(Payment):
    def __init__(self, name: str, card_number: str, card_flag: str, id: int = None):
        super().__init__(name, id)
        self._card_number = card_number
        self._card_flag = card_flag

    def __str__(self):
        return (
            super().__str__() + f"\nNúmero do cartão: {self.get_card_number()}"
            f"\nBandeira: {self.get_card_flag()}"
        )

    def get_card_number(self):
        return self._card_number

    def get_card_flag(self):
        return self._card_flag

    def set_card_number(self, card_number: str):
        self._card_number = card_number

    def set_card_flag(self, card_holder: str):
        self._card_holder = card_holder
