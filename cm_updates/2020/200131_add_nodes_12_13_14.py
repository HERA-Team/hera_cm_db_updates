#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)

node = 12
fps = 10
pch = 9
ncm = 'Prod7'
pams = [149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160]
snaps = ['C000049', 'C000060', 'C000020', 'C000017']
ser_num = {'node': 'H0030-2601.2#4'}
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate='2020/01/31', ctime=['10:00', '11:00'],
              ser_num=ser_num, override={'date': None})

node = 13
fps = 11
pch = 10
ncm = 'Prod8'
pams = [161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172]
snaps = ['C000035', 'C000029', 'C000015', 'C000047']
ser_num = {'node': 'H0030-2601.2#13'}
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate='2020/01/31', ctime=['10:00', '11:00'],
              ser_num=ser_num, override={'date': None})

node = 14
fps = 12
pch = 11
ncm = 'Prod10'
pams = [173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184]
snaps = ['C000051', 'C000043', 'C000028', 'C000038']
ser_num = {'node': 'H0030-2601.2#14'}
hera.add_node(node, fps, pch, ncm, pams, snaps, cdate='2020/01/31', ctime=['10:00', '11:00'],
              ser_num=ser_num, override={'date': None})

# node = 15
# fps = 13
# pch = 12
# ncm = 'Prod9'
# pams = []
# snaps = ['C000014', 'C000016', 'C000042', 'C000045']
# ser_num = {'node': 'H0030-2601.2#15'}
# hera.add_node(node, fps, pch, ncm, pams, snaps, cdate='2020/01/28', ctime=['10:00', '11:00'],
#               ser_num=ser_num, override=False)

hera.done()
