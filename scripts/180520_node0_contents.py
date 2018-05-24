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
                'PAM01': ['A', 'post-amp', 'PAM1', '@slot>PCH1:A:@slot01'],
                'PAM02': ['A', 'post-amp', 'PAM2', '@slot>PCH1:A:@slot02'],
                'PAM03': ['A', 'post-amp', 'PAM3', '@slot>PCH1:A:@slot03'],
                'PAM04': ['A', 'post-amp', 'PAM4', '@slot>PCH1:A:@slot04'],
                'PAM05': ['A', 'post-amp', 'PAM5', '@slot>PCH1:A:@slot05'],
                'PAM06': ['A', 'post-amp', 'PAM6', '@slot>PCH1:A:@slot06'],
                'PAM07': ['A', 'post-amp', 'PAM7', '@slot>PCH1:A:@slot07'],
                'PAM08': ['A', 'post-amp', 'PAM8', '@slot>PCH1:A:@slot08'],
                'PAM09': ['A', 'post-amp', 'PAM9', '@slot>PCH1:A:@slot09'],
                'PAM10': ['A', 'post-amp', 'PAM10', '@slot>PCH1:A:@slot10'],
                'PAM11': ['A', 'post-amp', 'PAM11', '@slot>PCH1:A:@slot11'],
                'PAM12': ['A', 'post-amp', 'PAM12', '@slot>PCH1:A:@slot12'],
                'SNP1': ['A', 'snap', 'SNP1', 'rack>N0:A:loc1'],
                'SNP2': ['A', 'snap', 'SNP2', 'rack>N0:A:loc2'],
                'SNP3': ['A', 'snap', 'SNP3', 'rack>N0:A:loc3'],
                'SNP4': ['A', 'snap', 'SNP4', 'rack>N0:A:loc4'],
                'PCM1': ['A', 'power-control-module', 'PCM1', '@rack>N0:A:@loc5'],
                'FPS1': ['A', 'fem-power-supply', 'FPS1', '@rack>N0:A:@loc6']}

fp = pc.init_script(sys.argv, log_file)


def add_part(hpn, rev, htype, serno, cdate, ctime, do_it_this_time):
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))


def add_connection(upart, urev, uport, dpart, drev, dport, cdate, ctime, do_it_this_time):
    up = [upart, urev, uport]
    down = [dpart, drev, dport]
    fp.write(pc.connect('add', up, down, cdate, ctime, do_it_this_time))


cdate = '2018/05/20'
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
