from view.gui import init as gui_init
import model.functions.database as db


def init_database():
    n = 5
    db.init()
    db.populate_user(n)
    db.populate_vehicle(n)


def main():
    gui_init()


def test():
    db.init()
    init_gui()
    init_gui()
    test = False
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


def select_all_vehicles():
    return db.select_all_vehicles()


def select_all_national_vehicles():
    return db.select_all_national_vehicles()


def select_all_imported_vehicles():
    return db.select_all_imported_vehicles()
