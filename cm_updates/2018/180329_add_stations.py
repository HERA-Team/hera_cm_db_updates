#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Updates antennas per Ziyaads email")

log_file = 'scripts.log'
do_it_this_time = True

stations_to_add = ['73', '74', '89', '90', '91', '178', '179', '184', '185', '186',
                   '198', '199', '200', '201', '202', '203', '204', '216', '217', '218',
                   '220', '221', '222', '223', '224', '225', '233', '235', '236', '237',
                   '238', '239', '240', '241', '242', '243', '250', '252', '253', '254',
                   '255', '256', '257', '258', '259', '260', '266', '281']

fp = pc.init_script(sys.argv, log_file)


def add_part(hpn, rev, htype, serno, cdate, ctime, do_it_this_time):
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))


cdate = '2018/03/29'
ctime = '10:00'
for s in stations_to_add:
    fp.write('add_station.py {}\n'.format('HH' + s))
sn = 84
for a in stations_to_add:
    add_part('A' + a, 'H', 'antenna', 'S/N' + str(sn), cdate, ctime, do_it_this_time)
    sn += 1

ctime = '12:00'
for s in stations_to_add:
    c = [['HH' + s, 'A', 'ground'], ['A' + s, 'H', 'ground']]
    fp.write(pc.connect('add', c[0], c[1], cdate, ctime, do_it_this_time))
fp.close()
