#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Updates to disconnect the other side of the NRAO RCVRs in R2")

log_file = 'scripts.log'
do_it_this_time = True

connections_to_stop = [
                      [['RCVR5', 'A', 'eb'], ['RO2A1E', 'A', 'a']],
                      [['RCVR5', 'A', 'nb'], ['RO2A1N', 'A', 'a']],
                      [['RCVR6', 'A', 'eb'], ['RO2A2E', 'A', 'a']],
                      [['RCVR6', 'A', 'nb'], ['RO2A2N', 'A', 'a']],
                      [['RCVR82', 'A', 'eb'], ['RO2A3E', 'A', 'a']],
                      [['RCVR82', 'A', 'nb'], ['RO2A3N', 'A', 'a']],
                      [['RCVR70', 'A', 'eb'], ['RO2A4E', 'A', 'a']],
                      [['RCVR70', 'A', 'nb'], ['RO2A4N', 'A', 'a']],
                      [['RCVR87', 'A', 'eb'], ['RO2A5E', 'A', 'a']],
                      [['RCVR87', 'A', 'nb'], ['RO2A5N', 'A', 'a']],
                      [['RCVR100', 'A', 'eb'], ['RO2A6E', 'A', 'a']],
                      [['RCVR100', 'A', 'nb'], ['RO2A6N', 'A', 'a']],
                      [['RCVR11', 'A', 'eb'], ['RO2A7E', 'A', 'a']],
                      [['RCVR11', 'A', 'nb'], ['RO2A7N', 'A', 'a']],
                      [['RCVR13', 'A', 'eb'], ['RO2A8E', 'A', 'a']],
                      [['RCVR13', 'A', 'nb'], ['RO2A8N', 'A', 'a']],
                      [['RCVR15', 'A', 'eb'], ['RO2B1E', 'A', 'a']],
                      [['RCVR15', 'A', 'nb'], ['RO2B1N', 'A', 'a']],
                      [['RCVR71', 'A', 'eb'], ['RO2B2E', 'A', 'a']],
                      [['RCVR71', 'A', 'nb'], ['RO2B2N', 'A', 'a']],
                      [['RCVR8', 'A', 'eb'], ['RO2B3E', 'A', 'a']],
                      [['RCVR8', 'A', 'nb'], ['RO2B3N', 'A', 'a']],
                      [['RCVR108', 'A', 'eb'], ['RO2B4E', 'A', 'a']],
                      [['RCVR108', 'A', 'nb'], ['RO2B4N', 'A', 'a']],
                      [['RCVR53', 'A', 'eb'], ['RO2B5E', 'A', 'a']],
                      [['RCVR53', 'A', 'nb'], ['RO2B5N', 'A', 'a']],
                      [['RCVR49', 'A', 'eb'], ['RO2B6E', 'A', 'a']],
                      [['RCVR49', 'A', 'nb'], ['RO2B6N', 'A', 'a']],
                      [['RCVR37', 'A', 'eb'], ['RO2B7E', 'A', 'a']],
                      [['RCVR37', 'A', 'nb'], ['RO2B7N', 'A', 'a']],
                      [['RCVR3', 'A', 'eb'], ['RO2B8E', 'A', 'a']],
                      [['RCVR3', 'A', 'nb'], ['RO2B8N', 'A', 'a']]
]

fp = pc.init_script(sys.argv, log_file)

cdate = '2018/01/20'
ctime = '10:00'

for c in connections_to_stop:
    fp.write(pc.connect('stop', c[0], c[1], cdate, ctime, do_it_this_time))

fp.close()
