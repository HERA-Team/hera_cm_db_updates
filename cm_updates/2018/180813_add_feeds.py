#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Add new feeds.")

log_file = 'scripts.log'
do_it_this_time = True

parts_to_add = [['FDV1', 'A', 'feed', 'MIT1'],
                ['FDV2', 'A', 'feed', 'MIT2'],
                ['FDV3', 'A', 'feed', 'MIT3'],
                ['FDV4', 'A', 'feed', 'CCL'],
                ['FDV5', 'A', 'feed', 'CCL'],
                ['FDV6', 'A', 'feed', 'CCL'],
                ['FDV7', 'A', 'feed', 'CCL']
                ]
connections_to_add = [[['A0', 'H', 'focus'], ['FDV1', 'A', 'input']],
                      [['A1', 'H', 'focus'], ['FDV2', 'A', 'input']],
                      [['A12', 'H', 'focus'], ['FDV3', 'A', 'input']],
                      [['A13', 'H', 'focus'], ['FDV4', 'A', 'input']],
                      [['A14', 'H', 'focus'], ['FDV5', 'A', 'input']],
                      [['A25', 'H', 'focus'], ['FDV6', 'A', 'input']],
                      [['A26', 'H', 'focus'], ['FDV7', 'A', 'input']]]

cdate = ['2018/05/21', '2018/05/21', '2018/05/21', '2018/08/10', '2018/08/10', '2018/08/10', '2018/08/10']

fp = pc.init_script(sys.argv, log_file)


def add_part(hpn, rev, htype, serno, cdate, ctime, do_it_this_time):
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))


def add_connection(upart, urev, uport, dpart, drev, dport, cdate, ctime, do_it_this_time):
    up = [upart, urev, uport]
    down = [dpart, drev, dport]
    fp.write(pc.connect('add', up, down, cdate, ctime, do_it_this_time))


ctime = '11:00'
for i, p in enumerate(parts_to_add):
    add_part(p[0], p[1], p[2], p[3], cdate[i], ctime, do_it_this_time)

ctime = '12:00'
for i, c in enumerate(connections_to_add):
    upart = c[0][0]
    urev = c[0][1]
    uport = c[0][2]
    dpart = c[1][0]
    drev = c[1][1]
    dport = c[1][2]
    add_connection(upart, urev, uport, dpart, drev, dport, cdate[i], ctime, do_it_this_time)

fp.close()
