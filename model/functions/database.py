# Init database
import sqlite3 as sql3
import model.classes.user as user
import model.classes.vehicle as vehicle
import model.functions.random as rand


sql = sql3.connect("./model/database/app.db")
cursor = sql.cursor()


def init():
    cursor.execute("PRAGMA foreign_keys = ON;").fetchone()
    if verify_if_table_exists("client") is False:
        create_client_table()

    if verify_if_table_exists("employee") is False:
        create_employee_table()

    if verify_if_table_exists("national_vehicle") is False:
        create_national_vehicle_table()

    if verify_if_table_exists("imported_vehicle") is False:
        create_imported_vehicle_table()

    if verify_if_table_exists("rent") is False:
        create_rent_table()

    if verify_if_table_exists("cash") is False:
        create_cash_table()

    if verify_if_table_exists("card") is False:
        create_card_table()

    if verify_if_table_exists("insurance") is False:
        create_insurance_table()


def create_client_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS client (
        cpf CHAR(11) PRIMARY KEY,
        name TEXT NOT NULL,
        rg CHAR(9) NOT NULL UNIQUE,
        birth_date DATE NOT NULL,
        address TEXT NOT NULL,
        zip_code CHAR(8) NOT NULL,
        email TEXT NOT NULL UNIQUE,
        permission_category CHAR(1) CHECK (permission_category IN ('A', 'B', 'C', 'D', 'E')),
        permission_number CHAR(10) UNIQUE,
        permission_expiration DATE,
        is_golden_client BOOL DEFAULT FALSE
        )"""
    )


def create_employee_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS employee (
        name TEXT NOT NULL,
        cpf CHAR(11) NOT NULL UNIQUE PRIMARY KEY,
        rg CHAR(9) NOT NULL UNIQUE,
        birth_date DATE NOT NULL,
        address TEXT NOT NULL,
        zip_code CHAR(8) NOT NULL,
        email TEXT NOT NULL UNIQUE,
        salary REAL CHECK (salary >= 0) DEFAULT 0.00,
        pis CHAR(11) UNIQUE,
        admission_date DATE
        )"""
    )


def create_national_vehicle_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS national_vehicle (
        plate CHAR(7) PRIMARY KEY,
        model TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        fabrication_year INTEGER NOT NULL,
        model_year INT NOT NULL,
        category TEXT NOT NULL CHECK (category IN ('car', 'motorcycle', 'truck', 'bus', 'van', 'bicycle')),
        fipe_value REAL NOT NULL CHECK (fipe_value > 0) DEFAULT 5000.00,
        rent_value REAL NOT NULL CHECK (rent_value > 0) DEFAULT 100.00,
        is_available BOOL NOT NULL DEFAULT TRUE,
        state_taxes REAL NOT NULL CHECK (state_taxes >= 0) DEFAULT 0.00
        )"""
    )


def create_imported_vehicle_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS imported_vehicle (
        plate CHAR(7) PRIMARY KEY,
        model TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        fabrication_year INTEGER NOT NULL,
        model_year INT NOT NULL,
        category TEXT NOT NULL CHECK (category IN ('car', 'motorcycle', 'truck', 'bus', 'van', 'bicycle')),
        fipe_value REAL NOT NULL CHECK (fipe_value > 0) DEFAULT 5000.00,
        rent_value REAL NOT NULL CHECK (rent_value > 0) DEFAULT 100.00,
        is_available BOOL NOT NULL DEFAULT TRUE,
        state_taxes REAL NOT NULL CHECK (state_taxes >= 0) DEFAULT 0.00,
        federal_taxes REAL CHECK (federal_taxes >= 0) DEFAULT 0.00
        )"""
    )


def create_rent_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS rent (
        id INTEGER PRIMARY KEY,

        vehicle CHAR(7) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        value REAL NOT NULL CHECK (total_value >= 0) DEFAULT 0.00,
        FOREIGN KEY payment_id REFERENCES payment(id),
        insurance INTEGER NOT NULL CHECK (insurance >= 0) DEFAULT 0.00,
        is_returned BOOL NOT NULL DEFAULT TRUE,
        employee CHAR(11) NOT NULL,
        FOREIGN KEY (employee) REFERENCES employee (cpf)
        client CHAR(11) NOT NULL,
        FOREIGN KEY (client) REFERENCES client (cpf)
        )"""
    )


def create_cash_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS cash (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        )"""
    )


def create_card_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS card (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        card_holder TEXT,
        card_number CHAR(16),
        card_flag TEXT,
        )"""
    )


def create_insurance_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS insurance (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        model TEXT NOT NULL,
        description TEXT NOT NULL,
        value REAL NOT NULL CHECK (value >= 0) DEFAULT 0.00,
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


# SELECTS #
def select_all_users():
    cursor.execute("SELECT * FROM user")
    return cursor.fetchall()


def select_all_cars():
    cursor.execute("SELECT * FROM vehicle")
    return cursor.fetchall()


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
def insert_user(object):
    if isinstance(object, user.Client):
        return insert_client(object)
    elif isinstance(object, user.Employee):
        return insert_employee(object)
    else:
        raise TypeError("Invalid user type")


def insert_employee(employee: user.Employee):
    cursor.execute(
        "INSERT INTO user (name, cpf, rg, birth_date, address, zip_code, email, salary, pis, admission_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            employee.get_name(),
            employee.get_cpf(),
            employee.get_rg(),
            employee.get_birth_date(),
            employee.get_address(),
            employee.get_zip_code(),
            employee.get_email(),
            employee.get_salary(),
            employee.get_pis(),
            employee.get_admission_date(),
        ),
    )
    sql.commit()
    return True


def insert_client(client: user.Client):
    cursor.execute(
        "INSERT INTO user (name, cpf, rg, birth_date, address, zip_code, email, permission_category, permission_number, permission_expiration, is_golden_client) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (
            client.get_name(),
            client.get_cpf(),
            client.get_rg(),
            client.get_birth_date(),
            client.get_address(),
            client.get_zip_code(),
            client.get_email(),
            client.get_permission_category(),
            client.get_permission_number(),
            client.get_permission_expiration(),
            client.get_is_golden_client(),
        ),
    )
    sql.commit()
    return True


def insert_vehicle(object):
    if isinstance(object, vehicle.National):
        return insert_national(object)
    elif isinstance(object, vehicle.International):
        return insert_international(object)
    else:
        raise TypeError("Invalid user type")


def insert_national(vehicle: vehicle.National):
    cursor.execute(
        "INSERT INTO vehicle (model, manufacturer, fabrication_year, model_year, plate, category, fipe_value, rent_value, state_taxes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            vehicle.get_model(),
            vehicle.get_manufacturer(),
            vehicle.get_fabrication_year(),
            vehicle.get_model_year(),
            vehicle.get_plate(),
            vehicle.get_category(),
            vehicle.get_fipe_value(),
            vehicle.get_rent_value(),
            vehicle.get_state_taxes(),
        ),
    )
    sql.commit()
    return True


def insert_international(vehicle: vehicle.International):
    cursor.execute(
        "INSERT INTO vehicle (model, manufacturer, fabrication_year, model_year, plate, category, fipe_value, rent_value, state_taxes, federal_taxes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            vehicle.get_model(),
            vehicle.get_manufacturer(),
            vehicle.get_fabrication_year(),
            vehicle.get_model_year(),
            vehicle.get_plate(),
            vehicle.get_category(),
            vehicle.get_fipe_value(),
            vehicle.get_rent_value(),
            vehicle.get_state_taxes(),
            vehicle.get_federal_taxes(),
        ),
    )
    sql.commit()
    return True


def select_client(id: int):
    cursor.execute(f"SELECT * FROM user WHERE id = {id}")
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
    ] = cursor.fetchone()
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


def select_employee(id: int):
    cursor.execute(f"SELECT * FROM user WHERE id = {id}")
    [
        name,
        cpf,
        rg,
        birth_date,
        address,
        zip_code,
        email,
        _,
        _,
        _,
        _,
        salary,
        pis,
        admission_date,
    ] = cursor.fetchone()
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
