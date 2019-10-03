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
]

# List the parts to stop and associated time (last two per entry are ignored)
pstop_time = "10:10"
parts_to_stop = [
]

# List the parts to add and associated time
pstart_time = "10:20"
parts_to_add = [
               ['TMPCBL', 'A', 'temp-cable', 'x']
]

# List the connections to add and associated time
cstart_time = "10:30"
connections_to_add = [
                     [['FDV5', 'A', 'terminals'], ['TMPCBL', 'A', 'ea']],
                     [['TMPCBL', 'A', 'eb'], ['SNPA000024', 'A', 'e6']],
                     [['FDV5', 'A', 'terminals'], ['TMPCBL', 'A', 'na']],
                     [['TMPCBL', 'A', 'nb'], ['SNPA000024', 'A', 'n4']]
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
