# Init database
import sqlite3 as sql

cars = sql.connect("./db/application.db")
cursor = cars.cursor()

# Classes dependencies
import functions.database as db
import classes.user as user
import classes.vehicle as vehicle

db.init()
# # Start GUI from here


test = False
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
