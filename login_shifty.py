from datetime import datetime, timedelta

f = open("logins.txt", "r").read().split("\n")

IN = {}
OUT = {}
FIRST = {}
SECOND = {}


def diff_time(time1, time2, val):

    datetime1 = datetime.combine(datetime.today(), time1)
    datetime2 = datetime.combine(datetime.today(), time2)

    time_delta = datetime2 - datetime1
    val = timedelta(minutes=val)

    return abs(time_delta) <= timedelta(minutes=24 * 60) - val and (
        time_delta > val or time_delta < -val
    )


val = 240
ans = None
for line in f:
    if not line:
        break
    dt, tm, usr, status = line.split("\t")
    tm = datetime.strptime(tm, "%H:%M:%S").time()
    if status == "IN":
        if usr in IN:
            if dt == FIRST[usr]:
                IN[usr].append(tm)
                continue

            check = False
            for temp in IN[usr]:
                if not diff_time(tm, temp, val):
                    check = True
                    break
            if not check and usr[0] == "j":

                ans = usr
                break
        else:
            FIRST[usr] = dt
            IN[usr] = [tm]

    else:
        if usr in OUT:
            if dt == SECOND[usr]:
                OUT[usr].append(tm)
                continue

            check = False
            for temp in OUT[usr]:
                if not diff_time(tm, temp, val):
                    check = True
                    break
            if not check and usr[0] == "j":

                ans = usr
                break

        else:
            SECOND[usr] = dt
            OUT[usr] = [tm]


print(ans)
