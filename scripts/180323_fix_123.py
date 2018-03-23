#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Updates addressing HERA_Commissioning issue #109")

log_file = 'scripts.log'
do_it_this_time = True

fems_to_add = ['75067']
pams_to_add = ['75157']
connections_to_stop = [
                      [['FDA24', 'B', 'terminals'], ['FEA24', 'A', 'input']],
                      [['FEA24', 'A', 'e'], ['C7F123', 'A', 'ea']],
                      [['FEA24', 'A', 'n'], ['C7F123', 'A', 'na']],
                      [['C7F123', 'A', 'eb'], ['RI4B4E', 'A', 'a']],
                      [['C7F123', 'A', 'nb'], ['RI4B4N', 'A', 'a']]
]
connections_to_add = [
                     [['FDA24', 'B', 'terminals'], ['FEM75067', 'A', 'input']],
                     [['FEM75067', 'A', 'e'], ['C7F123', 'A', 'ea']],
                     [['FEM75067', 'A', 'n'], ['C7F123', 'A', 'na']],
                     [['C7F123', 'A', 'eb'], ['RI2A8E', 'A', 'a']],
                     [['C7F123', 'A', 'nb'], ['RI2A8N', 'A', 'a']],
                     [['RI2A8E', 'A', 'b'], ['PAM75157', 'B', 'ea']],
                     [['RI2A8N', 'A', 'b'], ['PAM75157', 'B', 'na']],
                     [['PAM75157', 'B', 'eb'], ['RO2A8E', 'A', 'a']],
                     [['PAM75157', 'B', 'nb'], ['RO2A8N', 'A', 'a']]
]

fp = pc.init_script(sys.argv, log_file)

# Add FEM/PAM to parts
cdate = '2018/03/21'
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

# Stop then update old connections per issue 109
cdate = '2018/03/21'
ctime = '11:00'
for c in connections_to_stop:
    fp.write(pc.connect('stop', c[0], c[1], cdate, ctime, do_it_this_time))
ctime = '12:00'
for c in connections_to_add:
    fp.write(pc.connect('add', c[0], c[1], cdate, ctime, do_it_this_time))

fp.close()
