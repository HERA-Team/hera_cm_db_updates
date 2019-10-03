#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

log_file = 'scripts.log'
do_it_this_time = True

# Set the date
cdate = '2018/10/30'
print("Update for:  ", format(cdate))

# List the connections to stop and associated time
cstop_time = "10:00"
connections_to_stop = [
                      [['A13', 'H', 'focus'], ['FDA31', 'B', 'input']],
                      [['A25', 'H', 'focus'], ['FDA20', 'B', 'input']],
                      [['A26', 'H', 'focus'], ['FDA89', 'B', 'input']],
                      [['FDV2', 'A', 'terminals'], ['FEM92', 'A', 'input']],
                      [['FEM92', 'A', 'e'], ['CRF001', 'A', 'ea']],
                      [['FEM92', 'A', 'n'], ['CRF001', 'A', 'na']],
                      [['CRF000', 'A', 'eb'], ['PAM75199', 'A', 'ea']],
                      [['CRF000', 'A', 'nb'], ['PAM75199', 'A', 'na']],
                      [['PAM75199', 'A', 'eb'], ['SNPA000022', 'A', 'e2']],
                      [['PAM75199', 'A', '@slot'], ['PCH1', 'A', '@slot01']],
                      [['FDV1', 'A', 'terminals'], ['FEM96', 'A', 'input']],
                      [['FEM96', 'A', 'e'], ['CRF000', 'A', 'ea']],
                      [['FEM96', 'A', 'n'], ['CRF000', 'A', 'na']],
                      [['CRF001', 'A', 'eb'], ['PAM75196', 'A', 'ea']],
                      [['CRF001', 'A', 'nb'], ['PAM75196', 'A', 'na']],
                      [['PAM75196', 'A', 'nb'], ['SNPA000022', 'A', 'n4']],
                      [['PAM75196', 'A', '@slot'], ['PCH1', 'A', '@slot02']]
]

# List the parts to stop and associated time (last two per entry are ignored)
pstop_time = "10:10"
parts_to_stop = [
                ['FEM92', 'A', '-', '-'],
                ['FEM96', 'A', '-', '-']
]

# List the parts to add and associated time
pstart_time = "10:20"
parts_to_add = [
               ['FEM010', 'A', 'front-end', 'FEM010'],
               ['FEM011', 'A', 'front-end', 'FEM011'],
               ['FEM012', 'A', 'front-end', 'FEM012'],
               ['FEM013', 'A', 'front-end', 'FEM013'],
               ['FEM014', 'A', 'front-end', 'FEM014'],
               ['FEM015', 'A', 'front-end', 'FEM015'],
               ['PAM010', 'A', 'post-amp', 'PAM010'],
               ['PAM011', 'A', 'post-amp', 'PAM011'],
               ['PAM012', 'A', 'post-amp', 'PAM012'],
               ['PAM013', 'A', 'post-amp', 'PAM013'],
               ['PAM014', 'A', 'post-amp', 'PAM014'],
               ['PAM015', 'A', 'post-amp', 'PAM015'],
               ['CRF012', 'A', 'cable-rfof', 'orangegray'],
               ['CRF013', 'A', 'cable-rfof', '1/2'],
               ['CRF025', 'A', 'cable-rfof', '3/4'],
               ['CRF026', 'A', 'cable-rfof', '5/6']
]

# List the connections to add and associated time
cstart_time = "10:30"
connections_to_add = [
                     ### HH0
                     [['FDV1', 'A', 'terminals'], ['FEM010', 'A', 'input']],
                     [['FEM010', 'A', 'e'], ['CRF000', 'A', 'ea']],
                     [['FEM010', 'A', 'n'], ['CRF000', 'A', 'na']],
                     [['CRF000', 'A', 'eb'], ['PAM010', 'A', 'ea']],
                     [['CRF000', 'A', 'nb'], ['PAM010', 'A', 'na']],
                     [['PAM010', 'A', 'eb'], ['SNPA000008', 'A', 'e2']],
                     [['PAM010', 'A', 'nb'], ['SNPA000008', 'A', 'n0']],
                     [['PAM010', 'A', '@slot'], ['PCH1', 'A', '@slot01']],
                     ### HH1
                     [['FDV2', 'A', 'terminals'], ['FEM011', 'A', 'input']],
                     [['FEM011', 'A', 'e'], ['CRF001', 'A', 'ea']],
                     [['FEM011', 'A', 'n'], ['CRF001', 'A', 'na']],
                     [['CRF001', 'A', 'eb'], ['PAM011', 'A', 'ea']],
                     [['CRF001', 'A', 'nb'], ['PAM011', 'A', 'na']],
                     [['PAM011', 'A', 'eb'], ['SNPA000008', 'A', 'e6']],
                     [['PAM011', 'A', 'nb'], ['SNPA000008', 'A', 'n4']],
                     [['PAM011', 'A', '@slot'], ['PCH1', 'A', '@slot02']],
                     ### HH12
                     [['FDV3', 'A', 'terminals'], ['FEM012', 'A', 'input']],
                     [['FEM012', 'A', 'e'], ['CRF012', 'A', 'ea']],
                     [['FEM012', 'A', 'n'], ['CRF012', 'A', 'na']],
                     [['CRF012', 'A', 'eb'], ['PAM012', 'A', 'ea']],
                     [['CRF012', 'A', 'nb'], ['PAM012', 'A', 'na']],
                     [['PAM012', 'A', 'eb'], ['SNPA000008', 'A', 'e10']],
                     [['PAM012', 'A', 'nb'], ['SNPA000008', 'A', 'n8']],
                     [['PAM012', 'A', '@slot'], ['PCH1', 'A', '@slot03']],
                     ### HH13
                     [['FDV4', 'A', 'terminals'], ['FEM013', 'A', 'input']],
                     [['FEM013', 'A', 'e'], ['CRF013', 'A', 'ea']],
                     [['FEM013', 'A', 'n'], ['CRF013', 'A', 'na']],
                     [['CRF013', 'A', 'eb'], ['PAM013', 'A', 'ea']],
                     [['CRF013', 'A', 'nb'], ['PAM013', 'A', 'na']],
                     [['PAM013', 'A', 'eb'], ['SNPA000022', 'A', 'e2']],
                     [['PAM013', 'A', 'nb'], ['SNPA000022', 'A', 'n0']],
                     [['PAM013', 'A', '@slot'], ['PCH1', 'A', '@slot04']],
                     ### HH25
                     [['FDV6', 'A', 'terminals'], ['FEM014', 'A', 'input']],
                     [['FEM014', 'A', 'e'], ['CRF025', 'A', 'ea']],
                     [['FEM014', 'A', 'n'], ['CRF025', 'A', 'na']],
                     [['CRF025', 'A', 'eb'], ['PAM014', 'A', 'ea']],
                     [['CRF025', 'A', 'nb'], ['PAM014', 'A', 'na']],
                     [['PAM014', 'A', 'eb'], ['SNPA000022', 'A', 'e10']],
                     [['PAM014', 'A', 'nb'], ['SNPA000022', 'A', 'n8']],
                     [['PAM014', 'A', '@slot'], ['PCH1', 'A', '@slot05']],
                     ### HH26
                     [['FDV7', 'A', 'terminals'], ['FEM015', 'A', 'input']],
                     [['FEM015', 'A', 'e'], ['CRF026', 'A', 'ea']],
                     [['FEM015', 'A', 'n'], ['CRF026', 'A', 'na']],
                     [['CRF026', 'A', 'eb'], ['PAM015', 'A', 'ea']],
                     [['CRF026', 'A', 'nb'], ['PAM015', 'A', 'na']],
                     [['PAM015', 'A', 'eb'], ['SNPA000024', 'A', 'e2']],
                     [['PAM015', 'A', 'nb'], ['SNPA000024', 'A', 'n0']],
                     [['PAM015', 'A', '@slot'], ['PCH1', 'A', '@slot06']],
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
