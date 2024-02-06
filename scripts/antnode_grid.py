#! /usr/bin/env python
from hera_cm import ant_node_grid
import argparse



ap = argparse.ArgumentParser()
ap.add_argument('highlight', help="List of antennas to highlight or yaml file", nargs='?', default=None)
args = ap.parse_args()

grid = ant_node_grid.Grid(args.highlight)
print("Making grid...")
grid.get_connected()
grid.process_highlight(show_highlighted=7)
grid.addplot('Node Grid/Antenna Map')
ant_node_grid.plt.show()