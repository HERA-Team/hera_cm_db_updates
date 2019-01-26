#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Updates to disconnect the NRAO RCVRs in R2")

log_file = 'scripts.log'
do_it_this_time = True

connections_to_stop = [
                      [['RI2A1E', 'A', 'b'], ['RCVR5', 'A', 'ea']],
                      [['RI2A1N', 'A', 'b'], ['RCVR5', 'A', 'na']],
                      [['RI2A2E', 'A', 'b'], ['RCVR6', 'A', 'ea']],
                      [['RI2A2N', 'A', 'b'], ['RCVR6', 'A', 'na']],
                      [['RI2A3E', 'A', 'b'], ['RCVR82', 'A', 'ea']],
                      [['RI2A3N', 'A', 'b'], ['RCVR82', 'A', 'na']],
                      [['RI2A4E', 'A', 'b'], ['RCVR70', 'A', 'ea']],
                      [['RI2A4N', 'A', 'b'], ['RCVR70', 'A', 'na']],
                      [['RI2A5E', 'A', 'b'], ['RCVR87', 'A', 'ea']],
                      [['RI2A5N', 'A', 'b'], ['RCVR87', 'A', 'na']],
                      [['RI2A6E', 'A', 'b'], ['RCVR100', 'A', 'ea']],
                      [['RI2A6N', 'A', 'b'], ['RCVR100', 'A', 'na']],
                      [['RI2A7E', 'A', 'b'], ['RCVR11', 'A', 'ea']],
                      [['RI2A7N', 'A', 'b'], ['RCVR11', 'A', 'na']],
                      [['RI2A8E', 'A', 'b'], ['RCVR13', 'A', 'ea']],
                      [['RI2A8N', 'A', 'b'], ['RCVR13', 'A', 'na']],
                      [['RI2B1E', 'A', 'b'], ['RCVR15', 'A', 'ea']],
                      [['RI2B1N', 'A', 'b'], ['RCVR15', 'A', 'na']],
                      [['RI2B2E', 'A', 'b'], ['RCVR71', 'A', 'ea']],
                      [['RI2B2N', 'A', 'b'], ['RCVR71', 'A', 'na']],
                      [['RI2B3E', 'A', 'b'], ['RCVR8', 'A', 'ea']],
                      [['RI2B3N', 'A', 'b'], ['RCVR8', 'A', 'na']],
                      [['RI2B4E', 'A', 'b'], ['RCVR108', 'A', 'ea']],
                      [['RI2B4N', 'A', 'b'], ['RCVR108', 'A', 'na']],
                      [['RI2B5E', 'A', 'b'], ['RCVR53', 'A', 'ea']],
                      [['RI2B5N', 'A', 'b'], ['RCVR53', 'A', 'na']],
                      [['RI2B6E', 'A', 'b'], ['RCVR49', 'A', 'ea']],
                      [['RI2B6N', 'A', 'b'], ['RCVR49', 'A', 'na']],
                      [['RI2B7E', 'A', 'b'], ['RCVR37', 'A', 'ea']],
                      [['RI2B7N', 'A', 'b'], ['RCVR37', 'A', 'na']],
                      [['RI2B8E', 'A', 'b'], ['RCVR3', 'A', 'ea']],
                      [['RI2B8N', 'A', 'b'], ['RCVR3', 'A', 'na']],
]

fp = pc.init_script(sys.argv, log_file)

cdate = '2018/01/20'
ctime = '10:00'

for c in connections_to_stop:
    fp.write(pc.connect('stop', c[0], c[1], cdate, ctime, do_it_this_time))

fp.close()
