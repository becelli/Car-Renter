from datetime import datetime as dt, timedelta as td

a = dt.strptime("01/01/2020", "%d/%m/%Y")
b = td(days=1)
c = a + b
print(c)
