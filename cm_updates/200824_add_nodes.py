#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)

nodes = [6, 9, 11, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
sns = ['2#16', '1#1', '2#20', '2#17', '2#12', '2#11', '2#10', '2#',
       '2#', '2#', '2#', '2#', '2#', '2#', '2#']
cdate = '2020/08/01'
for node, sn in zip(nodes, sns):
    sn = 'H0030-2601.' + sn
    hera.just_add_node(node, sn, cdate=cdate, ctime='10:00')

door_dir = ['E', 'NW', 'E', 'SW', 'NW', 'NE', 'SE', 'N', 'NE', 'E', 'SE', 'SW', 'NW', 'NE',
            'SE', 'SW', 'S', 'E', 'SE', 'SE', 'NW', 'NE', 'NW', 'NW', 'NE', 'SE', 'SW', 'NW']

for i, dd in enumerate(door_dir):
    hpn = 'ND{:02d}'.format(i)
    note = 'Door direction: {}'.format(dd)
    hera.add_part_info(hpn, 'A', note, cdate, ctime='12:00')

hera.done()
