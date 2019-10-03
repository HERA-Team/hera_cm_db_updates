#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

log_file = 'scripts.log'
do_it_this_time = True

# Set the date
cdate = '2018/09/19'
print("Update for:  ", format(cdate))

# List the connections to stop and associated time
cstop_time = "10:00"
connections_to_stop = [
                      [['PAM75191', 'A', '@slot'], ['PCH1', 'A', '@slot07']],
                      [['PAM75192', 'A', '@slot'], ['PCH1', 'A', '@slot01']],
                      [['PAM75193', 'A', '@slot'], ['PCH1', 'A', '@slot02']],
                      [['PAM75194', 'A', '@slot'], ['PCH1', 'A', '@slot03']],
                      [['PAM75195', 'A', '@slot'], ['PCH1', 'A', '@slot05']],
                      [['PAM75195', 'A', 'eb'], ['SNP008', 'A', 'e6']],
                      [['PAM75195', 'A', 'nb'], ['SNP008', 'A', 'n4']],
                      [['PAM75196', 'A', '@slot'], ['PCH1', 'A', '@slot06']],
                      [['PAM75196', 'A', 'eb'], ['SNP008', 'A', 'e2']],
                      [['PAM75196', 'A', 'nb'], ['SNP008', 'A', 'n0']],
                      [['SNP008', 'A', 'rack'], ['N0', 'A', 'loc1']],
                      [['SNP023', 'A', 'rack'], ['N0', 'A', 'loc3']],
                      [['SNP024', 'A', 'rack'], ['N0', 'A', 'loc2']],
                      [['FEM06', 'A', 'e'], ['CRF000', 'A', 'ea']],
                      [['FEM06', 'A', 'n'], ['CRF000', 'A', 'na']],
                      [['FDV1', 'A', 'terminals'], ['FEM06', 'A', 'input']],
                      [['FDV2', 'A', 'terminals'], ['FEM04', 'A', 'input']],
                      [['CRF000', 'A', 'eb'], ['PAM75196', 'A', 'ea']],
                      [['CRF000', 'A', 'nb'], ['PAM75196', 'A', 'na']],
                      [['FEM04', 'A', 'e'], ['CRF001', 'A', 'ea']],
                      [['FEM04', 'A', 'n'], ['CRF001', 'A', 'na']],
                      [['CRF001', 'A', 'eb'], ['PAM75195', 'A', 'ea']],
                      [['CRF001', 'A', 'nb'], ['PAM75195', 'A', 'na']],
]

# List the parts to stop and associated time (last two per entry are ignored)
pstop_time = "10:10"
parts_to_stop = [
                ['FEM06', 'A', '-', '-'],
                ['FEM04', 'A', '-', '-'],
                ['SNP008', 'A', '-', '-'],
                ['SNP023', 'A', '-', '-'],
                ['SNP024', 'A', '-', '-']
]

# List the parts to add and associated time
pstart_time = "10:20"
parts_to_add = [
               ['FEM96', 'A', 'front-end', 'FEMxxx96'],
               ['FEM92', 'A', 'front-end', 'FEMxxx92'],
               ['SNPA000024', 'A', 'snap', 'A000024'],
               ['SNPA000022', 'A', 'snap', 'A000022'],
               ['SNPA000008', 'A', 'snap', 'A000008'],
               ['PAM75199', 'A', 'post-amp', 'PAM75199']
]

# List the connections to add and associated time
cstart_time = "10:30"
connections_to_add = [
                     [['PAM75196', 'A', '@slot'], ['PCH1', 'A', '@slot02']],
                     [['PAM75196', 'A', 'eb'], ['SNPA000022', 'A', 'e6']],
                     [['PAM75196', 'A', 'nb'], ['SNPA000022', 'A', 'n4']],
                     [['FDV1', 'A', 'terminals'], ['FEM96', 'A', 'input']],
                     [['FEM96', 'A', 'e'], ['CRF000', 'A', 'ea']],
                     [['FEM96', 'A', 'n'], ['CRF000', 'A', 'na']],
                     [['CRF000', 'A', 'eb'], ['PAM75199', 'A', 'ea']],
                     [['CRF000', 'A', 'nb'], ['PAM75199', 'A', 'na']],
                     [['PAM75199', 'A', 'eb'], ['SNPA000022', 'A', 'e2']],
                     [['PAM75199', 'A', 'nb'], ['SNPA000022', 'A', 'n0']],
                     [['SNPA000022', 'A', 'rack'], ['N0', 'A', 'loc1']],
                     [['FDV2', 'A', 'terminals'], ['FEM92', 'A', 'input']],
                     [['FEM92', 'A', 'e'], ['CRF001', 'A', 'ea']],
                     [['FEM92', 'A', 'n'], ['CRF001', 'A', 'na']],
                     [['CRF001', 'A', 'eb'], ['PAM75196', 'A', 'ea']],
                     [['CRF001', 'A', 'nb'], ['PAM75196', 'A', 'na']],
                     [['PAM75196', 'A', 'eb'], ['SNPA000022', 'A', 'e6']],
                     [['PAM75196', 'A', 'nb'], ['SNPA000022', 'A', 'n4']],
                     [['SNPA000024', 'A', 'rack'], ['N0', 'A', 'loc2']],
                     [['SNPA000008', 'A', 'rack'], ['N0', 'A', 'loc3']]
]

fp = pc.init_script(sys.argv, log_file)


def do_part(add_or_stop, hpn, rev, htype, serno, cdate, ctime, do_it_this_time):
    part = [hpn, rev, htype, serno]
    fp.write(pc.part(add_or_stop, part, cdate, ctime, do_it_this_time))


def do_connection(add_or_stop, upart, urev, uport, dpart, drev, dport, cdate, ctime, do_it_this_time):
    up = [upart, urev, uport]
    down = [dpart, drev, dport]
    fp.write(pc.connect(add_or_stop, up, down, cdate, ctime, do_it_this_time))


for c in connections_to_stop:
    upart = c[0][0]
    urev = c[0][1]
    uport = c[0][2]
    dpart = c[1][0]
    drev = c[1][1]
    dport = c[1][2]
    do_connection('stop', upart, urev, uport, dpart, drev, dport, cdate, cstop_time, do_it_this_time)

for p in parts_to_stop:
    do_part('stop', p[0], p[1], p[2], p[3], cdate, pstop_time, do_it_this_time)

for p in parts_to_add:
    do_part('add', p[0], p[1], p[2], p[3], cdate, pstart_time, do_it_this_time)

for c in connections_to_add:
    upart = c[0][0]
    urev = c[0][1]
    uport = c[0][2]
    dpart = c[1][0]
    drev = c[1][1]
    dport = c[1][2]
    do_connection('add', upart, urev, uport, dpart, drev, dport, cdate, cstart_time, do_it_this_time)

fp.close()
