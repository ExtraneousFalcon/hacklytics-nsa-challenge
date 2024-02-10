f = open('logins.txt', 'r').read().split('\n')

last = set()
users = set()
for line in f:
    if not line:
        break
    dt, tm, usr, status = line.split("\t")
    if usr in last:
        continue
    if dt > "2021-01-11":
        users.add(usr)
    last.add(usr)

print(len(users))
