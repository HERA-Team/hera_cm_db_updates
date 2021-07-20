#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)


ants = [320, 321, 324, 325, 322, 323, 326, 327, 328]
snrs = [324, 325, 326, 327, 328, 329, 330, 331, 332]
cdates = ['2021/05/11', '2021/05/11', '2021/05/11', '2021/05/11', '2021/05/12',
          '2021/05/13', '2021/05/13', '2021/05/13', '2021/05/13']

for i in range(len(ants)):
    hera.add_antenna_station(ants[i], snrs[i], cdates[i])

hera.done()
