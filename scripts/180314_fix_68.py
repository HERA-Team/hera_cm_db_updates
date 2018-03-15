#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Updates addressing HERA_Commissioning issue #92")

log_file = 'scripts.log'
do_it_this_time = True

fems_to_add = []
pams_to_add = ['75158']
connections_to_stop = [
                      [['C7F68', 'A', 'eb'], ['RI5A6E', 'A', 'a']],
                      [['C7F68', 'A', 'nb'], ['RI5A6N', 'A', 'a']]
]
connections_to_add = [
                     [['C7F68', 'A', 'eb'], ['RI2A7E', 'A', 'a']],
                     [['C7F68', 'A', 'nb'], ['RI2A7N', 'A', 'a']],
                     [['RI2A7E', 'A', 'b'], ['PAM75158', 'B', 'ea']],
                     [['RI2A7N', 'A', 'b'], ['PAM75158', 'B', 'na']],
                     [['PAM75158', 'B', 'eb'], ['RO2A7E', 'A', 'a']],
                     [['PAM75158', 'B', 'nb'], ['RO2A7N', 'A', 'a']]
]

fp = pc.init_script(sys.argv, log_file)

# Add FEM/PAM to parts
cdate = '2018/03/13'
ctime = '10:00'
for f in fems_to_add:
    hpn = 'FEM' + f
    rev = 'A'
    htype = 'front-end'
    serno = f
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))
for p in pams_to_add:
    hpn = 'PAM' + p
    rev = 'B'
    htype = 'post-amp'
    serno = p
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))

# Stop then update old connections per issue 102
cdate = '2018/03/13'
ctime = '11:00'
for c in connections_to_stop:
    fp.write(pc.connect('stop', c[0], c[1], cdate, ctime, do_it_this_time))
ctime = '12:00'
for c in connections_to_add:
    fp.write(pc.connect('add', c[0], c[1], cdate, ctime, do_it_this_time))

fp.close()
