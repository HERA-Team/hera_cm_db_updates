#! /usr/bin/env python
from hera_cm import ant_node_grid
import argparse



ap = argparse.ArgumentParser()
ap.add_argument('highlight', help="List of antennas to highlight or yaml file.", nargs='?', default=None)
ap.add_argument('-x', '--noplot', help="Flag to turn off the plot.", action='store_true')
ap.add_argument('-v', '--view', help="View all entries.", action='store_true')
ap.add_argument('-d', '--disabled_nodes', help="csv of disabled nodes.", default='0')
ap.add_argument('-s', '--ignore_status', help="Ignore status colors when setting display colors.", action='store_false')
ap.add_argument('-a', '--ignore_assign', help="Ignore reassigned antenna color", action='store_false')
ap.add_argument('-c', '--colors', help="Color legend to show (status or highlight).", default=None)
args = ap.parse_args()

disabled_nodes = [int(x) for x in args.disabled_nodes.split(",")]
grid = ant_node_grid.Grid(args.highlight, disabled_nodes=disabled_nodes)
grid.get_connected()
grid.process_array()
grid.set_display_color(args.ignore_status, args.ignore_assign, True)
if not args.noplot:
    plt_title = args.highlight if args.highlight is not None else "Antenna Node Grid"
    grid.addplot(plt_title, colors=args.colors)
    ant_node_grid.plt.show()
if args.view:
    grid.print_all()