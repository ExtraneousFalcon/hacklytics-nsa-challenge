from datetime import datetime, timedelta
f = open('logins.txt', 'r').read().split('\n')

last = {}

for line in f:
    if not line:
        break
    dt, tm, usr, status = line.split("\t")
    date_object = datetime.strptime(dt, "%Y-%m-%d")

    if usr in last and date_object - last[usr] > timedelta(days=15) and usr[0] == "m":
        print(usr)

    last[usr] = datetime.strptime(dt, "%Y-%m-%d")
