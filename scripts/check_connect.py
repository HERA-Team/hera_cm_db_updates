#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Script to run the hookup check between gsheet and database."""

import argparse
from hera_cm import upd_connect

ap = argparse.ArgumentParser()
ap.add_argument('-p', '--parts_to_find', help="If set, find the parts (csv list).", default=None)
ap.add_argument('-n', '--node_csv', help="For testing: flag for read/write of gsheet (r/w/n)",
                choices=['read', 'write', 'none', 'r', 'w', 'n'], default='n')
ap.add_argument('-v', '--verbose', help="Turn verbosity on.", action='store_true')
ap.add_argument('-s', '--skip_duplicate_check', help='Skip the duplicate check.', action='store_true')  # noqa
args = ap.parse_args()

update = upd_connect.UpdateConnect(script_type='no_signal_chain', script_path='.',
                                   disable_err=True, verbose=args.verbose)

if not args.skip_duplicate_check:
    print("Checking duplicate active parts...")
    update.check_active()

update.load_gsheet(args.node_csv)
update.make_sheet_connections()
if args.parts_to_find is not None:
    args.parts_to_find = args.parts_to_find.split(',')
    update.find_parts(args.parts_to_find, show=True)
