# Init database
import sqlite3 as sql3
from time import sleep

sql = sql3.connect("./model/database/app.db")
cursor = sql.cursor()

# Classes dependencies
import model.functions.database as db
import model.classes.user as user
import model.classes.vehicle as vehicle

cursor.execute("PRAGMA foreign_keys = ON;")
db.init()
# # Start GUI from here

# print(cursor.execute("PRAGMA foreign_keys;").fetchone())
test = True
if test:
    users = db.select_all_users()
    n = 3
    db.populate_user(n)
    db.populate_vehicle(n)

    users = db.select_all_users()
    vehicles = db.select_all_cars()

    for user in users:
        print(user)
        print("\n--------\n")
    for vehicle in vehicles:
        print(vehicle)
