#! /usr/bin/env python
"""Add antennas."""
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)

stns = [262, 248, 230, 231, 212, 192, 193, 195, 173, 275, 315, 316, 313, 314]
sers = [305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318]
cdates = ['2019/12/03', '2019/10/25', '2019/10/23', '2019/10/24', '2019/10/23',
          '2019/10/21', '2019/10/22', '2019/10/22', '2019/10/22', '2019/12/03',
          '2020/07/15', '2020/07/15', '2020/07/15', '2020/07/15']

for stn, sn, cd in zip(stns, sers, cdates):
    hera.add_antenna_station(stn, sn, cd)

hera.done()
