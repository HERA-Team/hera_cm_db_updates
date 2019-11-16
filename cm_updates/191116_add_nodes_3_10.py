#! /usr/bin/env python
import sys
sys.path.insert(1, '../hera_cm')
import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)

node = 3
fps = 9
pch = 7
ncm = 'Pro5'
pams = [125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136]
snaps = ['C000001', 'C000002', 'C000037', 'C000054']
ser_num = {'node': 'H0030-2601.2#7'}
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate='2019/11/13', ctime=['10:00', '11:00'], ser_num=ser_num, override=False)

node = 10
fps = 8
pch = 8
ncm = 'Pro6'
pams = [137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148]
snaps = ['C000014', 'C000016', 'C000042', 'C000045']
ser_num = {'node': 'H0030-2601.2#6'}
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate='2019/11/13', ctime=['10:00', '11:00'], ser_num=ser_num, override=False)

hera.done()
