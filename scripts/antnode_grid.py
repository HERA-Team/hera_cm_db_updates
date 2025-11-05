#! /usr/bin/env python
from hera_cm import ant_node_grid
import argparse



ap = argparse.ArgumentParser()
ap.add_argument('highlight', help="List of antennas to highlight or yaml file.", nargs='?', default=None)
ap.add_argument('-x', '--noplot', help="Flag to turn off the plot.", action='store_true')
ap.add_argument('-v', '--view', help="View all entries.", action='store_true')
ap.add_argument('-d', '--disabled_nodes', help="csv of disabled nodes.", default='0')
ap.add_argument('--verbose', help="Turn on verbose output.", action='store_true')
ap.add_argument('-i', '--ignore_status', help="Ignore status colors when setting display colors.", action='store_true')
ap.add_argument('-x', '--ignore_reassign', help="Ignore reassigned antenna color", action='store_true')
args = ap.parse_args()

disabled_nodes = args.disabled_nodes.split(",")
grid = ant_node_grid.Grid(args.highlight, disabled_nodes=disabled_nodes)
grid.get_connected()
grid.process_array(verbose=args.verbose)
grid.set_display_color(args.ignore_status)
if not args.noplot:
    grid.addplot('Node Grid/Antenna Map')
    ant_node_grid.plt.show()
if args.view:
    grid.print_all()