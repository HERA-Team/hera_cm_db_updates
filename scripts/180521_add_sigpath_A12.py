#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Set up new sigpath")

log_file = 'scripts.log'
do_it_this_time = True

parts_to_add = [['FDV3', 'A', 'feed', 'MIT3'],
                ['FEM02', 'A', 'fem', 'FEMxxx02'],
                ['CRF012', 'A', 'cable-rfof', 'orangegray']]
connections_to_add = [[['A12', 'H', 'focus'], ['FDV3', 'A', 'input']],
                      [['FDV3', 'A', 'terminals'], ['FEM02', 'A', 'input']],
                      [['FEM02', 'A', 'e'], ['CRF012', 'A', 'ea']],
                      [['FEM02', 'A', 'n'], ['CRF012', 'A', 'na']],
                      [['CRF012', 'A', 'eb'], ['PAM05', 'A', 'ea']],
                      [['CRF012', 'A', 'nb'], ['PAM05', 'A', 'na']],
                      [['PAM05', 'A', 'eb'], ['SNP1', 'A', 'e3']],
                      [['PAM05', 'A', 'nb'], ['SNP1', 'A', 'n3']]]

fp = pc.init_script(sys.argv, log_file)


def add_part(hpn, rev, htype, serno, cdate, ctime, do_it_this_time):
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))


def add_connection(upart, urev, uport, dpart, drev, dport, cdate, ctime, do_it_this_time):
    up = [upart, urev, uport]
    down = [dpart, drev, dport]
    fp.write(pc.connect('add', up, down, cdate, ctime, do_it_this_time))


cdate = '2018/05/21'

ctime = '11:00'
for p in parts_to_add:
    add_part(p[0], p[1], p[2], p[3], cdate, ctime, do_it_this_time)

ctime = '12:00'
for c in connections_to_add:
    upart = c[0][0]
    urev = c[0][1]
    uport = c[0][2]
    dpart = c[1][0]
    drev = c[1][1]
    dport = c[1][2]
    add_connection(upart, urev, uport, dpart, drev, dport, cdate, ctime, do_it_this_time)

fp.close()
