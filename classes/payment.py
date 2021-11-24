class insurance:
    def __init__(self, name: str, type: str, description: str, value: float):
        self.name = name
        self.type = type
        self.description = description
        self.value = value

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_description(self):
        return self.description

    def get_value(self):
        return self.value

    def set_name(self, name: str):
        self.name = name

    def set_type(self, type: str):
        self.type = type

    def set_description(self, description: str):
        self.description = description

    def set_value(self, value: float):
        self.value = value
