import controller.controller as c

# d = int(input("Debug mode? (1/0): "))
d = 1
c.init_database()
c.main()
if not d:
    3
else:
    eval(input("Enter a command: "))
