#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Set up a node")

log_file = 'scripts.log'
do_it_this_time = True

node = 'ND0'

parts_to_add = {'N0': ['A', 'node', 'N0', '@ground>ND0:A:@ground'],
                'PCH1': ['A', 'pam-chassis', 'PCH1', '@rack>N0:A:@loc0'],
                'PAM75191': ['A', 'post-amp', 'PAM75191', '@slot>PCH1:A:@slot07'],
                'PAM75192': ['A', 'post-amp', 'PAM75192', '@slot>PCH1:A:@slot01'],
                'PAM75193': ['A', 'post-amp', 'PAM75193', '@slot>PCH1:A:@slot02'],
                'PAM75194': ['A', 'post-amp', 'PAM75194', '@slot>PCH1:A:@slot03'],
                'PAM75195': ['A', 'post-amp', 'PAM75195', '@slot>PCH1:A:@slot05'],
                'PAM75196': ['A', 'post-amp', 'PAM75196', '@slot>PCH1:A:@slot06'],
                'SNP008': ['A', 'snap', 'SNP008', 'rack>N0:A:loc1'],
                'SNP024': ['A', 'snap', 'SNP024', 'rack>N0:A:loc2'],
                'SNP023': ['A', 'snap', 'SNP023', 'rack>N0:A:loc3'],
                'NCM1': ['A', 'node-control-module', 'NCM1', '@rack>N0:A:@loc5'],
                'FPS1': ['A', 'fem-power-supply', 'FPS1', '@rack>N0:A:@loc6']}

fp = pc.init_script(sys.argv, log_file)


def add_part(hpn, rev, htype, serno, cdate, ctime, do_it_this_time):
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))


def add_connection(upart, urev, uport, dpart, drev, dport, cdate, ctime, do_it_this_time):
    up = [upart, urev, uport]
    down = [dpart, drev, dport]
    fp.write(pc.connect('add', up, down, cdate, ctime, do_it_this_time))


cdate = '2018/07/18'
ctime = '10:00'
fp.write('add_station.py {} --date {} --time {}\n'.format(node, cdate, ctime))

ctime = '11:00'
for p, d in parts_to_add.iteritems():
    add_part(p, d[0], d[1], d[2], cdate, ctime, do_it_this_time)

ctime = '12:00'
for p, d in parts_to_add.iteritems():
    upart = p
    urev = d[0]
    uport = d[3].split('>')[0]
    dpart = d[3].split('>')[1].split(':')[0]
    drev = d[3].split('>')[1].split(':')[1]
    dport = d[3].split('>')[1].split(':')[2]
    add_connection(upart, urev, uport, dpart, drev, dport, cdate, ctime, do_it_this_time)

fp.close()
