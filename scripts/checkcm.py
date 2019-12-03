#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
"""
from hera_cm import cm_checks
import argparse

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--comments', help="Check for duplicate comments", action='store_true')
    ap.add_argument('--connections', help="Check connections for ...", action='store_true')
    ap.add_argument('--apriori', help="Check for overlapping apriori states", action='store_true')
    args = ap.parse_args()

    cc = cm_checks.Checks()

    if args.comments:
        cc.check_for_duplicate_comments()
    if args.connections:
        cc.part_conn_assoc()
    if args.apriori:
        cc.apriori()
