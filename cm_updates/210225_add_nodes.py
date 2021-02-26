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

nodes = [18, 19, 20]
ncms = [12, 18, 15]
fpss = [20, 17, 19]
pchs = [15, 16, 17]
pams = [[700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711],
        [720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731],
        [740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751]]
snaps = [['A00002', 65, 83, 68],
         [78, 8, 61, 25],
         [70, 85, 85, 86]]
cdate = '2021/02/25'

for node, ncm, fps, pch, pam, snap in zip(nodes, ncms, fpss, pchs, pams, snaps):
    hera.add_node(node, fps, pch, ncm, pam, snap, cdate=cdate, ctime='10:00', override=True)

hera.done()
