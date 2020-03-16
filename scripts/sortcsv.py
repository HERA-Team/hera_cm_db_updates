#! /usr/bin/env python
"""Convert output of hookup.py --file all.csv to helpful format."""

fin = open('all.csv', 'r')
fot = open('allsort.csv', 'w')

for line in fin:
    for le in ['e', 'n']:
        for i in range(10):
            a = '{}{}>'.format(le, i)
            b = '{}{:02d}>'.format(le, i)
            line = line.replace(a, b)
    line = line.replace('> ', '","').replace(' <', '","')
    fot.write(line)
