from datetime import datetime, timedelta

f = open("logins.txt", "r").read().split("\n")[:-1]


def diff_helper(time1, time2):

    datetime1 = datetime.combine(datetime.today(), time1)
    datetime2 = datetime.combine(datetime.today(), time2)

    time_delta = datetime2 - datetime1
    return time_delta


def diff_time(time1, time2, val):

    datetime1 = datetime.combine(datetime.today(), time1)
    datetime2 = datetime.combine(datetime.today(), time2)

    time_delta = datetime2 - datetime1
    val = timedelta(minutes=val)

    return abs(time_delta) <= timedelta(minutes=24 * 60) - val and (
        time_delta > val or time_delta < -val
    )


targ = {}
dates = {}
rem = set()
use = set()
TEST = False
for line in f:
    dt, tm, usr, status = line.split("\t")
    rem.add(usr)
    use.add(dt)
    if status == "OUT":
        continue
    if usr not in targ:
        targ[usr] = datetime.strptime(dt + " " + tm, "%Y-%m-%d %H:%M:%S").time()

    if usr not in dates:
        dates[usr] = {}
    dates[usr][dt] = diff_helper(
        targ[usr], datetime.strptime(dt + " " + tm, "%Y-%m-%d %H:%M:%S").time()
    )


main_per = "s.kinkel"
cnt = {}
for usr in rem:
    cnt[usr] = 10
for line in f:
    dt, tm, usr, status = line.split("\t")
    if dt not in dates[main_per]:
        continue

    if usr == main_per or usr not in rem or usr not in dates or dt not in dates[usr]:
        continue
    if len(dates[usr]) < 10:
        rem.remove(usr)
    if (
        abs(dates[main_per][dt] - dates[usr][dt]) > timedelta(minutes=10)
        and status == "IN"
    ):
        cnt[usr] -= 1
        if cnt[usr] < 1:
            rem.remove(usr)


ans = timedelta(0)
best = None


for date in use:
    s = timedelta(0)
    tot = 0
    for person in rem:
        if date in dates[person]:
            s += dates[person][date]
            tot += 1
    if tot < 1:
        continue
    s = s.total_seconds() / tot
    s = timedelta(seconds=s)
    if s > ans:
        ans = s
        best = date


print(ans)
print(rem)
print(best)

test = timedelta(0)
dt = None
for usr in rem:
    for date in dates[usr]:
        if dates[usr][date] > test:
            test = dates[usr][date]
            dt = date

print(test)
print(dt)
