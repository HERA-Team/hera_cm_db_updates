import numpy as np


hant, dhant = [], {}
aant, daant = [], {}
hsta = []

# \o hant.txt
# select * from parts where hpn like 'H%';
with open('hant.txt', 'r') as fp:
    for line in fp:
        data = line.split('|')
        a = int(data[0][3:])
        b = int(data[3])
        hant.append([a, b])
        dhant[a] = b
hant = np.array(hant)

# \o aant.txt
# select * from parts where hpn like 'A%';
with open('aant.txt', 'r') as fp:
    for line in fp:
        data = line.split('|')
        a = int(data[0][2:])
        try:
            end = int(data[5])
            continue
        except ValueError:
            pass
        try:
            b = int(data[3])
        except ValueError:
            b = int(data[3][2:])
        aant.append([a, b])
        daant[a] = b
aant = np.array(aant)

# \o hsta.txt
# select * from geo_location where station_name like 'H%';
with open('hsta.txt', 'r') as fp:
    for line in fp:
        data = line.split('|')
        hsta.append([int(data[0][3:]), float(data[4]), float(data[5])])
hsta = np.array(hsta)
