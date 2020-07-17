#! /usr/bin/env python
"""Add antennas."""
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)

stns = [312]
sers = [319]
cdates = ['2020/07/17']

for stn, sn, cd in zip(stns, sers, cdates):
    hera.add_antenna_station(stn, sn, cd)

hera.done()
