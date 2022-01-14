# from datetime import datetime as dt
import time
import random as rd
import controller.controller as c
from datetime import datetime as dt, timedelta as td

from model.classes.insurance import Insurance
from model.classes.payment import Payment


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
        self.database_name = database
        self.controller = c.Controller(database)
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
            cpf,
            rg,
            name,
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
                cpf,
                rg,
                name,
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
                cpf,
                rg,
                name,
                birth_date,
                address,
                zip_code,
                email,
                salary,
                pis,
                admission_date,
            )

    def payment(self, client_name: str = "desconhecido"):
        import model.classes.payment as payment

        c = rd.choice([0, 1])
        if c:
            return payment.Cash("Dinheiro")
        else:
            name = (
                self.basic_data.name() if client_name == "desconhecido" else client_name
            )
            name = "Cartão de " + name
            number = self.formats.nsize_num_as_str(16)
            flags = ["Visa", "Mastercard", "American Express", "Hipercard", "Elo"]
            flag = rd.choice(flags)
            return payment.Card(name, number, flag)

    def insurance(self):
        [name, model, description, value] = self.insurance_info()
        return Insurance(name, model, description, value)

    def default_insurances(self):
        insurance_types = [
            "Roubo",
            "Furto",
            "Acidente",
            "Incêndio",
            "Perda total",
            "Alagamento",
            "Dano mecânico",
        ]
        insurance_models = ["Reembolso", "Reposição"]
        insurance_description = [
            "Seguro contra roubos",
            "Seguro contra furto",
            "Seguro contra acidentes de trânsito",
            "Seguro contra incendios e explosões",
            "Seguro contra perda total de veículo",
            "Seguro contra alagamentos",
            "Seguro contra danos mecânicos",
        ]
        insurances = []
        for i in range(len(insurance_types)):
            i_type = insurance_types[i]
            i_model = rd.choice(insurance_models)
            description = insurance_description[i]
            insurances.append(
                Insurance(
                    f"Seguro contra {i_type}",
                    i_model,
                    description,
                    round(rd.randint(30, 60) + rd.random(), 2),
                )
            )
        return insurances

    def rent(self):
        import model.classes.rent as rent
        import model.classes.payment as pmt
        import model.classes.user as user

        data = self.rent_info()
        if data is None:
            return None
        else:
            [
                plate,
                client_cpf,
                employee_cpf,
                start_date,
                end_date,
                total_value,
                insurance,
                is_returned,
            ] = data

            clt: user.Client = self.controller.select_client(client_cpf)
            clt_str = clt.get_name() if clt is not None else "desconhecido"
            paymt: pmt.Payment = self.payment(clt_str)
            return rent.Rent(
                plate,
                client_cpf,
                employee_cpf,
                start_date,
                end_date,
                total_value,
                paymt,
                insurance,
                is_returned,
            )

    def rent_info(self):
        import model.classes.vehicle as vehicle
        import model.classes.user as user
        import model.classes.insurance as ins

        vehicles = self.controller.select_all_available_vehicles()
        employees = self.controller.select_all_employees()
        clients = self.controller.select_all_clients()
        v: vehicle.Vehicle = rd.choice(vehicles) if len(vehicles) > 0 else None
        e: user.Employee = rd.choice(employees) if len(employees) > 0 else None
        c: user.Client = rd.choice(clients) if len(clients) > 0 else None
        if v is None or e is None or c is None:
            return None
        else:
            year = rd.randint(2020, 2021)
            d = dt.strptime(self.formats.date_as_string(year, year + 1), "%Y-%m-%d")

            df = d + td(days=rd.randint(1, 14))

            value = v.calculate_daily_rent_value() * df.day

            insurances = self.controller.select_all_insurances()
            insurance = []
            for i in insurances:
                insurance.append(0)

            for insur in insurances:
                if rd.choice([0, 0, 0, 1]):
                    i: ins.Insurance = insur
                    value += i.get_value()
                    insurance[insurances.index(insur)] = 1

            is_returned = (
                rd.choice([True, True, False])
                if dt.now() > df
                else rd.choice([True, False, False])
            )

            return [
                v.get_plate(),
                c.get_cpf(),
                e.get_cpf(),
                d,
                df,
                value,
                insurance,
                is_returned,
            ]

    def user_info(self):

        name = self.basic_data.name()
        return [
            self.formats.nsize_num_as_str(11),  # cpf
            self.formats.nsize_num_as_str(9),  # rg
            name,  # user name
            self.formats.date_as_string(),  # birth_date
            f"Rua {self.basic_data.letter()}",  # address
            f"{self.formats.nsize_num_as_str(5)}-{self.formats.nsize_num_as_str(3)}",  # zip_code
            f"{name.split()[0].lower()}{rd.randint(0, 100000)}@mail.com",  # email
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
        value = 100
        return [
            rd.choice(model),
            rd.choice(brand),  # manufacturer
            fabrication_year,
            fabrication_year + rd.choice([0, 1]),  # model year
            self.basic_data.plate(),
            rd.choice(category),
            round(
                rd.random() * 10000 * rd.randint(4, 6), 2
            ),  # price based on FIPE table
            round(value + rd.random() * 100 * rd.randint(1, 3), 2),  # rent price
            rd.choice([True, False]),  # is available
            round(rd.random() / 3, 2),  # state taxes
            round(rd.random() / 4, 2),  # federal taxes
        ]

    def insurance_info(self):
        insurance_types = ["Roubo", "Furto", "Acidente", "Incendio", "Perda Total"]
        insurance_models = ["Reembolso", "Substituição"]
        insurance_description = [
            "Seguro contra roubos",
            "Seguro contra furto",
            "Seguro contra acidentes de trânsito",
            "Seguro contra incendios e explosões",
            "Seguro contra perda total de veículo",
        ]
        insurance = rd.choice(insurance_types)
        model = rd.choice(insurance_models)
        description = insurance_description[insurance_types.index(insurance)]
        return [
            f"Seguro contra {insurance}",
            model,
            description,
            round(rd.random() * 50 * rd.randint(1, 3), 2),  # price based on FIPE table
        ]


class BasicData:
    def __init__(self, db: str = "app.db"):
        self.controller = c.Controller(db)
        self.formats = Formats()

    def plate(self) -> str:
        letters = "".join(self.letter() for _i in range(3))
        return f"{letters}-{self.formats.nsize_num_as_str(4)}"

    def letter(self) -> str:
        return chr(rd.randint(65, 90))

    def card_flag(self) -> str:
        flags = ["Visa", "Mastercard", "American Express", "Hipercard", "Elo"]
        return rd.choice(flags)

    def name(self) -> str:
        firstname_list = [
            "Clara",
            "Wesley",
            "Gustavo",
            "João",
            "Maria",
            "José",
            "Pedro",
            "Paulo",
            "Lucas",
            "Joana",
            "Roberto",
            "Vinicius",
            "Mariana",
            "Ana",
            "Paula",
            "Larissa",
            "Marcos",
            "Joaquim",
            "Rafael",
            "Ricardo",
            "Fernando",
            "Luiz",
            "Eduardo",
            "Henrique",
            "Vitor",
            "Gabriel",
            "Clarisse",
            "Rafaela",
            "Leticia",
            "Bruno",
            "Roberta",
            "Daniel",
            "Emanuel",
            "Gabriela",
            "Eduarda",
            "Eva",
            "Adão",
            "Ana Paula",
            "Antônio",
            "Benedito",
            "Bianca",
            "Bruna",
            "Catarina",
            "Cecília",
            "Cristiane",
            "Davi",
            "Samuel",
            "Sophia",
            "Thiago",
            "Vitória",
            "Cleiton",
            "Cleverson",
            "Wagner",
            "Waldir",
            "Xavier",
            "Yuri",
            "Sérgio",
            "Sônia",
            "Fábio",
            "Fátima",
            "Fernando",
            "Fernanda",
            "Débora",
            "Décio",
            "Solange",
            "Sabrina",
            "Cristian",
            "Calisto",
        ]

        lastname_list = [
            "Silva",
            "Santos",
            "Oliveira",
            "Pereira",
            "Souza",
            "Costa",
            "Rodrigues",
            "Almeida",
            "Martins",
            "Araújo",
            "Simolini",
            "Becelli",
            "Borges",
            "Bruno",
            "Cabral",
            "Carvalho",
            "Cardoso",
            "Cunha",
            "Dias",
            "Domingues",
            "Fernandes",
            "Fernando",
            "Gomes",
            "Gonçalves",
            "Henrique",
            "Jesus",
            "Lima",
            "Lopes",
            "Macedo",
            "Moraes",
            "Moreira",
            "Moura",
            "Nascimento",
            "Nogueira",
            "Oliveira",
            "Pacheco",
            "Pereira",
            "Ramos",
            "Ribeiro",
            "Rocha",
            "Serra",
            "Teixeira",
            "Vieira",
            "Valente",
            "Voss",
            "Xavier",
            "Zanella",
            "Zanetti",
            "Zanin",
            "Zanoni",
            "Umbelino",
            "Umbelita",
            "Quaresma",
            "Queiroz",
            "Ernesto",
            "Bernardes",
            "Bianchi",
            "Bianco",
            "Brunelli",
            "Durante",
            "Duccio",
            "Duchini",
        ]

        return rd.choice(firstname_list) + " " + rd.choice(lastname_list)
