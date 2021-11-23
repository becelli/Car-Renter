import sqlite3 as sql

cars = sql.connect("./db/example_db.db")
cur = cars.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS cars(
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            year INTEGER NOT NULL,
            color TEXT NOT NULL
            )"""
)

cur.execute(
    "INSERT INTO cars(name, price, year, color) VALUES (?, ?, ?, ?)",
    ("Qwid", "34000", 2018, "black"),
)

cur.execute(
    "INSERT INTO cars(name, price, year, color) VALUES (?, ?, ?, ?)",
    ("HB20", "42570", 2020, "red"),
)

cars.commit()

cur.execute("SELECT * FROM cars WHERE color = 'red'")
print(cur.fetchall())
