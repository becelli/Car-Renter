import controller.controller as controller
import view.main as gui

db = "app.db"

c = controller.Controller(db=db)
c.init_database(20)
gui.main(db)
