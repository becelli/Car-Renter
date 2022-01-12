import controller.controller as controller
import view.main as gui

db = "app2.db"

c = controller.Controller(db=db)
c.init_database()
gui.main(db)
