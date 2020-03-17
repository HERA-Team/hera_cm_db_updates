#! /usr/bin/env python
"""Add Nodes 1 and 2."""
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)

install_date = '2020/02/15'

node = 1
fps = 15
pch = 13
ncm = '13'
pams = [209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220]
snaps = ['C000063', 'C000071', 'C000067', 'C000064']
ser_num = {'node': 'H0030-2601.2#18', 'node-control-module': 'Prod13'}
hera.load_active(cdate=install_date, ctime='09:00')
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate=install_date, ctime=['10:00', '11:00'],
              ser_num=ser_num, override=False)

node = 2
fps = 14
pch = 14
ncm = '14'
pams = [197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208]
snaps = ['C000066', 'C000074', 'C000079', 'C000081']
ser_num = {'node': 'H0030-2601.2#19', 'node-control-module': 'Prod14'}
hera.load_active(cdate=install_date, ctime='09:00')
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate=install_date, ctime=['10:00', '11:00'],
              ser_num=ser_num, override=False)

hera.done()
