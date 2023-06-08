#! /usr/bin/env python
from hera_cm import ant_node_grid
import argparse



ap = argparse.ArgumentParser()
ap.add_argument('-a', '--antenna', help="List of antennas to highlight", default='')
args = ap.parse_args()

data = {}
if len(args.antenna):
    data['antennas'] = {}
    for ant in args.antenna.split(','):
        data['antennas'][int(ant)] = 'r'

grid = ant_node_grid.Grid(data)
print("Making...")
grid.make()
if False:
    print("\nChecking...")
    grid.check()
grid.addplot('Node Grid/Antenna Map')
ant_node_grid.plt.show()