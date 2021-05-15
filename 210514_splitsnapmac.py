from hera_cm import signal_chain

mc = {}  # from hera_mc
gs = {}  # from the googlesheet
sh = {}  # from hera-snap-head

with open('210514_snapmac_numbers.csv', 'r') as fp_numbers:
    for line in fp_numbers:
        if line.startswith('From'):
            header = line.strip()
            continue
        data = line.strip().split(',')
        if len(data[0]):
            if data[1] in mc.keys():
                print(f"{data[1]} already present in mc")
            mc[data[1]] = data[0]
        if len(data[2]):
            if data[3] in gs.keys():
                print(f"{data[3]} already present in gs")
            gs[data[3]] = data[2]
        if len(data[4]):
            if data[5] in sh.keys():
                print(f"{data[5]} already present in sh")
            sh[data[5]] = data[4]

fullset = set(list(mc.keys()) + list(gs.keys()) + list(sh.keys()))

snaps = {}
for key in fullset:
    snaps[key] = {'mc': "", 'gs': "", 'sh': "",
                  'cnt': 0, 'set': set()}
    if key in mc.keys() and mc[key].count(':') == 5:
        snaps[key]['mc'] = mc[key]
        snaps[key]['cnt'] += 1
        snaps[key]['set'].add(mc[key])
    if key in gs.keys() and gs[key].count(':') == 5:
        snaps[key]['gs'] = gs[key]
        snaps[key]['cnt'] += 1
        snaps[key]['set'].add(gs[key])
    if key in sh.keys() and sh[key].count(':') == 5:
        snaps[key]['sh'] = sh[key]
        snaps[key]['cnt'] += 1
        snaps[key]['set'].add(sh[key])

fp = open('snapmac_numbers_out.csv', 'w')
fphosts = open('hosts.snap', 'w')
header = "SNAP,HERA_MC,GOOGLESHEET,HOSTS"
print(header, file=fp)


unique_macs = []
add_macs_to_mc = {}


for key in sorted(fullset):
    print("{},{},{},{}".format(key, snaps[key]['mc'], snaps[key]['gs'], snaps[key]['sh']), file=fp)
    if snaps[key]['cnt'] > 1 and len(snaps[key]['set']) > 1:
        print("Not the same:  ", key, snaps[key])
    if not snaps[key]['cnt']:
        print("No entries:  ", key, snaps[key])
    else:
        this_mac = list(snaps[key]['set'])[0]
        print("{} {}".format(this_mac, key), file=fphosts)
        if this_mac in unique_macs:
            print(f"{this_mac} already in {key}")
        else:
            unique_macs.append(this_mac)
        if key not in mc.keys():
            add_macs_to_mc[key] = this_mac
fp.close()
fphosts.close()

# read off manually...
add_snaps_to_mc = ['A000023', 'C000005', 'C000012', 'C000026', 'C000027', 'C000034', 'C000036',
                   'C000039', 'C000041', 'C000052', 'C000059', 'C000069', 'C000073', 'C000075',
                   'C000077', 'C000080', 'C000084', 'C000087', 'C000088', 'C000089', 'C000090',
                   'C000091', 'C000092', 'C000093', 'C000094', 'C000095', 'C000098', 'C000099',
                   'C000100', 'C000101', 'C000113', 'C000114', 'C000116', 'C000117', 'C000118',
                   'C000119', 'C000120', 'C000121', 'C000123', 'C000124', 'C000125', 'C000126',
                   'C000127', 'C000128', 'C000129']

updsn = signal_chain.Update('update_snaps')
for sn2ad in add_snaps_to_mc:
    hpn = f"SNP{sn2ad}"
    updsn.update_part('add', [hpn, 'A', 'snap', sn2ad], '2021/05/01', '10:00')
for in2ad, mac in add_macs_to_mc.items():
    note = f"MAC - {mac}"
    updsn.add_part_info(in2ad, 'A', note, '2021/05/13', '11:00')
updsn.done()
