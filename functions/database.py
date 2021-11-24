# Init database
import sqlite3 as sql3
import sys

# sys.path.append("..")
import classes.user as user
import classes.vehicle as vehicle
import functions.random as rand


sql = sql3.connect("./db/application.db")
cursor = sql.cursor()


def init():
    if verify_if_table_exists("user") is False:
        create_user_table()

    if verify_if_table_exists("vehicle") is False:
        create_vehicle_table()


def create_vehicle_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS vehicle (
        id INTEGER PRIMARY KEY, 
        model TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        fabrication_year INTEGER NOT NULL,
        model_year INT NOT NULL,
        plate CHAR(7) NOT NULL UNIQUE,
        category TEXT NOT NULL CHECK (category IN ('car', 'motorcycle', 'truck', 'bus', 'van', 'bicycle')),
        fipe_value REAL NOT NULL CHECK (fipe_value > 0) DEFAULT 5000.00,
        rent_value REAL NOT NULL CHECK (rent_value > 0) DEFAULT 100.00,
        is_available BOOL NOT NULL DEFAULT TRUE,
        state_taxes REAL NOT NULL CHECK (state_taxes >= 0) DEFAULT 0.00,
        federal_taxes REAL CHECK (federal_taxes >= 0) DEFAULT 0.00
        )"""
    )


def create_user_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        cpf CHAR(11) NOT NULL UNIQUE,
        rg CHAR(9) NOT NULL UNIQUE,
        birth_date DATE NOT NULL,
        address TEXT NOT NULL,
        zip_code CHAR(8) NOT NULL,
        email TEXT NOT NULL UNIQUE,
        permission_category CHAR(1) CHECK (permission_category IN ('A', 'B', 'C', 'D', 'E')),
        permission_number CHAR(10) UNIQUE,
        permission_expiration DATE,
        is_golden_client BOOL DEFAULT FALSE,
        salary REAL CHECK (salary >= 0) DEFAULT 0.00,
        pis CHAR(11) UNIQUE,
        admission_date DATE
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
