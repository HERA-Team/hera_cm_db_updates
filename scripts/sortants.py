#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
from __future__ import print_function

import argparse

ap = argparse.ArgumentParser()
ap.add_argument('filename', nargs='?', help="Filename to sort [installed.txt].  Use this with geo.py -f xxx", default='installed.txt')
ap.add_argument('--listed', help="Filename for formatted listed output [listants.txt]", default='listants.txt')
ap.add_argument('--num_per_row', help="Number to print per row in listed output [15]", default=15)
args = ap.parse_args()

ants = {}
with open(args.filename, 'r') as fp:
    for line in fp:
        data = line.split()
        ano = int(data[0][2:])
        ana = data[0]
        E = float(data[1])
        N = float(data[2])
        lng = float(data[3])
        lat = float(data[4])
        ants[ano] = [ana, E, N, lng, lat]
sak = sorted(list(ants.keys()))
with open(args.filename, 'w') as fp:
    for k in sak:
        x = ants[k]
        s = '{:5s}  {:.2f} {:.2f} {:.4f} {:.4f}\n'.format(x[0], x[1], x[2], x[3], x[4])
        fp.write(s)

with open(args.listed, 'w') as fp:
    for i in range(0, len(sak), args.num_per_row):
        s = ' '.join(['{:>3s}'.format(str(x)) for x in sak[i: i + args.num_per_row]])
        print(s)
        fp.write(s + '\n')
