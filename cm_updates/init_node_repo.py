#! /usr/bin/env python
import argparse
from shutil import copyfile

ap = argparse.ArgumentParser()
ap.add_argument('day')
args = ap.parse_args()

for node in range(0, 21):
    nfile = f"node{node}.csv"
    ndfile = f"node{node}_{args.day}.csv"
    try:
        print(ndfile, nfile)
        # copyfile(ndfile, f"../{nfile}")
    except FileNotFoundError:
        continue
