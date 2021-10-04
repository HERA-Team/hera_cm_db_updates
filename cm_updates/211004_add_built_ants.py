#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)


ants = [331, 332, 335, 336, 339, 340]
snrs = [333, 334, 335, 336, 337, 338]
cdates = ['2021/09/27', '2021/09/23', '2021/09/23', '2021/09/29', '2021/09/28', '2021/09/27']

for i in range(len(ants)):
    hera.add_antenna_station(ants[i], snrs[i], cdates[i])

hera.done()
