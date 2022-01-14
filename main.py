import controller.controller as controller
import view.main as gui
import random as rnd

db = f"app{rnd.randint(0, 327672131232)}.db"

c = controller.Controller(db=db)
c.init_database(20)
gui.main(db)
