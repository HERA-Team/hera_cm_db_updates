#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

import argparse
import cm_overview

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--sheet', help="Flag to run sheet commands.", action='store_true')
    ap.add_argument('-m', '--mismatch', help="Flag to find/fix mismatches.", action='store_true')
    ap.add_argument('-a', '--apriori_only', help="Include only apriori mismatches", action='store_true')
    ap.add_argument('--no-copy', dest='keep_dated_copy', help="Keep a dated copy", action='store_false')
    ap.add_argument('--hide-view', dest='view', help="Print out results.", action='store_false')
    args = ap.parse_args()
else:
    args = argparse.Namespace(sheet=True, mismatch=True, apriori_only=True, keep_dated_copyTrue, view=True)

x = cm_overview.Overview()
x.compare(antkeys='sheet')
if args.view:
    print(x.view_compare())

if args.sheet:
    x.add_sheet_commands()
if args.mismatch:
    x.add_mismatch_commands(apriori_only=args.apriori_only)

x.process_commands(keep_dated=args.keep_dated_copy)
