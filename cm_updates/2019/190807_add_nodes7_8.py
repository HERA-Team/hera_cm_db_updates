#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0])

node = 7
fps = 5
pch = 4
ncm = 'Pre2'
pams = [53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 49]
snaps = ['C000019', 'C000021', 'C000030', 'C000031']
ser_num = {'node': 3}
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate='2019/08/02', ctime=['10:00', '11:00'], ser_num=ser_num, override=False)

node = 8
fps = 4
pch = 3
ncm = 'Pro1'
pams = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
snaps = ['C000023', 'C000044', 'C000055', 'C000056']
ser_num = {'node': 2}
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate='2019/08/02', ctime=['10:00', '11:00'], ser_num=ser_num, override=False)

hera.done()
