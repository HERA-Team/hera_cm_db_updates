#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Updates addressing HERA_Commissioning issue #102")

log_file = 'scripts.log'
do_it_this_time = True

fems_to_add = ['75066']
pams_to_add = ['75159']
connections_to_stop = [
                      [['FDA5', 'B', 'terminals'], ['FEA5', 'A', 'input']],
                      [['FEA5', 'A', 'e'], ['C7F65', 'A', 'ea']],
                      [['FEA5', 'A', 'n'], ['C7F65', 'A', 'na']],
                      [['C7F65', 'A', 'eb'], ['RI4A4E', 'A', 'a']],
                      [['C7F65', 'A', 'nb'], ['RI4A4N', 'A', 'a']]
]
connections_to_add = [
                     [['FDA5', 'B', 'terminals'], ['FEM75066', 'A', 'input']],
                     [['FEM75066', 'A', 'e'], ['C7F65', 'A', 'ea']],
                     [['FEM75066', 'A', 'n'], ['C7F65', 'A', 'na']],
                     [['C7F65', 'A', 'eb'], ['RI2A6E', 'A', 'a']],
                     [['C7F65', 'A', 'nb'], ['RI2A6N', 'A', 'a']],
                     [['RI2A6E', 'A', 'b'], ['PAM75159', 'B', 'ea']],
                     [['RI2A6N', 'A', 'b'], ['PAM75159', 'B', 'na']],
                     [['PAM75159', 'B', 'eb'], ['RO2A6E', 'A', 'a']],
                     [['PAM75159', 'B', 'nb'], ['RO2A6N', 'A', 'a']]
]

fp = pc.init_script(sys.argv, log_file)

# Add FEM/PAM to parts
cdate = '2018/02/21'
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
cdate = '2018/02/21'
ctime = '11:00'
for c in connections_to_stop:
    fp.write(pc.connect('stop', c[0], c[1], cdate, ctime, do_it_this_time))
ctime = '12:00'
for c in connections_to_add:
    fp.write(pc.connect('add', c[0], c[1], cdate, ctime, do_it_this_time))

fp.close()
