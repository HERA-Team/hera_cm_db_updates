#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Set up new sigpath")

log_file = 'scripts.log'
do_it_this_time = True

parts_to_add = [['FEM06', 'A', 'front-end', 'FEMxxx06'],
                ['CRF000', 'A', 'cable-rfof', 'bluewhite'],
                ['FEM04', 'A', 'front-end', 'FEMxxx04'],
                ['CRF001', 'A', 'cable-rfof', 'browngreen']
                ]
connections_to_add = [[['A0', 'H', 'focus'], ['FDV1', 'A', 'input']],
                      [['FDV1', 'A', 'terminals'], ['FEM06', 'A', 'input']],
                      [['FEM06', 'A', 'e'], ['CRF000', 'A', 'ea']],
                      [['FEM06', 'A', 'n'], ['CRF000', 'A', 'na']],
                      [['CRF000', 'A', 'eb'], ['PAM75196', 'A', 'ea']],
                      [['CRF000', 'A', 'nb'], ['PAM75196', 'A', 'na']],
                      [['PAM75196', 'A', 'eb'], ['SNP008', 'A', 'e2']],
                      [['PAM75196', 'A', 'nb'], ['SNP008', 'A', 'n0']],
                      [['A1', 'H', 'focus'], ['FDV2', 'A', 'input']],
                      [['FDV2', 'A', 'terminals'], ['FEM04', 'A', 'input']],
                      [['FEM04', 'A', 'e'], ['CRF001', 'A', 'ea']],
                      [['FEM04', 'A', 'n'], ['CRF001', 'A', 'na']],
                      [['CRF001', 'A', 'eb'], ['PAM75195', 'A', 'ea']],
                      [['CRF001', 'A', 'nb'], ['PAM75195', 'A', 'na']],
                      [['PAM75195', 'A', 'eb'], ['SNP008', 'A', 'e6']],
                      [['PAM75195', 'A', 'nb'], ['SNP008', 'A', 'n4']]
                      ]

fp = pc.init_script(sys.argv, log_file)


def add_part(hpn, rev, htype, serno, cdate, ctime, do_it_this_time):
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))


def add_connection(upart, urev, uport, dpart, drev, dport, cdate, ctime, do_it_this_time):
    up = [upart, urev, uport]
    down = [dpart, drev, dport]
    fp.write(pc.connect('add', up, down, cdate, ctime, do_it_this_time))


cdate = '2018/07/21'

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
