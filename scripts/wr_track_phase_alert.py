#! /usr/bin/env python
import argparse
from hera_cm import wr_redis_tools

ap = argparse.ArgumentParser()
ap.add_argument('-n', '--nodes', help="'all' or csv list of nodes", default='all')
ap.add_argument('--alert', help="List of emails to alert if bad wr", default='')
args = ap.parse_args()

if args.nodes == 'all':
    args.nodes = list(range(30))
else:
    args.nodes = [int(x) for x in args.nodes.split(',')]

if not len(args.alert):
    args.alert = []
else:
    args.alert = args.alert.split(',')


wr_redis_tools.wrview(nodes=args.nodes, alert=args.alert)
