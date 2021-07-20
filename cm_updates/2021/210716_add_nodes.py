#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)

# Node 18
# NCM 12
# FPS 20
# Snap 0 - A000022
# Snap 1 - C000065
# Snap 2 - C000083
# Snap 3 - C000068
#
# Node 19
# NCM 18
# FPS 17
# Snap 0 - C000078
# Snap 1 - C000008
# Snap 2 - C000061
# Snap 3 - C000025
#
# Node 20
# NCM 15
# FPS 19
# Snap 0 - C000070
# Snap 1 - C000085
# Snap 2 - C000085
# Snap 3 - C000086

# Part ('NCM12', 'A', 'node-control-module', 'NCM12') is already added
# Part ('N18', 'A', 'node', 'N18') is already added
# Part ('NCM18', 'A', 'node-control-module', 'NCM18') is already added
# Part ('N19', 'A', 'node', 'N19') is already added
# Part ('NCM15', 'A', 'node-control-module', 'NCM15') is already added
# Part ('N20', 'A', 'node', 'N20') is already added

nodes = [6, 11, 16]
ncms = [16, 20, 11]
fpss = [21, 18, 22]
pchs = [18, 19, 20]
pams = [269, 245, 281]
snaps = [[95, 36, 84, 100],
         [59, 93, 26, 89],
         [12, 90, 101, 120]]
cdate = '2021/07/01'

for node, ncm, fps, pch, start_pam, snap in zip(nodes, ncms, fpss, pchs, pams, snaps):
    pam = list(range(start_pam, start_pam+12))
    hera.add_node(node, fps, pch, ncm, pam, snap, cdate=cdate, ctime='10:00', override=True)

hera.done()
