fp = open('hh.out', 'r')
hh = {}

for line in fp:
    data = line.split('|')
    dte = data[5].split()
    dte.append(data[1].strip())
    xxx = ''.join(dte)
    if xxx in hh.keys():
        print(xxx)
    hh[xxx] = data[1:]
fp.close()

sortedkeys = sorted(hh.keys())

newsn = {}
Anew = {}
fp = open('hh.txt', 'w')
for i, k in enumerate(sortedkeys):
    x = hh[k][0].strip()
    s = '{:5s} {:3s}  H{:03d} {}\n'.format(x, hh[k][3].strip(), i + 1, hh[k][4])
    newsn[x] = '{:03d}'.format(i + 1)
    Akey = 'A' + x[2:]
    Anew[Akey] = 'H{:03d}'.format(i + 1)
    fp.write(s)
fp.close()

fpin = open('update_sn_initialization_data_parts.csv', 'r')
fput = open('new_initialization_data_parts.csv', 'w')

for line in fpin:
    up = line.strip()
    data = up.split(',')
    if data[0] in newsn.keys():
        print("Update station:  ", data[0])
        data[3] = newsn[data[0]]
        up = ','.join(data)
    if data[0] in Anew.keys() and data[1] == 'H':
        print("Update antenna:  ", data[0], data[1])
        data[3] = Anew[data[0]]
        up = ','.join(data)
    up += '\n'
    fput.write(up)
