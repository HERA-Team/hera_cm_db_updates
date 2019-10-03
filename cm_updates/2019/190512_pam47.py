#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to start/stop parts/connections
connections_to_stop = [
                      [['PAM028', 'A', '@slot'], ['PCH010', 'A', '@slot07'], '2019/03/01', '11:00']
]
parts_to_add = [
               [['PAM047', 'A', 'post-amp', '047'], '2019/05/12', '10:00']
]
connections_to_add = [
                     [['PAM047', 'A', '@slot'], ['PCH010', 'A', '@slot07'], '2019/05/12', '10:30'],
                     [['CRF014', 'A', 'eb'], ['PAM047', 'A', 'ea'], '2019/05/12', '11:00'],
                     [['CRF014', 'A', 'nb'], ['PAM047', 'A', 'na'], '2019/05/12', '11:00'],
                     [['PAM047', 'A', 'eb'], ['SNPA000024', 'A', 'e2'], '2019/05/12', '11:30'],
                     [['PAM047', 'A', 'nb'], ['SNPA000024', 'A', 'n4'], '2019/05/12', '11:30']
]

for up, down, cdate, ctime in connections_to_stop:
    hera.update_connection('stop', up, down, cdate, ctime)

for part, cdate, ctime in parts_to_add:
    hera.update_part('add', part, cdate, ctime)

for up, down, cdate, ctime in connections_to_add:
    hera.update_connection('add', up, down, cdate, ctime)

hera.done()
