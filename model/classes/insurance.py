import model.classes.database as db


class Insurance:
    def __init__(
        self, name: str, model: str, description: str, value: float, id: int = None
    ):
        self._name: str = name
        self._model: str = model
        self._description: str = description
        self._value: str = value
        self._id: int = id

    def save(self, database: str = "app.db"):
        ret = db.Database(database).insert_insurance(self)
        if ret is not None:
            self._id = ret

    def __str__(self):
        return (
            f"Identificador: {self.get_id()} \n"
            f"Nome: {self.get_name()} \n"
            f"Modelo: {self.get_model()} \n"
            f"Descrição: {self.get_description()} \n"
            f"Valor: {self.get_value()} \n"
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
