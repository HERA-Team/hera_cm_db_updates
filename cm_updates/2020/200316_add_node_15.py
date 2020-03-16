#! /usr/bin/env python
"""Add Node 15."""
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)

install_date = '2020/01/28'
node = 15
fps = 13
pch = 12
ncm = 'Prod9'
pams = [185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196]
snaps = ['C000006', 'C000024', 'C000009', 'C000076']
ser_num = {'node': 'H0030-2601.2#15'}
hera.load_active(cdate=install_date, ctime='09:00')
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate=install_date, ctime=['10:00', '11:00'],
              ser_num=ser_num, override=False)

hera.done()
