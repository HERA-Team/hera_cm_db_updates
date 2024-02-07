#! /usr/bin/env python
from hera_cm import ant_node_grid
import argparse



ap = argparse.ArgumentParser()
ap.add_argument('highlight', help="List of antennas to highlight or yaml file.", nargs='?', default=None)
ap.add_argument('-n', '--number', help="Number to show as screen text.", type=int, default=7)
ap.add_argument('-x', '--noplot', help="Flag to turn off the plot.", action='store_true')
args = ap.parse_args()

if args.noplot:
    args.number = True  # Show them all

grid = ant_node_grid.Grid(args.highlight)
print("Making grid...")
grid.get_connected()
grid.process_highlight(show_highlighted=args.number)
if not args.noplot:
    grid.addplot('Node Grid/Antenna Map')
    ant_node_grid.plt.show()