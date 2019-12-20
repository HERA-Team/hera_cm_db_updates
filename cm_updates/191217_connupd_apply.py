#! /usr/bin/env python
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)
"""
update_part
    add_or_stop:  'add' or 'stop'
    part:  [hpn, rev, <type>, <mfg num>] (last two only for 'add')
    cdate:  date of update YYYY/MM/DD
    ctime:  time of update HH:MM
update_connection
    add_or_stop:  'add' or 'stop'
    up:  upstream connection [part, rev, port]
    down:  downstream connection [part, rev, port]
    cdate:  date of update YYYY/MM/DD
    ctime:  time of update HH:MM
"""

# Antenna 50
connections_to_stop = [[['FDV85', 'A', 'terminals'], ['FEM129', 'A', 'input'],
                        '2019/12/12', '10:00'],
                       [['FEM129', 'A', 'e'], ['NBP03', 'A', 'e10'],
                        '2019/12/12', '10:00'],
                       [['FEM129', 'A', 'n'], ['NBP03', 'A', 'n10'],
                        '2019/12/12', '10:00'],
                       ]
for conn in connections_to_stop:
    hera.update_connection('stop', conn[0], conn[1], conn[2], conn[3])

parts_to_add = []
for part in parts_to_add:
    hera.update_part('add', part[0], part[1], part[2])

connections_to_start = []
for conn in connections_to_start:
    hera.update_connection('add', conn[0], conn[1], conn[2], conn[3])

hera.done()
