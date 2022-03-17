#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)

nodes = [21]
ncms = [4]
fpss = [24]
pchs = [22]
pams = [305]
snaps = [[99, 127, 98, 117]]
cdate = '2022/03/17'

for node, ncm, fps, pch, start_pam, snap in zip(nodes, ncms, fpss, pchs, pams, snaps):
    pam = list(range(start_pam, start_pam+12))
    hera.add_node(node, fps, pch, ncm, pam, snap, cdate=cdate, ctime='10:00', override=True)

hera.done()
