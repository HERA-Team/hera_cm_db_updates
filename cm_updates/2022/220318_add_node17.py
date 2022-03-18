#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)

nodes = [17]
ncms = [22]
fpss = [23]
pchs = [23]
pams = [293]
snaps = [[87, 52, 34, 27]]
cdate = '2022/03/18'

for node, ncm, fps, pch, start_pam, snap in zip(nodes, ncms, fpss, pchs, pams, snaps):
    pam = list(range(start_pam, start_pam+12))
    hera.add_node(node, fps, pch, ncm, pam, snap, cdate=cdate, ctime='10:00', override=True)

hera.done()
