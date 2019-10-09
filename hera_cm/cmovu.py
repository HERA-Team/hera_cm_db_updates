#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

import argparse
import cm_overview

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--sheet', help="Flag to add sheet commands to processing queue", action='store_true')
    ap.add_argument('-m', '--mismatch', help="Flag to find and add mismatches to processing queue", action='store_true')
    ap.add_argument('-a', '--apriori_only', help="Include only apriori mismatches to processing queue", action='store_true')
    ap.add_argument('--no-copy', dest='keep_dated_copy', help="Don't keep a dated copy of script in cm_updates", action='store_false')
    ap.add_argument('--hide-view', dest='view', help="Don't print out mismatch results", action='store_false')
    ap.add_argument('--compare_keys', help="Keys to search in compare.  See cm_overview.compare", default='sheet')
    ap.add_argument('--getlist', help="List of info material to get. See cm_overview.allowed_getlist", default='hookup,apriori,sheets')
    args = ap.parse_args()
else:
    args = argparse.Namespace(sheet=True, mismatch=True, apriori_only=True, keep_dated_copy=True, view=True,
                              compare_keys='sheet', getlist='hookup,apriori,sheets')

args.getlist = args.getlist.split(',')

cmovu = cm_overview.Overview()
cmovu.get(getlist=args.getlist)
cmovu.compare(antkeys=args.compare_keys)
if args.view:
    print(cmovu.view_compare())

if args.sheet:
    cmovu.add_sheet_commands()
if args.mismatch:
    cmovu.add_mismatch_commands(apriori_only=args.apriori_only)

cmovu.process_commands(keep_dated=args.keep_dated_copy)
