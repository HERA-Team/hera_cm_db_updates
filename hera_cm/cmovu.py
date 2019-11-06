#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

import argparse
import cm_overview

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--sheet-commands', dest='sheet_commands',
                    help="Flag to add sheet commands to processing queue", action='store_true')
    ap.add_argument('-m', '--hookup-mismatch', dest='hookup_mismatch',
                    help="Flag to add hookup mismatches to processing queue", action='store_true')
    ap.add_argument('-a', '--apriori-mismatch', dest='apriori_mismatch',
                    help="Flag to add apriori mismatches to processing queue", action='store_true')
    ap.add_argument('--no-copy', dest='keep_dated_copy', help="Don't keep a dated copy of script in cm_updates", action='store_false')
    ap.add_argument('--hide-view', dest='view', help="Don't print out mismatch results", action='store_false')
    ap.add_argument('--compare_keys', help="Keys to search in compare.  See cm_overview.compare", default='sheet')
    ap.add_argument('--getlist', help="List of info material to get. See cm_overview.allowed_getlist", default='hookup,sheets,apriori')
    args = ap.parse_args()
else:
    args = argparse.Namespace(sheet_commands=True, hookup_mismatch=True, apriori_mismatch=True, keep_dated_copy=True,
                              view=True, compare_keys='sheet', getlist='hookup,sheets,apriori')

args.getlist = args.getlist.split(',')

cmovu = cm_overview.Overview()
cmovu.get(getlist=args.getlist)
cmovu.compare(antkeys=args.compare_keys)
if args.view:
    print(cmovu.view_compare())

include_mismatches = args.hookup_mismatch or args.apriori_mismatch
if args.sheet_commands:
    cmovu.add_sheet_commands()
if include_mismatches:
    cmovu.add_mismatch_commands(add_hookup=args.hookup_mismatch, add_apriori=args.apriori_mismatch)

cmovu.process_commands(keep_dated=args.keep_dated_copy)
