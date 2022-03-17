"""
Use 'hookup.py > nants.out'
Writes nants.csv
"""
fout = open('nants.csv', 'w')

nodes = {}
with open('nants.out', 'r') as fp:
    for line in fp:
        if line[0] != 'H':
            continue
        b = [a.split('>') for a in line.strip().split('<')]
        x = []
        for a in b:
            if len(a) == 1:
                x.append(a[0].strip())
            else:
                x.append("{}".format('-'.join([z.strip() for z in a[0].split()])))
                x.append(a[1].split()[0].strip())
        print(','.join(x), file=fout)
        if len(x[-1].strip()):
            nodes.setdefault(x[-1], [])
            nodes[x[-1]].append(x)

nodelist = sorted(nodes.keys())
for nn in nodelist:
    print(f"{nn} - ", end=' ')
    ants = set()
    for a in nodes[nn]:
        ants.add(a[0])
    print(f"{len(ants):02d}: {','.join(ants)}")
