f = open('logins.txt', 'r').read().split('\n')

users = set()
for line in f:
    if not line:
        break
    dt, tm, usr, status = line.split("\t")
    
    if usr[0] == "j":
        users.add(usr)

print(len(users))
print(dates['t.thames'])
