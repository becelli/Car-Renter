# Init database
from datetime import datetime
import sqlite3 as sql3
import model.classes.user as user
import model.classes.vehicle as vehicle
from model.classes import user, vehicle, payment, rent, insurance
import model.functions.random as rand


sql = sql3.connect("./model/database/app.db")
cursor = sql.cursor()


def init():
    cursor.execute("PRAGMA foreign_keys = ON;").fetchone()
    if verify_if_table_exists("user") is False:
        create_user_table()

    if verify_if_table_exists("client") is False:
        create_client_table()

    if verify_if_table_exists("employee") is False:
        create_employee_table()

    if verify_if_table_exists("vehicle") is False:
        create_vehicle_table()

    if verify_if_table_exists("national_vehicle") is False:
        create_national_vehicle_table()

    if verify_if_table_exists("imported_vehicle") is False:
        create_imported_vehicle_table()

    if verify_if_table_exists("rent") is False:
        create_rent_table()

    if verify_if_table_exists("payment") is False:
        create_payment_table()

    if verify_if_table_exists("payment_cash") is False:
        create_payment_cash_table()

    if verify_if_table_exists("payment_card") is False:
        create_payment_card_table()

    if verify_if_table_exists("insurance") is False:
        create_insurance_table()


def create_user_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS user (
        cpf CHAR(11) PRIMARY KEY,
        role TEXT NOT NULL CHECK (role IN ('client', 'employee')),
        rg CHAR(9) NOT NULL UNIQUE,
        name TEXT NOT NULL,
        birth_date DATE NOT NULL,
        address TEXT NOT NULL,
        zip_code CHAR(8) NOT NULL,
        email TEXT NOT NULL UNIQUE
        )"""
    )


def create_client_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS client (
        cpf CHAR(11) PRIMARY KEY,
        permission_category CHAR(1) CHECK (permission_category IN ('A', 'B', 'C', 'D', 'E')),
        permission_number CHAR(10) UNIQUE,
        permission_expiration DATE,
        is_golden_client BOOL DEFAULT FALSE,
        FOREIGN KEY (cpf) REFERENCES user (cpf)
        )"""
    )


def create_employee_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS employee (
        cpf CHAR(11) PRIMARY KEY,
        salary REAL CHECK (salary >= 0) DEFAULT 0.00,
        pis CHAR(11) UNIQUE,
        admission_date DATE,
        FOREIGN KEY (cpf) REFERENCES user (cpf)
        )"""
    )


def create_vehicle_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS vehicle (
        plate CHAR(8) PRIMARY KEY,
        origin TEXT NOT NULL,
        model TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        fabrication_year INTEGER NOT NULL,
        model_year INT NOT NULL,
        category TEXT NOT NULL CHECK (category IN ('car', 'motorcycle', 'truck', 'bus', 'van', 'bicycle')),
        fipe_value REAL NOT NULL CHECK (fipe_value > 0) DEFAULT 5000.00,
        rent_value REAL NOT NULL CHECK (rent_value > 0) DEFAULT 100.00,
        is_available BOOL NOT NULL DEFAULT TRUE
        )"""
    )


def create_national_vehicle_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS national_vehicle (
        plate CHAR(8) PRIMARY KEY,
        state_taxes REAL NOT NULL CHECK (state_taxes >= 0) DEFAULT 0.00,
        FOREIGN KEY (plate) REFERENCES vehicle (plate)
        )"""
    )


def create_imported_vehicle_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS imported_vehicle (
        plate CHAR(8) PRIMARY KEY,
        state_taxes REAL NOT NULL CHECK (state_taxes >= 0) DEFAULT 0.00,
        federal_taxes REAL NOT NULL CHECK (federal_taxes >= 0) DEFAULT 0.00,
        FOREIGN KEY (plate) REFERENCES vehicle (plate)
        )"""
    )


def create_rent_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS rent (
        id INTEGER PRIMARY KEY,
        vehicle CHAR(8) NOT NULL,
        client CHAR(11) NOT NULL,
        employee CHAR(11) NOT NULL,
        payment_id INTEGER,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        value REAL NOT NULL CHECK (value >= 0) DEFAULT 0.00,
        insurance INTEGER NOT NULL CHECK (insurance >= 0) DEFAULT 0.00,
        is_returned BOOL NOT NULL DEFAULT TRUE,
        FOREIGN KEY (vehicle) REFERENCES vehicle (plate),
        FOREIGN KEY (client) REFERENCES client (cpf),
        FOREIGN KEY (employee) REFERENCES employee (cpf),
        FOREIGN KEY (payment_id) REFERENCES payment (id) ON DELETE CASCADE
        )"""
    )


def create_payment_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS payment (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
        )"""
    )


def create_payment_cash_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS cash (
        id INTEGER PRIMARY KEY,
        FOREIGN KEY (id) REFERENCES payment (id)
        )"""
    )


def create_payment_card_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS card (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        card_holder TEXT,
        card_number CHAR(16),
        card_flag TEXT,
        FOREIGN KEY (id) REFERENCES payment (id)
        )"""
    )


def create_insurance_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS insurance (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        model TEXT NOT NULL,
        description TEXT NOT NULL,
        value REAL NOT NULL CHECK (value >= 0) DEFAULT 0.00
        )"""
    )


def verify_if_table_exists(table_name: str):
    cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    )
    return cursor.fetchone() is not None


def populate_user(quantity: int = 10):
    for _i in range(quantity):
        u = rand.user()
        u.save()


def populate_vehicle(quantity: int = 10):
    for _i in range(quantity):
        v = rand.vehicle()
        v.save()


def populate_rent(quantity: int = 10):
    for _i in range(quantity):
        r = rand.rent()
        r.save()


def populate_payment(quantity: int = 10):
    for _i in range(quantity):
        p = rand.payment()
        p.save()


def populate_insurance(quantity: int = 10):
    for _i in range(quantity):
        i = rand.insurance()
        i.save()


# DROPS #
def drop_table(table_name: str):
    cursor.execute(f"DROP TABLE {table_name}")
    sql.commit()
    return True


# DELETES #
def delete_users_by(property: str, value: str, limit: int = 0):
    limits = f"LIMIT {limit}" if limit > 0 else ""
    sql_query = f"DELETE FROM user WHERE {property} = '{value}' {limit}"
    cursor.execute(sql_query)
    sql.commit()
    return True


# INSERTS #
# USER #
def insert_user(user_object: user.User):
    cursor.execute(
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
        insert_client(user_object)
    elif isinstance(user_object, user.Employee):
        insert_employee(user_object)
    sql.commit()


def insert_employee(employee: user.Employee):
    cursor.execute(
        "INSERT INTO employee (cpf, salary, pis, admission_date) VALUES (?, ?, ?, ?)",
        (
            employee.get_cpf(),
            employee.get_salary(),
            employee.get_pis(),
            employee.get_admission_date(),
        ),
    )


def insert_client(client: user.Client):
    cursor.execute(
        "INSERT INTO client (cpf, permission_category, permission_number, permission_expiration, is_golden_client) VALUES (?,?,?,?, ?)",
        (
            client.get_cpf(),
            client.get_permission_category(),
            client.get_permission_number(),
            client.get_permission_expiration(),
            client.get_is_golden_client(),
        ),
    )


# VEHICLE #
def insert_vehicle(vehicle_object: vehicle.Vehicle):
    cursor.execute(
        "INSERT INTO vehicle (model, origin, manufacturer, fabrication_year, model_year, plate, category, fipe_value, rent_value) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            vehicle_object.get_model(),
            "national" if isinstance(vehicle_object, vehicle.National) else "imported",
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
        insert_national(vehicle_object)
    elif isinstance(vehicle_object, vehicle.Imported):
        insert_imported(vehicle_object)
    sql.commit()


def insert_national(vehicle_object: vehicle.National):
    cursor.execute(
        """INSERT INTO national_vehicle (plate, state_taxes) VALUES (?,?)""",
        (
            vehicle_object.get_plate(),
            vehicle_object.get_state_taxes(),
        ),
    )


def insert_imported(vehicle_object: vehicle.Imported):
    cursor.execute(
        "INSERT INTO imported_vehicle (plate, state_taxes, federal_taxes) VALUES (?, ?, ?)",
        (
            vehicle_object.get_plate()[0:8],
            vehicle_object.get_state_taxes(),
            vehicle_object.get_federal_taxes(),
        ),
    )


# PAYMENT #
def insert_payment(payment_object: payment.Payment):
    cursor.execute(
        "INSERT INTO payment (name) VALUES (?)",
        (payment_object.get_name(),),
    )
    if isinstance(payment_object, payment.Cash):
        insert_cash(payment_object)
    elif isinstance(payment_object, payment.Card):
        insert_card(payment_object)
    sql.commit()


def insert_cash(payment_object: payment.Cash):
    cursor.execute(
        "INSERT INTO cash (id) VALUES (?)",
        (payment_object.get_id(),),
    )


def insert_card(payment_object: payment.Card):
    cursor.execute(
        "INSERT INTO card (id, name, card_holder, card_number, card_flag) VALUES (?, ?, ?, ?, ?)",
        (
            payment_object.get_id(),
            payment_object.get_name(),
            payment_object.get_card_holder(),
            payment_object.get_card_number(),
            payment_object.get_card_flag(),
        ),
    )


# INSURANCE #
def insert_insurance(insurance_object: insurance.Insurance):
    cursor.execute(
        "INSERT INTO insurance (name, model, description, value) VALUES (?, ?, ?, ?)",
        (
            insurance_object.get_name(),
            insurance_object.get_model(),
            insurance_object.get_description(),
            insurance_object.get_value(),
        ),
    )
    sql.commit()


# RENT #
def insert_rent(rent_object: rent.Rent):
    cursor.execute(
        "INSERT INTO rent (id, client_cpf, vehicle_plate, start_date, end_date, payment_id, insurance_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            rent_object.get_id(),
            rent_object.get_client_cpf(),
            rent_object.get_vehicle_plate(),
            rent_object.get_start_date(),
            rent_object.get_end_date(),
            rent_object.get_payment_id(),
            rent_object.get_insurance_id(),
        ),
    )
    sql.commit()


# SELECTS #
def select_all_users():
    cursor.execute("SELECT * FROM user")
    query_result = cursor.fetchall()
    users = []
    for user in query_result:
        [cpf, role, rg, name, birth_date, address, zip_code, email] = user
        if role == "client":
            cursor.execute(f"SELECT * FROM {role} WHERE cpf = {cpf}")
            query_result = cursor.fetchone()
            [
                permission_category,
                permission_number,
                permission_expiration,
                is_golden_client,
            ] = query_result
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
            cursor.execute(f"SELECT * FROM {role} WHERE cpf = {cpf}")
            query_result = cursor.fetchone()
            [
                salary,
                pis,
                admission_date,
            ] = query_result
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


def select_all_vehicles():
    cursor.execute("SELECT * FROM vehicle")
    query_result = cursor.fetchall()
    vehicles = []
    for vehicle in query_result:
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
        ] = vehicle
        # print(vehicle)
        if origin == "national":
            cursor.execute(f"SELECT * FROM {origin}_vehicle WHERE plate = {plate}")
            query_result = cursor.fetchone()
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
        elif origin == "imported":
            cursor.execute(
                f"SELECT state_taxes, federal_taxes FROM imported_vehicle WHERE plate = {plate};"
            )
            query_result = cursor.fetchone()
            [
                state_taxes,
                federal_taxes,
            ] = query_result
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


def select_all_payments():
    cursor.execute("SELECT * FROM payment")
    return cursor.fetchall()


def select_client(cpf: str):
    cursor.execute(
        f"SELECT * FROM user JOIN client ON user.cpf = client.cpf WHERE user.cpf = '{cpf}'"
    )
    query_execution = cursor.fetchone()
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
        permission_category,
        permission_number,
        permission_expiration_date,
        is_golden_client,
    ] = query_execution
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


def select_employee(cpf: str):
    cursor.execute(
        f"SELECT * FROM user JOIN employee ON user.cpf = employee.cpf WHERE user.cpf = '{cpf}'"
    )
    query_execution = cursor.fetchone()
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


def select_national_vehicle(plate: str):
    cursor.execute(
        f"SELECT * FROM vehicle JOIN national_vehicle ON vehicle.plate = national_vehicle.plate WHERE vehicle.plate = '{plate}'"
    )
    query_execution = cursor.fetchone()
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


def select_all_imported_vehicles():
    cursor.execute(
        f"SELECT * FROM vehicle JOIN imported_vehicle ON vehicle.plate = imported_vehicle.plate"
    )
    query_execution = cursor.fetchall()
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
            _,  # join
            state_taxes,
            federal_taxes,
        ] = v
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


def select_all_national_vehicles():
    cursor.execute(
        f"SELECT * FROM vehicle JOIN national_vehicle ON vehicle.plate = national_vehicle.plate"
    )
    query_execution = cursor.fetchall()
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
            _,  # join
            state_taxes,
        ] = v
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


def select_available_vehicles():
    cursor.execute(f"SELECT * FROM vehicle WHERE is_available = 1")
    query_execution = cursor.fetchall()
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
            cursor.execute(
                f"SELECT state_taxes, federal_taxes FROM imported_vehicle WHERE plate = '{plate}'"
            )
            query_execution = cursor.fetchone()
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
            cursor.execute(
                f"SELECT state_taxes FROM national_vehicle WHERE plate = '{plate}'"
            )
            query_execution = cursor.fetchone()
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


def select_rented_vehicles():
    cursor.execute(f"SELECT * FROM vehicle WHERE is_available = 0")
    query_execution = cursor.fetchall()
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
            cursor.execute(
                f"SELECT state_taxes, federal_taxes FROM imported_vehicle WHERE plate = '{plate}'"
            )
            query_execution = cursor.fetchone()
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
            cursor.execute(
                f"SELECT state_taxes FROM national_vehicle WHERE plate = '{plate}'"
            )
            query_execution = cursor.fetchone()
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


def select_not_returned_vehicles():
    current_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        f"SELECT * FROM vehicle JOIN rent ON rent.vehicle = vehicle.plate WHERE {current_date} > rent.end_date"
    )
    query_execution = cursor.fetchall()
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
        ] = v
        if origin == "imported":
            cursor.execute(
                f"SELECT state_taxes, federal_taxes FROM imported_vehicle WHERE plate = '{plate}'"
            )
            query_execution = cursor.fetchone()
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
            cursor.execute(
                f"SELECT state_taxes FROM national_vehicle WHERE plate = '{plate}'"
            )
            query_execution = cursor.fetchone()
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


def select_imported_vehicle(plate: str):
    cursor.execute(
        f"SELECT * FROM vehicle JOIN imported_vehicle ON vehicle.plate = imported_vehicle.plate WHERE vehicle.plate = '{plate}'"
    )
    query_execution = cursor.fetchone()
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


def select_all(table_name: str):
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()
