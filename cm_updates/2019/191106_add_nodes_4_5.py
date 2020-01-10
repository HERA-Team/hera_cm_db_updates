#! /usr/bin/env python
import sys
sys.path.insert(1, '../hera_cm')
import signal_chain
hera = signal_chain.Update(sys.argv[0])

node = 4
fps = 6
pch = 5
ncm = 'Pro3'
pams = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]
snaps = ['C000022', 'C000003', 'C000048', 'C000040']
ser_num = {'node': 4}
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate='2019/10/31', ctime=['10:00', '11:00'], ser_num=ser_num, override=False)

node = 5
fps = 7
pch = 6
ncm = 'Pro4'
pams = [113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124]
snaps = ['C000058', 'C000050', 'C000032', 'C000018']
ser_num = {'node': 5}
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate='2019/10/31', ctime=['10:00', '11:00'], ser_num=ser_num, override=False)

hera.done()
