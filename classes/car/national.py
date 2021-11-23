import classes.car.car as c


class national_car(c.Car):
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

    def calculate_daily_rent_value(self):
        return self.rent_value * (1 + self.get_state_taxes())

    def __str__(self):
        return super().__str__() + f"\nState Taxes: {self.get_state_taxes()}"

    # *************************************************************************
    # Getters and Setters
    # *************************************************************************
    def get_state_taxes(self):
        return self.state_taxes

    def set_state_taxes(self, state_taxes):
        self.state_taxes = state_taxes
