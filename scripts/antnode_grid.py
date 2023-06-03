#! /usr/bin/env python
from hera_cm import ant_node_grid
import argparse



ap = argparse.ArgumentParser()
ap.add_argument('-a', '--antenna', help="List of antennas to highnmclr", default='')
ap.add_argument('--highlight-color', dest='highlight_color', help="Color to use to highlight above", default='r')
args = ap.parse_args()
args.antenna = args.antenna.split(',')
ant_node_grid.grid(args.antenna, args.highlight_color)