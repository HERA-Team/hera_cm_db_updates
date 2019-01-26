#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Updates addressing HERA_Commissioning issues #92 and #99")

log_file = 'scripts.log'
do_it_this_time = True

sigch_to_add = [
               ['CC2R5C8', 'A', '"cable-container"', 'CBLC2R5C8'],
               ['CC2R6C8', 'A', '"cable-container"', 'CBLC2R6C8']
]
conns_to_add = [
               [['CR3B8E', 'A', 'b'], ['CC2R5C8', 'A', 'a']],
               [['CR3B8N', 'A', 'b'], ['CC2R6C8', 'A', 'a']],
               [['CC2R5C8', 'A', 'b'], ['DF1C4', 'A', 'input']],
               [['CC2R6C8', 'A', 'b'], ['DF1C3', 'A', 'input']]
]
cdate = '2017/10/01'
ctime = '10:00'
fp = pc.init_script(sys.argv, log_file)
for s in sigch_to_add:
    fp.write(pc.part('add', s, cdate, ctime, do_it_this_time))
for c in conns_to_add:
    fp.write(pc.connect('add', c[0], c[1], cdate, ctime, do_it_this_time))

fp.close()
