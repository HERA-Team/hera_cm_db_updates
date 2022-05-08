#! /usr/bin/env python

import os

with open('node_cat.csv', 'w') as fpout:
    for node in range(22):
        fn = f"node{node}.csv"
        if not os.path.exists(fn):
            continue
        with open(fn, 'r') as fpin:
            for line in fpin:
                if line.startswith('#END'):
                    break
                print(f"{node}:  {line.strip()}", file=fpout)
