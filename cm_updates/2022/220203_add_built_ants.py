#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)


ants = [329, 333, 337, 341, 342, 343, 344, 345, 346, 347, 348, 349]
snrs = [339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350]
cdates = ['2022/01/24', '2022/01/24', '2022/01/24', '2022/01/24', '2022/01/25', '2022/01/24',
          '2022/01/24', '2022/01/24', '2022/01/25', '2022/01/25', '2022/01/25', '2022/01/25']

for i in range(len(ants)):
    hera.add_antenna_station(ants[i], snrs[i], cdates[i])

hera.done()
