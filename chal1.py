f = open('logins.txt','r').read().split('\n')

curr_dt = None
users = set()
for line in f:
    if not line:
        break
    dt, tm, usr, status = line.split("\t")
    if dt != curr_dt:
        curr_dt = dt
        users = set()
    if usr in users:
        if status == "IN" and "e" == usr[0]:
            print(usr) 
            break
            
    
    else:
        if status == "IN":
            users.add(usr)

    