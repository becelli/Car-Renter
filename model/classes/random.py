# from datetime import datetime as dt
import time
import random as rd
import model.classes.database as db
from datetime import datetime as dt, timedelta as td

from model.classes.insurance import Insurance


class Formats:
    def __init__(self):
        pass

    # Generate random date as a string.
    def date_as_string(self, y_min: int = 1950, y_max: int = 2003):

        birth_day = self.nsize_padded_num_as_str(2, 1, 28)
        birth_month = self.nsize_padded_num_as_str(2, 1, 12)
        birth_year = self.nsize_padded_num_as_str(4, y_min, y_max)
        birth_date = f"{birth_year}-{birth_month}-{birth_day}"
        return birth_date

    # Generate random letter.

    def nsize_padded_num_as_str(
        self, size: int, min_value: int = 0, max_value: int = 9
    ):
        num = rd.randint(min_value, max_value)
        num = str(num)
        for _i in range(size - len(num)):
            num = "0" + num
        return num

    # Generate random number with a fixed size. It may contain zeros at the beginning.
    def nsize_num_as_str(self, size: int, min_value: int = 0, max_value: int = 9):
        num = ""
        for _i in range(size):
            num += str(rd.randint(min_value, max_value))
        return num


class ClassesData:
    def __init__(self, database: str = "app.db"):
        self.db = db.Database(database)
        self.basic_data = BasicData(database)
        self.formats = Formats()

        # Generate random vehicle. National or Imported.

    def vehicle(self, only_this_subclass=None):
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
            plate,
            category,
            price,
            rent_price,
            is_available,
            state_taxes,
            federal_taxes,
        ] = self.vehicle_info()

        if choice == 0:
            return vehicle.National(
                plate,
                model,
                manufacturer,
                fabrication_year,
                model_year,
                category,
                price,
                rent_price,
                is_available,
                state_taxes,
            )
        else:
            return vehicle.Imported(
                plate,
                model,
                manufacturer,
                fabrication_year,
                model_year,
                category,
                price,
                rent_price,
                is_available,
                state_taxes,
                federal_taxes,
            )

    def user(self, only_this_subclass=None):
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
        ] = self.user_info()

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

    def rent(self):
        vehicles = db.select_all_vehicles()
        employees = db.select_all_employees()
        clients = db.select_all_clients()
        v = rd.choice(vehicles)
        e = rd.choice(employees)
        c = rd.choice(clients)
        year = rd.randint(2019, 2021)
        d = dt.strptime(self.formats.date_as_string(year, year + 1), "%d/%m/%Y")
        df = d + td(days=rd.randint(15, 45))
        import model.classes.rent as rent

        r = rent.Rent(
            v.get_plate(),
            c.get_cpf(),
            e.get_cpf(),
            d,
            df,
            float(rd.randint(200, 700)) + rd.random() * 100,
        )

    def payment(self):
        import model.classes.payment as payment

        c = rd.choice([0, 1])
        if c:
            return payment.Cash()
        else:
            name = self.basic_data.name()
            number = self.formats.nsize_num_as_str(16)
            flags = ["Visa", "Mastercard", "American Express", "Hipercard", "Elo"]
            flag = rd.choice(flags)
            return payment.Card(name, number, flag)

    def insurance(self):
        [name, model, description, value] = self.insurance_info()
        return Insurance(name, model, description, value)

    # User info for testing.
    def user_info(self):

        name = self.basic_data.name()
        return [
            name,  # user name
            self.formats.nsize_num_as_str(11),  # cpf
            self.formats.nsize_num_as_str(9),  # rg
            self.formats.date_as_string(),  # birth_date
            f"Street {self.basic_data.letter()}",  # address
            f"{self.formats.nsize_num_as_str(5)}-{self.formats.nsize_num_as_str(3)}",  # zip_code
            f"{name.split()[0].lower()}{rd.randint(0, 1000)}@mail.com",  # email
            rd.choice(["A", "B", "C", "D", "E"]),  # permission_category
            self.formats.nsize_num_as_str(10),  # permission_number
            self.formats.date_as_string(y_min=2022, y_max=2025)[
                :-3
            ],  # permission_expiration_date
            rd.choice([True, False]),  # is_golden_client
            round(rd.random() * 10000, 2),  # salary
            self.formats.nsize_num_as_str(11),  # pis
            self.formats.date_as_string(y_min=2000, y_max=2020),  # admission_date
        ]

    # Vehicle info for testing.
    def vehicle_info(self):

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
        category = ["CARRO", "MOTOCICLETA", "CAMINHAO", "ONIBUS", "VAN", "BICICLETA"]
        fabrication_year = rd.randint(1990, 2021)
        return [
            rd.choice(model),
            rd.choice(brand),  # manufacturer
            fabrication_year,
            fabrication_year + rd.choice([0, 1]),  # model year
            self.basic_data.plate(),
            rd.choice(category),
            round(
                rd.random() * 10000 * rd.randint(1, 6), 2
            ),  # price based on FIPE table
            round(rd.random() * 100 * rd.randint(1, 3), 2),  # rent price
            rd.choice([True, False]),  # is available
            round(rd.random() / 3, 2),  # state taxes
            round(rd.random() / 4, 2),  # federal taxes
        ]

    def insurance_info(self):
        insurance_types = ["Roubo", "Furto", "Acidente", "Incendio", "Perda Total"]
        insurance_description = [
            "Seguro contra roubos",
            "Seguro contra furto",
            "Seguro contra acidentes de trânsito",
            "Seguro contra incendios e explosões",
            "Seguro contra perda total de veículo",
        ]
        insurance = rd.choice(insurance_types)
        description = insurance_description[insurance_types.index(insurance)]
        return [
            f"Seguro {rd.choice(insurance)}",
            insurance,
            description,
            round(
                rd.random() * 10000 * rd.randint(1, 3), 2
            ),  # price based on FIPE table
        ]


class BasicData:
    def __init__(self, database):
        self.db = db.Database(database)
        self.formats = Formats()

    def plate(self) -> str:
        letters = "".join(self.letter() for _i in range(3))
        return f"{letters}-{self.formats.nsize_num_as_str(4)}"

    def letter(self) -> str:
        return chr(rd.randint(65, 90))

    def name(self) -> str:
        firstname_list = [
            "Carol",
            "William",
            "Chloe",
            "Linda",
            "Paul",
            "Oliver",
            "Jessica",
            "Anna",
            "George",
            "Thomas",
            "Elizabeth",
            "James",
            "Mia",
            "Jack",
            "Sophie",
            "Olivia",
            "Harry",
            "Isabella",
            "Jacob",
            "Jessica",
            "Noah",
            "Emily",
            "Liam",
            "Ava",
            "Alfie",
            "Isla",
            "Aria",
            "Daniel",
            "Chloe",
            "Lucas",
            "Sophia",
            "Harry",
            "Amelia",
            "Ethan",
            "Mia",
            "Jacob",
            "Charlotte",
            "Michael",
            "Abigail",
            "Alexander",
            "Elizabeth",
            "William",
            "Olivia",
            "James",
            "Isabella",
            "Benjamin",
            "Sophia",
            "Elijah",
            "Amelia",
            "Lucas",
            "Chloe",
            "Hannah",
            "Jack",
            "Charlotte",
            "Joshua",
            "Charlotte",
            "William",
            "Olivia",
            "James",
            "Isabella",
            "William",
            "Amelia",
            "James",
            "Emily",
            "Daniel",
            "Abigail",
            "Lucas",
            "Ava",
            "Ethan",
            "Charlotte",
            "Lucas",
            "Chloe",
            "Jack",
            "Charlotte",
            "Joshua",
            "Charlotte",
            "William",
            "Olivia",
            "James",
            "Isabella",
            "William",
            "Amelia",
            "James",
            "Emily",
            "Daniel",
            "Abigail",
            "Lucas",
            "Ava",
            "Ethan",
            "Charlotte",
            "Lucas",
            "Chloe",
            "Jack",
            "Charlotte",
            "Joshua",
            "Charlotte",
            "William",
            "Olivia",
            "James",
            "Isabella",
            "William",
            "Amelia",
            "James",
            "Emily",
            "Daniel",
            "Abigail",
            "Lucas",
            "Ava",
            "Ethan",
            "Charlotte",
            "Lucas",
            "Chloe",
            "Jack",
            "Charlotte",
            "Joshua",
            "Charlotte",
            "William",
            "Olivia",
            "James",
            "Isabella",
            "William",
            "Amelia",
            "James",
            "Emily",
            "Daniel",
            "Abigail",
            "Lucas",
            "Ava",
            "Ethan",
            "Charlotte",
            "Lucas",
            "Chloe",
            "Jack",
            "Charlotte",
            "Joshua",
            "Charlotte",
            "Oliver",
        ]

        lastname_list = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
            "Hernandez",
            "Lopez",
            "Gonzalez",
            "Wilson",
            "Anderson",
            "Thomas",
            "Taylor",
            "Moore",
            "Jackson",
            "Martin",
            "Lee",
            "Perez",
            "Thompson",
            "White",
            "Harris",
            "Sanchez",
            "Clark",
            "Ramirez",
            "Lewis",
            "Robinson",
            "Walker",
            "Young",
            "Allen",
            "King",
            "Wright",
            "Scott",
            "Torres",
            "Nguyen",
            "Hill",
            "Flores",
            "Green",
            "Adams",
            "Nelson",
            "Baker",
            "Hall",
            "Rivera",
            "Campbell",
            "Mitchell",
            "Carter",
            "Roberts",
        ]

        return rd.choice(firstname_list) + " " + rd.choice(lastname_list)


class DBGetter:
    def __init__(self, database):
        self.db = db.Database(database)

    def client(self):
        clients = self.db.select_all_clients()
        return rd.choice(clients)

    def employee(self):
        employees = self.db.select_all_employees()
        return rd.choice(employees)

    def national_vehicle(self):
        national_vehicles = self.db.select_all_national_vehicles()
        return rd.choice(national_vehicles)

    def imported_vehicle(self):
        imported_vehicles = self.db.select_all_imported_vehicles()
        return rd.choice(imported_vehicles)
