#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Checks the database for:
    associativity of connections to active parts
    duplicated comments
    concurrent apriori states
"""
from hera_cm import cm_checks
import argparse

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-m', '--comments', help="Check for duplicate comments",
                    action='store_true')
    ap.add_argument('-n', '--connections', help="Check connections for ...",
                    action='store_true')
    ap.add_argument('-a', '--apriori', help="Check for overlapping apriori states",
                    action='store_true')
    ap.add_argument('-e', '--ethers', help="Check the hosts/ethers hera_mc vs redis",
                    action='store_true')
    ap.add_argument('-d', '--daemons', help="Check running daemons",
                    action='store_true')
    ap.add_argument('--output-format', dest='output_format', default='orgtbl',
                    help='Format of output table - uses cm_utils.general_table_handler')
    args = ap.parse_args()

    cc = cm_checks.Checks()

    if args.comments:
        cc.check_for_duplicate_comments()
    if args.connections:
        cc.part_conn_assoc()
    if args.apriori:
        cc.apriori()
    if args.ethers:
        cc.check_hosts_ethers(table_fmt=args.output_format)
        cc.check_for_same(use_lower=True, ignore_no_data=True)
    if args.daemons:
        cc.check_daemon()
