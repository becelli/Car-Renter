import classes.car.car as c


class international_car(c.Car):
    def __init__(
        self,
        id,
        model,
        manufacturer,
        fabrication_year,
        model_year,
        plate,
        category,
        fipe_value,
        rent_value,
        is_available,
        state_taxes,
        federal_taxes,
    ):
        super().__init__(
            id,
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
        self.state_taxes = state_taxes
        self.federal_taxes = federal_taxes

    def calculate_daily_rent_value(self, days):
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

    def set_state_taxes(self, state_taxes):
        self.state_taxes = state_taxes

    def set_federal_taxes(self, federal_taxes):
        self.federal_taxes = federal_taxes
