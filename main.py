# Init database
import sqlite3 as sql

cars = sql.connect("./db/application.db")
cursor = cars.cursor()

# Classes dependencies
import classes.car.national as nc
import classes.car.international as ic


# Example of a car
car1 = nc.national_car(
    1, "Qwid", "Renault", 2018, 2018, "CHW9797", "Sedan", 34000, 200, True, 0.12
)
car2 = ic.international_car(
    2, "Onix", "Chevrolet", 2021, 2020, "BKV3413", "Sedan", 52300, 200, True, 0.10, 0.05
)

print(car1.__str__())
print(car1.calculate_daily_rent_value())

print(car2.__str__())
print(car2.calculate_daily_rent_value())
