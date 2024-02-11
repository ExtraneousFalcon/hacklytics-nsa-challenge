import json
f = open('a1.txt','r').read().split('\n')

ips = set()

for i in f:
    ips.add(i.split('\t')[0])

f = open('a2.txt','r').read().split('\n')

for i in f:
    ips.add(i.split(': ')[1])

f = json.loads(open('a3.json','r').read())
for i in f:
    ips.add(i['ip'])


f = open('attack.txt','w')
for i in ips:
    f.write(i+'\n')