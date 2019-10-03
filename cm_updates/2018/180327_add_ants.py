#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Updates addressing HERA_Commissioning issue #112")

log_file = 'scripts.log'
do_it_this_time = True

ants_to_add = ['180', '181', '182', '183']
fems_to_add = ['75064', '75065', '75047']
pams_to_add = ['75153', '75154', '75155', '75156']
feeds_to_add = ['69', '70', '71', '73']
connections_to_stop = []
connections_to_add = [
                     [['HH180', 'A', 'ground'], ['A180', 'H', 'ground']],
                     [['A180', 'H', 'focus'], ['FDA69', 'B', 'input']],
                     [['FDA69', 'B', 'terminals'], ['FEM75064', 'A', 'input']],
                     [['FEM75064', 'A', 'e'], ['C7F180', 'A', 'ea']],
                     [['FEM75064', 'A', 'n'], ['C7F180', 'A', 'na']],
                     [['C7F180', 'A', 'eb'], ['RI2B1E', 'A', 'a']],
                     [['C7F180', 'A', 'nb'], ['RI2B1N', 'A', 'a']],
                     [['RI2B1E', 'A', 'b'], ['PAM75156', 'B', 'ea']],
                     [['RI2B1N', 'A', 'b'], ['PAM75156', 'B', 'na']],
                     [['PAM75156', 'B', 'eb'], ['RO2B1E', 'A', 'a']],
                     [['PAM75156', 'B', 'nb'], ['RO2B1N', 'A', 'a']],
                     [['HH181', 'A', 'ground'], ['A181', 'H', 'ground']],
                     [['A181', 'H', 'focus'], ['FDA70', 'B', 'input']],
                     [['FDA70', 'B', 'terminals'], ['FEM75065', 'A', 'input']],
                     [['FEM75065', 'A', 'e'], ['C7F181', 'A', 'ea']],
                     [['FEM75065', 'A', 'n'], ['C7F181', 'A', 'na']],
                     [['C7F181', 'A', 'eb'], ['RI2B2E', 'A', 'a']],
                     [['C7F181', 'A', 'nb'], ['RI2B2N', 'A', 'a']],
                     [['RI2B2E', 'A', 'b'], ['PAM75155', 'B', 'ea']],
                     [['RI2B2N', 'A', 'b'], ['PAM75155', 'B', 'na']],
                     [['PAM75155', 'B', 'eb'], ['RO2B2E', 'A', 'a']],
                     [['PAM75155', 'B', 'nb'], ['RO2B2N', 'A', 'a']],
                     [['HH182', 'A', 'ground'], ['A182', 'H', 'ground']],
                     [['A182', 'H', 'focus'], ['FDA71', 'B', 'input']],
                     [['FDA71', 'B', 'terminals'], ['FEM75043', 'A', 'input']],
                     [['FEM75043', 'A', 'e'], ['C7F182', 'A', 'ea']],
                     [['FEM75043', 'A', 'n'], ['C7F182', 'A', 'na']],
                     [['C7F182', 'A', 'eb'], ['RI2B3E', 'A', 'a']],
                     [['C7F182', 'A', 'nb'], ['RI2B3N', 'A', 'a']],
                     [['RI2B3E', 'A', 'b'], ['PAM75154', 'B', 'ea']],
                     [['RI2B3N', 'A', 'b'], ['PAM75154', 'B', 'na']],
                     [['PAM75154', 'B', 'eb'], ['RO2B3E', 'A', 'a']],
                     [['PAM75154', 'B', 'nb'], ['RO2B3N', 'A', 'a']],
                     [['HH183', 'A', 'ground'], ['A183', 'H', 'ground']],
                     [['A183', 'H', 'focus'], ['FDA73', 'B', 'input']],
                     [['FDA73', 'B', 'terminals'], ['FEM75047', 'A', 'input']],
                     [['FEM75047', 'A', 'e'], ['C7F183', 'A', 'ea']],
                     [['FEM75047', 'A', 'n'], ['C7F183', 'A', 'na']],
                     [['C7F183', 'A', 'eb'], ['RI2B4E', 'A', 'a']],
                     [['C7F183', 'A', 'nb'], ['RI2B4N', 'A', 'a']],
                     [['RI2B4E', 'A', 'b'], ['PAM75153', 'B', 'ea']],
                     [['RI2B4N', 'A', 'b'], ['PAM75153', 'B', 'na']],
                     [['PAM75153', 'B', 'eb'], ['RO2B4E', 'A', 'a']],
                     [['PAM75153', 'B', 'nb'], ['RO2B4N', 'A', 'a']]
]

fp = pc.init_script(sys.argv, log_file)


def add_part(hpn, rev, htype, serno, cdate, ctime, do_it_this_time):
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))


# Add parts
cdate = '2018/03/26'
ctime = '10:00'
for s in ants_to_add:
    fp.write('add_station.py {}\n'.format('HH' + s))
sn = 80
for a in ants_to_add:
    add_part('A' + a, 'H', 'antenna', 'S/N' + str(sn), cdate, ctime, do_it_this_time)
    sn += 1
for f in feeds_to_add:
    add_part('FDA' + f, 'B', 'feed', 'P' + f, cdate, ctime, do_it_this_time)
for f in fems_to_add:
    add_part('FEM' + f, 'A', 'front-end', f, cdate, ctime, do_it_this_time)
for c in ants_to_add:
    add_part('C7F' + c, 'A', 'cable-feed75', 'P' + c, cdate, ctime, do_it_this_time)
for p in pams_to_add:
    add_part('PAM' + p, 'B', 'post-amp', p, cdate, ctime, do_it_this_time)

# Stop then update old connections per issue 109
cdate = '2018/03/26'
ctime = '11:00'
for c in connections_to_stop:
    fp.write(pc.connect('stop', c[0], c[1], cdate, ctime, do_it_this_time))
ctime = '12:00'
for c in connections_to_add:
    fp.write(pc.connect('add', c[0], c[1], cdate, ctime, do_it_this_time))

fp.close()
