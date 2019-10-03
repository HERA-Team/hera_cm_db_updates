#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to start/stop parts/connections
connections_to_stop = [
                      [['PAM047', 'A', 'nb'], ['SNPA000024', 'A', 'n4'], '2019/05/12', '11:30']
]
connections_to_add = [
                     [['PAM047', 'A', 'nb'], ['SNPA000024', 'A', 'n0'], '2019/05/12', '11:30']
]

for up, down, cdate, ctime in connections_to_stop:
    hera.update_connection('stop', up, down, cdate, ctime)

for up, down, cdate, ctime in connections_to_add:
    hera.update_connection('add', up, down, cdate, ctime)

hera.done()
