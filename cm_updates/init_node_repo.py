#! /usr/bin/env python
import argparse
from shutil import copyfile

ap = argparse.ArgumentParser()
ap.add_argument('day')
args = ap.parse_args()

for node in range(0, 21):
    nfile = f"gsheet/node{node}.csv"
    ndfile = f"gsheettmp/node{node}_{args.day}.csv"
    try:
        copyfile(ndfile, nfile)
    except FileNotFoundError:
        continue
