# from datetime import datetime as dt
import time
import random as rd

# import model.functions.database as db

# Generate random vehicle. National or Imported.
def vehicle(only_this_subclass=None):
    import model.classes.vehicle as vehicle

    choice = rd.randint(0, 1)
    if only_this_subclass == vehicle.National:
        choice = 0
    elif only_this_subclass == vehicle.Imported:
        choice = 1
    [
        model,
        manufacturer,
        fabrication_year,
        model_year,
        plate_number,
        category,
        price,
        rent_price,
        is_available,
        state_taxes,
        federal_taxes,
    ] = vehicle_info()

    if choice == 0:
        return vehicle.National(
            model,
            manufacturer,
            fabrication_year,
            model_year,
            plate_number,
            category,
            price,
            rent_price,
            is_available,
            state_taxes,
        )
    else:
        return vehicle.Imported(
            model,
            manufacturer,
            fabrication_year,
            model_year,
            plate_number,
            category,
            price,
            rent_price,
            is_available,
            state_taxes,
            federal_taxes,
        )


# Generate random user.
def user(only_this_subclass=None):
    import model.classes.user as user

    choice = rd.randint(0, 1)
    if isinstance(only_this_subclass, user.Client):
        choice = 0
    elif isinstance(only_this_subclass, user.Employee):
        choice = 1
    rd.seed(time.time())
    [
        name,
        cpf,
        rg,
        birth_date,
        address,
        zip_code,
        email,
        permission_category,
        permission_number,
        permission_expiration_date,
        is_golden_client,
        salary,
        pis,
        admission_date,
    ] = user_info()

    if choice == 0:
        return user.Client(
            name,
            cpf,
            rg,
            birth_date,
            address,
            zip_code,
            email,
            permission_category,
            permission_number,
            permission_expiration_date,
            is_golden_client,
        )
    else:
        return user.Employee(
            name,
            cpf,
            rg,
            birth_date,
            address,
            zip_code,
            email,
            salary,
            pis,
            admission_date,
        )


# def rent():
#     vehicle_id = db.select_all("vehicle")[0][0]
#     employee_id = db.select_all("employee")[0][0]
#     client_id = db.select_all("client")[0][0]


# User info for testing.
def user_info():
    import names as nm

    name = nm.get_full_name()
    return [
        name,  # user name
        nsize_num_as_str(11),  # cpf
        nsize_num_as_str(9),  # rg
        date_as_string(),  # birth_date
        f"Street {letter()}",  # address
        f"{nsize_num_as_str(5)}-{nsize_num_as_str(3)}",  # zip_code
        f"{name.split()[0].lower()}{rd.randint(0, 1000)}@mail.com",  # email
        rd.choice(["A", "B", "C", "D", "E"]),  # permission_category
        nsize_num_as_str(10),  # permission_number
        date_as_string(y_min=2022, y_max=2025)[:-3],  # permission_expiration_date
        rd.choice([True, False]),  # is_golden_client
        round(rd.random() * 10000, 2),  # salary
        nsize_num_as_str(11),  # pis
        date_as_string(y_min=2000, y_max=2020),  # admission_date
    ]


# Vehicle info for testing.
def vehicle_info():

    brand = [
        "Fiat",
        "Ford",
        "Chevrolet",
        "Honda",
        "Hyundai",
        "Toyota",
        "Volkswagen",
        "Audi",
        "BMW",
        "Mercedes",
    ]
    model = [
        "Uno",
        "Fiesta",
        "Fusion",
        "Corsa",
        "Civic",
        "Corolla",
        "Gol",
        "Astra",
        "Santana",
        "S10",
    ]
    category = ["car", "motorcycle", "truck", "bus", "van", "bicycle"]
    fabrication_year = rd.randint(1990, 2021)
    return [
        rd.choice(model),
        rd.choice(brand),  # manufacturer
        fabrication_year,
        fabrication_year + rd.randint(-1, 1),  # model year
        plate_number(),
        rd.choice(category),
        round(rd.random() * 10000 * rd.randint(1, 6), 2),  # price based on FIPE table
        round(rd.random() * 100 * rd.randint(1, 3), 2),  # rent price
        rd.choice([True, False]),  # is available
        round(rd.random() / 3, 2),  # state taxes
        round(rd.random() / 4, 2),  # federal taxes
    ]


# Generate random date as a string.
def date_as_string(y_min: int = 1950, y_max: int = 2003):

    birth_day = nsize_padded_num_as_str(2, 1, 28)
    birth_month = nsize_padded_num_as_str(2, 1, 12)
    birth_year = nsize_padded_num_as_str(4, y_min, y_max)
    birth_date = f"{birth_year}-{birth_month}-{birth_day}"
    return birth_date


# Generate random letter.
def letter():
    return chr(rd.randint(65, 90))


def nsize_padded_num_as_str(size: int, min_value: int = 0, max_value: int = 9):
    num = rd.randint(min_value, max_value)
    num = str(num)
    for _i in range(size - len(num)):
        num = "0" + num
    return num


# Generate random number with a fixed size. It may contain zeros at the beginning.
def nsize_num_as_str(size: int, min_value: int = 0, max_value: int = 9):
    num = ""
    for _i in range(size):
        num += str(rd.randint(min_value, max_value))
    return num


# Generate random plate number.
def plate_number():
    letters = "".join(letter() for _i in range(3))
    return f"{letters}-{nsize_num_as_str(4)}"
