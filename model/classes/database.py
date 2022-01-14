# Init database
from datetime import datetime
import sqlite3 as sql3
import model.classes.user as user
import model.classes.vehicle as vehicle
import model.classes.converter as converter
import model.classes.payment as payment
import model.classes.insurance as insurance
import model.classes.rent as rent
import model.classes.random as rand


class Database:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = sql3.connect(f"model/database/{self.database_name}")
        self.cursor = self.connection.cursor()

    def init_tables(self):
        self.cursor.execute("PRAGMA foreign_keys = ON;").fetchone()

        if self.verify_if_table_exists("user") is False:
            self.create_user_table()

        if self.verify_if_table_exists("client") is False:
            self.create_client_table()

        if self.verify_if_table_exists("employee") is False:
            self.create_employee_table()

        if self.verify_if_table_exists("vehicle") is False:
            self.create_vehicle_table()

        if self.verify_if_table_exists("national_vehicle") is False:
            self.create_national_vehicle_table()

        if self.verify_if_table_exists("imported_vehicle") is False:
            self.create_imported_vehicle_table()

        if self.verify_if_table_exists("rent") is False:
            self.create_rent_table()

        if self.verify_if_table_exists("payment") is False:
            self.create_payment_table()

        if self.verify_if_table_exists("payment_cash") is False:
            self.create_payment_cash_table()

        if self.verify_if_table_exists("payment_card") is False:
            self.create_payment_card_table()

        if self.verify_if_table_exists("insurance") is False:
            self.create_insurance_table()

    def is_empty(self, table):
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall() == []

    def create_user_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS user (
            cpf CHAR(11) PRIMARY KEY,
            role TEXT NOT NULL CHECK (role IN ('client', 'employee')),
            rg CHAR(9) NOT NULL UNIQUE,
            name TEXT NOT NULL,
            birth_date DATE NOT NULL,
            address TEXT NOT NULL,
            zip_code CHAR(8) NOT NULL,
            email TEXT NOT NULL,
            active BOOL NOT NULL DEFAULT TRUE
            )"""
        )

    def create_client_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS client (
            cpf CHAR(11) PRIMARY KEY,
            permission_category CHAR(1) CHECK (permission_category IN ('A', 'B', 'C', 'D', 'E')),
            permission_number CHAR(10) UNIQUE,
            permission_expiration DATE,
            is_golden_client BOOL DEFAULT FALSE,
            FOREIGN KEY (cpf) REFERENCES user (cpf) ON DELETE CASCADE
            )"""
        )

    def create_employee_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS employee (
            cpf CHAR(11) PRIMARY KEY,
            salary REAL CHECK (salary >= 0) DEFAULT 0.00,
            pis CHAR(11) UNIQUE,
            admission_date DATE,
            FOREIGN KEY (cpf) REFERENCES user (cpf) ON DELETE CASCADE
            )"""
        )

    def create_vehicle_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS vehicle (
            plate CHAR(8) PRIMARY KEY,
            origin TEXT NOT NULL,
            model TEXT NOT NULL,
            manufacturer TEXT NOT NULL,
            fabrication_year INTEGER NOT NULL,
            model_year INT NOT NULL,
            category TEXT NOT NULL CHECK (category IN ('CARRO', 'MOTOCICLETA', 'CAMINHAO', 'ONIBUS', 'VAN', 'BICICLETA')),
            fipe_value REAL NOT NULL CHECK (fipe_value > 0) DEFAULT 5000.00,
            rent_value REAL NOT NULL CHECK (rent_value > 0) DEFAULT 100.00,
            is_available BOOL NOT NULL DEFAULT TRUE,
            active BOOL NOT NULL DEFAULT TRUE
            )"""
        )

    def create_national_vehicle_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS national_vehicle (
            plate CHAR(8) PRIMARY KEY,
            state_taxes REAL NOT NULL DEFAULT 0.00,
            FOREIGN KEY (plate) REFERENCES vehicle (plate) ON DELETE CASCADE
            )"""
        )

    def create_imported_vehicle_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS imported_vehicle (
            plate CHAR(8) PRIMARY KEY,
            state_taxes REAL NOT NULL CHECK (state_taxes >= 0) DEFAULT 0.00,
            federal_taxes REAL NOT NULL CHECK (federal_taxes >= 0) DEFAULT 0.00,
            FOREIGN KEY (plate) REFERENCES vehicle (plate) ON DELETE CASCADE
            )"""
        )

    def create_rent_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS rent (
            id INTEGER PRIMARY KEY,
            vehicle CHAR(8) NOT NULL,
            client CHAR(11) NOT NULL,
            employee CHAR(11) NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            value REAL NOT NULL CHECK (value >= 0) DEFAULT 0.00,
            payment_id INTEGER,
            insurance INTEGER NOT NULL CHECK (insurance >= 0) DEFAULT 0.00,
            is_returned BOOL NOT NULL DEFAULT TRUE,
            FOREIGN KEY (vehicle) REFERENCES vehicle (plate),
            FOREIGN KEY (client) REFERENCES client (cpf),
            FOREIGN KEY (employee) REFERENCES employee (cpf),
            FOREIGN KEY (payment_id) REFERENCES payment (id) ON DELETE CASCADE
            )"""
        )

    def create_payment_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS payment (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
            )"""
        )

    def create_payment_cash_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS cash (
            id INTEGER NOT NULL,
            name TEXT NOT NULL DEFAULT 'Dinheiro',
            FOREIGN KEY (id) REFERENCES payment (id) ON DELETE CASCADE
            FOREIGN KEY (name) REFERENCES payment (name)
            )"""
        )

    def create_payment_card_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS card (
            id INTEGER NOT NULL,
            name TEXT NOT NULL,
            card_number CHAR(16),
            card_flag TEXT,
            FOREIGN KEY (id) REFERENCES payment (id) ON DELETE CASCADE
            FOREIGN KEY (name) REFERENCES payment (name)
            )"""
        )

    def create_insurance_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS insurance (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            model TEXT NOT NULL,
            description TEXT NOT NULL,
            value REAL NOT NULL CHECK (value >= 0) DEFAULT 0.00
            )"""
        )

    def verify_if_table_exists(self, table_name: str):
        self.cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        )
        return self.cursor.fetchone() is not None

    # Random Inserts
    def populate_user(self, quantity: int = 10):
        for _i in range(quantity):
            u = rand.ClassesData(self.database_name).user()
            u.save(self.database_name)

    def populate_vehicle(self, quantity: int = 10):
        for _i in range(quantity):
            v = rand.ClassesData(self.database_name).vehicle()
            v.save(self.database_name)

    def populate_rent(self, quantity: int = 10):
        for _i in range(quantity):
            r: rent.Rent = rand.ClassesData(self.database_name).rent()
            p: payment.Payment = r.get_payment()
            p.save(self.database_name)
            r.save(self.database_name)

    def populate_payment(self, quantity: int = 10):
        for _i in range(quantity):
            p = rand.ClassesData(self.database_name).payment()
            p.save(self.database_name)

    def populate_insurance(self):
        di = rand.ClassesData(self.database_name).default_insurances()
        for i in di:
            i.save(self.database_name)

    # USER #
    def insert_user(self, user_object: user.User):
        self.cursor.execute(
            """INSERT INTO user (cpf, role, rg, name, birth_date, address, zip_code, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_object.get_cpf(),
                "client" if isinstance(user_object, user.Client) else "employee",
                user_object.get_rg(),
                user_object.get_name(),
                user_object.get_birth_date(),
                user_object.get_address(),
                user_object.get_zip_code(),
                user_object.get_email(),
            ),
        )
        if isinstance(user_object, user.Client):
            self.insert_client(user_object)
        elif isinstance(user_object, user.Employee):
            self.insert_employee(user_object)
        self.connection.commit()

    def insert_employee(self, employee: user.Employee):
        self.cursor.execute(
            "INSERT INTO employee (cpf, salary, pis, admission_date) VALUES (?, ?, ?, ?)",
            (
                employee.get_cpf(),
                employee.get_salary(),
                employee.get_pis(),
                employee.get_admission_date(),
            ),
        )

    def insert_client(self, client: user.Client):
        self.cursor.execute(
            "INSERT INTO client (cpf, permission_category, permission_number, permission_expiration, is_golden_client) VALUES (?,?,?,?, ?)",
            (
                client.get_cpf(),
                client.get_permission_category(),
                client.get_permission_number(),
                client.get_permission_expiration(),
                client.get_is_golden_client(),
            ),
        )

    # VEHICLES #
    def select_vehicle(self, plate: str):
        self.cursor.execute(f"SELECT * FROM vehicle WHERE plate = '{plate}'")
        v = self.cursor.fetchone()
        [
            plate,
            origin,
            model,
            manufacturer,
            fabrication_year,
            model_year,
            category,
            fipe_value,
            rent_value,
            is_available,
            active,
        ] = v
        if active:
            if origin == "national":
                q = self.cursor.execute(
                    f"""SELECT state_taxes FROM national_vehicle WHERE plate = '{plate}'"""
                ).fetchone()
                [state_taxes] = q
                return vehicle.National(
                    plate,
                    model,
                    manufacturer,
                    fabrication_year,
                    model_year,
                    category,
                    fipe_value,
                    rent_value,
                    is_available,
                    state_taxes,
                )
            elif origin == "imported":
                q = self.cursor.execute(
                    f"""SELECT state_taxes, federal_taxes FROM imported_vehicle WHERE plate = '{plate}'"""
                ).fetchone()
                [state_taxes, federal_taxes] = q
                return vehicle.Imported(
                    plate,
                    model,
                    manufacturer,
                    fabrication_year,
                    model_year,
                    category,
                    fipe_value,
                    rent_value,
                    is_available,
                    state_taxes,
                    federal_taxes,
                )
        return None

    def insert_vehicle(self, vehicle_object: vehicle.Vehicle):
        self.cursor.execute(
            "INSERT INTO vehicle (model, origin, manufacturer, fabrication_year, model_year, plate, category, fipe_value, rent_value) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                vehicle_object.get_model(),
                "national"
                if isinstance(vehicle_object, vehicle.National)
                else "imported",
                vehicle_object.get_manufacturer(),
                vehicle_object.get_fabrication_year(),
                vehicle_object.get_model_year(),
                vehicle_object.get_plate(),
                vehicle_object.get_category(),
                vehicle_object.get_fipe_value(),
                vehicle_object.get_rent_value(),
            ),
        )
        if isinstance(vehicle_object, vehicle.National):
            self.insert_national(vehicle_object)
        elif isinstance(vehicle_object, vehicle.Imported):
            self.insert_imported(vehicle_object)
        self.connection.commit()

    def insert_national(self, vehicle_object: vehicle.National):
        self.cursor.execute(
            """INSERT INTO national_vehicle (plate, state_taxes) VALUES (?,?)""",
            (
                vehicle_object.get_plate(),
                vehicle_object.get_state_taxes(),
            ),
        )

    def insert_imported(self, vehicle_object: vehicle.Imported):
        self.cursor.execute(
            "INSERT INTO imported_vehicle (plate, state_taxes, federal_taxes) VALUES (?, ?, ?)",
            (
                vehicle_object.get_plate(),
                vehicle_object.get_state_taxes(),
                vehicle_object.get_federal_taxes(),
            ),
        )

    # PAYMENTS #
    def insert_payment(self, payment_object: payment.Payment):
        id = self.cursor.execute(
            "INSERT INTO payment (name) VALUES (?)",
            (payment_object.get_name(),),
        ).lastrowid
        if isinstance(payment_object, payment.Cash):
            self.insert_cash(payment_object, id)
        elif isinstance(payment_object, payment.Card):
            self.insert_card(payment_object, id)
        self.connection.commit()
        return id

    def insert_cash(self, payment_object: payment.Cash, id):
        self.cursor.execute(
            "INSERT INTO cash (id, name) VALUES (?, ?)",
            (
                id,
                payment_object.get_name(),
            ),
        )

    def insert_card(self, payment_object: payment.Card, id):
        self.cursor.execute(
            "INSERT INTO card (id, name, card_number, card_flag) VALUES (?, ?, ?, ?)",
            (
                id,
                payment_object.get_name(),
                payment_object.get_card_number(),
                payment_object.get_card_flag(),
            ),
        )

    # INSURANCES #
    def insert_insurance(self, insurance_object: insurance.Insurance):
        id = self.cursor.execute(
            "INSERT INTO insurance (name, model, description, value) VALUES (?, ?, ?, ?)",
            (
                insurance_object.get_name(),
                insurance_object.get_model(),
                insurance_object.get_description(),
                insurance_object.get_value(),
            ),
        ).lastrowid
        self.connection.commit()
        return id

    # RENT #
    def insert_rent(self, rent_object: rent.Rent) -> int:
        insurances = rent_object.get_insurance()
        insurance = converter.Converter().b_list2dec(insurances)
        obj_payment: payment.Payment = rent_object.get_payment()
        payment_id = obj_payment.get_id() if obj_payment else None

        id = self.cursor.execute(
            "INSERT INTO rent (vehicle, client, employee, start_date, end_date, value, payment_id, insurance, is_returned) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                rent_object.get_vehicle_plate(),
                rent_object.get_client_cpf(),
                rent_object.get_employee_cpf(),
                rent_object.get_start_date(),
                rent_object.get_end_date(),
                rent_object.get_total_value(),
                payment_id,
                insurance,
                rent_object.get_is_returned(),
            ),
        ).lastrowid
        self.cursor.execute(
            "UPDATE vehicle SET is_available = ? WHERE plate = ?",
            (False, rent_object.get_vehicle_plate()),
        )
        self.connection.commit()
        return id

    def select_all_users(self):
        self.cursor.execute("SELECT * FROM user WHERE active = 1")
        query_result = self.cursor.fetchall()
        users = []
        for user in query_result:
            [cpf, role, rg, name, birth_date, address, zip_code, email, active] = user
            if active:
                if role == "client":
                    self.cursor.execute(f"SELECT * FROM {role} WHERE cpf = '{cpf}'")
                    query_result_2 = self.cursor.fetchone()
                    [
                        permission_category,
                        permission_number,
                        permission_expiration,
                        is_golden_client,
                    ] = query_result_2
                    users.append(
                        user.Client(
                            cpf,
                            rg,
                            name,
                            birth_date,
                            address,
                            zip_code,
                            email,
                            permission_category,
                            permission_number,
                            permission_expiration,
                            is_golden_client,
                        )
                    )
                elif role == "employee":
                    self.cursor.execute(f"SELECT * FROM {role} WHERE cpf = '{cpf}'")
                    query_result_2 = self.cursor.fetchone()
                    [
                        salary,
                        pis,
                        admission_date,
                    ] = query_result_2
                    users.append(
                        user.Employee(
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
                    )
        return users

    def select_all_vehicles(self):
        self.cursor.execute("SELECT * FROM vehicle WHERE active = 1")
        query_result = self.cursor.fetchall()
        vehicles = []
        for query in query_result:
            [
                plate,
                origin,
                model,
                manufacturer,
                fabrication_year,
                model_year,
                category,
                fipe_value,
                rent_value,
                is_available,
                active,
            ] = query
            if active:
                if origin == "imported":
                    self.cursor.execute(
                        f"SELECT state_taxes, federal_taxes FROM {origin}_vehicle WHERE plate = '{plate}'"
                    )
                    query_result = self.cursor.fetchone()
                    [state_taxes, federal_taxes] = query_result
                    vehicles.append(
                        vehicle.Imported(
                            plate,
                            model,
                            manufacturer,
                            fabrication_year,
                            model_year,
                            category,
                            fipe_value,
                            rent_value,
                            is_available,
                            state_taxes,
                            federal_taxes,
                        )
                    )
                elif origin == "national":
                    self.cursor.execute(
                        f"SELECT state_taxes FROM {origin}_vehicle WHERE plate = '{plate}'"
                    )
                    query_result = self.cursor.fetchone()
                    [state_taxes] = query_result
                    vehicles.append(
                        vehicle.National(
                            plate,
                            model,
                            manufacturer,
                            fabrication_year,
                            model_year,
                            category,
                            fipe_value,
                            rent_value,
                            is_available,
                            state_taxes,
                        )
                    )
        return vehicles

    def select_all_available_vehicles(self) -> list:
        self.cursor.execute(
            "SELECT * FROM vehicle WHERE active = 1 AND is_available = 1"
        )
        query_result = self.cursor.fetchall()
        vehicles = []
        for query in query_result:
            [
                plate,
                origin,
                model,
                manufacturer,
                fabrication_year,
                model_year,
                category,
                fipe_value,
                rent_value,
                is_available,
                active,
            ] = query
            if active:
                if origin == "imported":
                    self.cursor.execute(
                        f"SELECT state_taxes, federal_taxes FROM {origin}_vehicle WHERE plate = '{plate}'"
                    )
                    query_result = self.cursor.fetchone()
                    [state_taxes, federal_taxes] = query_result
                    vehicles.append(
                        vehicle.Imported(
                            plate,
                            model,
                            manufacturer,
                            fabrication_year,
                            model_year,
                            category,
                            fipe_value,
                            rent_value,
                            is_available,
                            state_taxes,
                            federal_taxes,
                        )
                    )
                elif origin == "national":
                    self.cursor.execute(
                        f"SELECT state_taxes FROM {origin}_vehicle WHERE plate = '{plate}'"
                    )
                    query_result = self.cursor.fetchone()
                    [state_taxes] = query_result
                    vehicles.append(
                        vehicle.National(
                            plate,
                            model,
                            manufacturer,
                            fabrication_year,
                            model_year,
                            category,
                            fipe_value,
                            rent_value,
                            is_available,
                            state_taxes,
                        )
                    )
        return vehicles

    def select_all_payments(self):
        self.cursor.execute("SELECT * FROM payment")
        query_result = self.cursor.fetchall()
        payments = []
        for query in query_result:
            self.cursor.execute(f"SELECT * FROM cash WHERE id = '{query[0]}'")
            q = self.cursor.fetchone()
            if q is not None and q != []:
                [id, name] = q
                payments.append(payment.Cash(name="ovo", id=id))
            else:
                self.cursor.execute(f"SELECT * FROM card WHERE id = '{id}'")
                query_result = self.cursor.fetchone()
                [
                    id,
                    name,
                    card_holder,
                    card_number,
                    card_flag,
                ] = query_result
                payments.append(
                    payment.Card(
                        name,
                        card_holder,
                        card_number,
                        card_flag,
                        id,
                    )
                )

        return payments

    def select_all_rents(self):
        self.cursor.execute("SELECT * FROM rent")
        query_result = self.cursor.fetchall()
        rents = []
        for query in query_result:
            [
                id,
                vehicle_plate,
                client_cpf,
                employee_cpf,
                start_date,
                end_date,
                value,
                payment_id,
                insurance_sum,
                is_returned,
            ] = query
            insurances = converter.Converter().dec2b_list(insurance_sum)
            insurances_list = []
            for i in range(len(insurances)):
                ins = insurances[i]
                if ins == 1:
                    self.cursor.execute(
                        f"SELECT * FROM insurance WHERE id = '{2 ** i}'"
                    )
                    query_result = self.cursor.fetchone()
                    [
                        _,
                        name,
                        model,
                        description,
                        value,
                    ] = query_result
                    insurances_list.append(
                        insurance.Insurance(
                            2 ** i,
                            name,
                            model,
                            description,
                            value,
                        )
                    )
            payment_obj = None
            self.cursor.execute(f"SELECT * FROM cash WHERE id = '{payment_id}'")
            payment_data = self.cursor.fetchone()
            if payment_data is not None:
                payment_obj = payment.Cash(payment_data[1])
            else:
                self.cursor.execute(f"SELECT * FROM card WHERE id = '{payment_id}'")
                payment_data = self.cursor.fetchone()
                if payment_data is not None:
                    payment_obj = payment.Card(
                        payment_data[1],
                        payment_data[2],
                        payment_data[3],
                        payment_data[0],
                    )
            rents.append(
                rent.Rent(
                    vehicle_plate,
                    client_cpf,
                    employee_cpf,
                    datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S"),
                    datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S"),
                    value,
                    payment_obj,
                    insurances_list,
                    is_returned,
                    id,
                )
            )
        return rents

    # TODO  verifiy these selects on rents! WRONG VALUES!
    def select_all_finished_rents(self):
        self.cursor.execute("SELECT * FROM rent WHERE is_returned = 1")
        query_result = self.cursor.fetchall()
        rents = []
        for query in query_result:
            [
                id,
                vehicle_plate,
                client_cpf,
                employee_cpf,
                start_date,
                end_date,
                value,
                payment_id,
                insurance_id,
                is_returned,
            ] = query
            rents.append(
                rent.Rent(
                    vehicle_plate,
                    client_cpf,
                    employee_cpf,
                    datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S"),
                    datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S"),
                    value,
                    payment_id,
                    insurance_id,
                    is_returned,
                    id,
                )
            )
        return rents

    def select_all_ongoing_rents(self):
        self.cursor.execute(
            "SELECT * FROM rent WHERE end_date > CURRENT_DATE AND is_returned = 0"
        )
        query_result = self.cursor.fetchall()
        rents = []
        for query in query_result:
            [
                id,
                vehicle_plate,
                client_cpf,
                employee_cpf,
                start_date,
                end_date,
                value,
                payment_id,
                insurance_id,
                is_returned,
            ] = query
            rents.append(
                rent.Rent(
                    vehicle_plate,
                    client_cpf,
                    employee_cpf,
                    datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S"),
                    datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S"),
                    value,
                    payment_id,
                    insurance_id,
                    is_returned,
                    id,
                )
            )
        return rents

    def select_all_expired_rents(self):
        self.cursor.execute(
            "SELECT * FROM rent WHERE end_date < CURRENT_DATE AND is_returned = 0"
        )
        query_result = self.cursor.fetchall()
        rents = []
        for query in query_result:
            [
                id,
                vehicle_plate,
                client_cpf,
                employee_cpf,
                start_date,
                end_date,
                value,
                payment_id,
                insurance_id,
                is_returned,
            ] = query
            rents.append(
                rent.Rent(
                    vehicle_plate,
                    client_cpf,
                    employee_cpf,
                    datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S"),
                    datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S"),
                    value,
                    payment_id,
                    insurance_id,
                    is_returned,
                    id,
                )
            )
        return rents

    def select_monthly_rents(self, date: datetime):
        year = date.year
        month = date.month
        next_year = year + 1 if month == 12 else year
        next_month = month + 1 if next_year else 1
        self.cursor.execute(
            f"SELECT * FROM rent WHERE end_date >= {year}-{month}-01 AND end_date < {next_year}-{next_month}-01 AND is_returned = 0"
        )
        query_result = self.cursor.fetchall()
        rents = []
        for query in query_result:
            [
                id,
                vehicle_plate,
                client_cpf,
                employee_cpf,
                start_date,
                end_date,
                value,
                payment_id,
                insurance_id,
                is_returned,
            ] = query
            rents.append(
                rent.Rent(
                    vehicle_plate,
                    client_cpf,
                    employee_cpf,
                    datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S"),
                    datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S"),
                    value,
                    payment_id,
                    insurance_id,
                    is_returned,
                    id,
                )
            )
        return rents

    def select_all_employees(self):
        self.cursor.execute(
            f"SELECT cpf, rg, name, birth_date, address, zip_code, email, active FROM user WHERE role = 'employee'"
        )
        query_result = self.cursor.fetchall()
        employees = []
        for employee in query_result:
            [cpf, rg, name, birth_date, address, zip_code, email, active] = employee
            if active:
                self.cursor.execute(
                    f"SELECT salary, pis, admission_date FROM employee WHERE cpf = '{cpf}'"
                )
                query_result_2 = self.cursor.fetchone()
                [salary, pis, admission_date] = query_result_2
                employees.append(
                    user.Employee(
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
                )
        return employees

    def select_all_insurances(self):
        self.cursor.execute("SELECT * FROM insurance")
        query_result = self.cursor.fetchall()
        insurances = []
        for query in query_result:
            [
                id,
                name,
                model,
                description,
                value,
            ] = query
            insurances.append(insurance.Insurance(name, model, description, value, id))
        return insurances

    def select_all_clients(self):
        self.cursor.execute(
            f"SELECT cpf, rg, name, birth_date, address, zip_code, email, active FROM user WHERE role = 'client'"
        )
        query_result = self.cursor.fetchall()
        clients = []
        for client in query_result:
            [cpf, rg, name, birth_date, address, zip_code, email, active] = client
            if active:
                self.cursor.execute(
                    f"SELECT permission_category, permission_number, permission_expiration, is_golden_client FROM client WHERE cpf = '{cpf}'"
                )
                query_result_2 = self.cursor.fetchone()
                [
                    permission_category,
                    permission_number,
                    permission_expiration,
                    is_golden_client,
                ] = query_result_2
                clients.append(
                    user.Client(
                        cpf,
                        rg,
                        name,
                        birth_date,
                        address,
                        zip_code,
                        email,
                        permission_category,
                        permission_number,
                        permission_expiration,
                        is_golden_client,
                    )
                )
        return clients

    def select_all_payments(self):
        self.cursor.execute("SELECT * FROM payment")
        return self.cursor.fetchall()

    def select_client(self, cpf: str):
        self.cursor.execute(
            f"SELECT * FROM user JOIN client ON user.cpf = client.cpf WHERE user.cpf = '{cpf}'"
        )
        query_execution = self.cursor.fetchone()
        if query_execution is None:
            return None
        # else...
        [
            cpf,
            _,
            rg,
            name,
            birth_date,
            address,
            zip_code,
            email,
            active,
            _,
            permission_category,
            permission_number,
            permission_expiration_date,
            is_golden_client,
        ] = query_execution
        if active:
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

        return None

    def select_employee(self, cpf: str):
        self.cursor.execute(
            f"SELECT * FROM user JOIN employee ON user.cpf = employee.cpf WHERE user.cpf = '{cpf}'"
        )
        query_execution = self.cursor.fetchone()
        if query_execution is None:
            return None
        # else...
        [
            cpf,
            rg,
            name,
            birth_date,
            address,
            zip_code,
            email,
            _,
            salary,
            pis,
            admission_date,
        ] = query_execution
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

    def select_national_vehicle(self, plate: str):
        self.cursor.execute(
            f"SELECT * FROM vehicle JOIN national_vehicle ON vehicle.plate = national_vehicle.plate WHERE vehicle.plate = '{plate}'"
        )
        query_execution = self.cursor.fetchone()
        if query_execution is None:
            return None
        # else...
        [
            plate,
            model,
            manufacturer,
            fabrication_year,
            model_year,
            category,
            fipe_value,
            rent_value,
            is_available,
            _,
            state_taxes,
        ] = query_execution
        return vehicle.National(
            plate,
            model,
            manufacturer,
            fabrication_year,
            model_year,
            category,
            fipe_value,
            rent_value,
            is_available,
            state_taxes,
        )

    def select_all_imported_vehicles(self):
        self.cursor.execute(
            f"SELECT * FROM vehicle JOIN imported_vehicle ON vehicle.plate = imported_vehicle.plate"
        )
        query_execution = self.cursor.fetchall()
        if query_execution is None:
            return None
        # else...
        vehicles = []
        for v in query_execution:
            [
                plate,
                _,
                model,
                manufacturer,
                fabrication_year,
                model_year,
                category,
                fipe_value,
                rent_value,
                is_available,
                active,
                _,  # join
                state_taxes,
                federal_taxes,
            ] = v
            if active:
                vehicles.append(
                    vehicle.Imported(
                        plate,
                        model,
                        manufacturer,
                        fabrication_year,
                        model_year,
                        category,
                        fipe_value,
                        rent_value,
                        is_available,
                        state_taxes,
                        federal_taxes,
                    )
                )
        return vehicles

    def select_all_national_vehicles(self):
        self.cursor.execute(
            f"SELECT * FROM vehicle JOIN national_vehicle ON vehicle.plate = national_vehicle.plate"
        )
        query_execution = self.cursor.fetchall()
        if query_execution is None:
            return None
        # else...
        vehicles = []
        for v in query_execution:
            [
                plate,
                _,
                model,
                manufacturer,
                fabrication_year,
                model_year,
                category,
                fipe_value,
                rent_value,
                is_available,
                active,
                _,  # join
                state_taxes,
            ] = v
            if active:
                vehicles.append(
                    vehicle.National(
                        plate,
                        model,
                        manufacturer,
                        fabrication_year,
                        model_year,
                        category,
                        fipe_value,
                        rent_value,
                        is_available,
                        state_taxes,
                    )
                )
        return vehicles

    def select_available_vehicles(self):
        self.cursor.execute(f"SELECT * FROM vehicle WHERE is_available = 1")
        query_execution = self.cursor.fetchall()
        if query_execution is None:
            return None
        # else...
        vehicles = []
        for v in query_execution:
            [
                plate,
                origin,
                model,
                manufacturer,
                fabrication_year,
                model_year,
                category,
                fipe_value,
                rent_value,
                is_available,
                active,
            ] = v
            if active:
                if origin == "imported":
                    self.cursor.execute(
                        f"SELECT state_taxes, federal_taxes FROM imported_vehicle WHERE plate = '{plate}'"
                    )
                    query_execution = self.cursor.fetchone()
                    if query_execution is None:
                        return None
                    # else...
                    [state_taxes, federal_taxes] = query_execution
                    vehicles.append(
                        vehicle.Imported(
                            plate,
                            model,
                            manufacturer,
                            fabrication_year,
                            model_year,
                            category,
                            fipe_value,
                            rent_value,
                            is_available,
                            state_taxes,
                            federal_taxes,
                        )
                    )
                else:
                    self.cursor.execute(
                        f"SELECT state_taxes FROM national_vehicle WHERE plate = '{plate}'"
                    )
                    query_execution = self.cursor.fetchone()
                    if query_execution is None:
                        return None
                    # else...
                    [state_taxes] = query_execution
                    vehicles.append(
                        vehicle.National(
                            plate,
                            model,
                            manufacturer,
                            fabrication_year,
                            model_year,
                            category,
                            fipe_value,
                            rent_value,
                            is_available,
                            state_taxes,
                        )
                    )
        return vehicles

    def select_rented_vehicles(self):
        self.cursor.execute(f"SELECT * FROM vehicle WHERE is_available = 0")
        query_execution = self.cursor.fetchall()
        if query_execution is None:
            return None
        # else...
        vehicles = []
        for v in query_execution:
            [
                plate,
                origin,
                model,
                manufacturer,
                fabrication_year,
                model_year,
                category,
                fipe_value,
                rent_value,
                is_available,
            ] = v
            if origin == "imported":
                self.cursor.execute(
                    f"SELECT state_taxes, federal_taxes FROM imported_vehicle WHERE plate = '{plate}'"
                )
                query_execution = self.cursor.fetchone()
                if query_execution is None:
                    return None
                # else...
                [state_taxes, federal_taxes] = query_execution
                vehicles.append(
                    vehicle.Imported(
                        plate,
                        model,
                        manufacturer,
                        fabrication_year,
                        model_year,
                        category,
                        fipe_value,
                        rent_value,
                        is_available,
                        state_taxes,
                        federal_taxes,
                    )
                )
            else:
                self.cursor.execute(
                    f"SELECT state_taxes FROM national_vehicle WHERE plate = '{plate}'"
                )
                query_execution = self.cursor.fetchone()
                if query_execution is None:
                    return None
                # else...
                [state_taxes] = query_execution
                vehicles.append(
                    vehicle.National(
                        plate,
                        model,
                        manufacturer,
                        fabrication_year,
                        model_year,
                        category,
                        fipe_value,
                        rent_value,
                        is_available,
                        state_taxes,
                    )
                )
        return vehicles

    def select_not_returned_vehicles(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            f"SELECT * FROM vehicle JOIN rent ON rent.vehicle = vehicle.plate WHERE rent.is_returned = 0 AND rent.end_date < '{current_date}'"
        )
        query_execution = self.cursor.fetchall()
        if query_execution is None:
            return None
        # else...
        rents = []
        for v in query_execution:
            [
                plate,
                origin,
                model,
                manufacturer,
                fabrication_year,
                model_year,
                category,
                fipe_value,
                rent_value,
                is_available,
                active,
                _,
                _,
                _,
                _,
                _,
                _,
                _,
                _,
                _,
                _,
            ] = v
            if active:
                if origin == "imported":
                    self.cursor.execute(
                        f"SELECT state_taxes, federal_taxes FROM imported_vehicle WHERE plate = '{plate}'"
                    )
                    query_execution = self.cursor.fetchone()
                    [state_taxes, federal_taxes] = query_execution
                    rents.append(
                        vehicle.Imported(
                            plate,
                            model,
                            manufacturer,
                            fabrication_year,
                            model_year,
                            category,
                            fipe_value,
                            rent_value,
                            is_available,
                            state_taxes,
                            federal_taxes,
                        )
                    )
                    rents.append(
                        vehicle.Imported(
                            plate,
                            model,
                            manufacturer,
                            fabrication_year,
                            model_year,
                            category,
                            fipe_value,
                            rent_value,
                            is_available,
                            state_taxes,
                            federal_taxes,
                        )
                    )
                else:
                    self.cursor.execute(
                        f"SELECT state_taxes FROM national_vehicle WHERE plate = '{plate}'"
                    )
                    query_execution = self.cursor.fetchone()
                    [state_taxes] = query_execution
                    rents.append(
                        vehicle.National(
                            plate,
                            model,
                            manufacturer,
                            fabrication_year,
                            model_year,
                            category,
                            fipe_value,
                            rent_value,
                            is_available,
                            state_taxes,
                        )
                    )
        return rents

    def select_imported_vehicle(self, plate: str):
        self.cursor.execute(
            f"SELECT * FROM vehicle JOIN imported_vehicle ON vehicle.plate = imported_vehicle.plate WHERE vehicle.plate = '{plate}'"
        )
        query_execution = self.cursor.fetchone()
        if query_execution is None:
            return None
        # else...
        [
            plate,
            model,
            manufacturer,
            fabrication_year,
            model_year,
            category,
            fipe_value,
            rent_value,
            is_available,
            _,
            state_taxes,
            federal_taxes,
        ] = query_execution
        return vehicle.Imported(
            plate,
            model,
            manufacturer,
            fabrication_year,
            model_year,
            category,
            fipe_value,
            rent_value,
            is_available,
            state_taxes,
            federal_taxes,
        )

    def return_vehicle(self, rent_id: int):
        self.cursor.execute(f"UPDATE rent SET is_returned = '1' WHERE id = '{rent_id}'")
        self.cursor.execute(
            f"UPDATE vehicle SET is_available = '1' WHERE plate = (SELECT vehicle FROM rent WHERE rent.id = {rent_id} LIMIT 1)"
        )
        self.connection.commit()
