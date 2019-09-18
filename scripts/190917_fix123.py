#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0])

parts_to_add = []

connections_to_add = [
                     [['A123', 'H', 'focus'], ['FDV45', 'A', 'input'], '2019/08/07', '12:30'],  # 88
]

for part, cdate, ctime in parts_to_add:
    hera.update_part('add', part, cdate, ctime)

for up, down, cdate, ctime in connections_to_add:
    hera.update_connection('stop', up, down, cdate, ctime)


hera.done()
