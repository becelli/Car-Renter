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
# db.init()
# # Start GUI from here


test = True
# test = False
if test:
    n = 5
    # db.populate_user(n)
    # db.populate_vehicle(n)
    # db.populate_rent(n)
    # db.populate_payment(n)
    # db.populate_insurance(n)
    users = db.select_all_users()

    users = db.select_all_users()
    vehicles = db.select_all_vehicles()

    # for user in users:
    #     print(user)
    for vehicle in vehicles:
        # print(vehicle)
        pass

# user2 = db.select_employee("13129652527")
# print(user2)
national = db.select_imported_vehicle("KCW-2989")
# national = db.select_all_imported()
print(national)
