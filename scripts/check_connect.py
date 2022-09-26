#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Script to run the hookup check between gsheet and database."""

import argparse
from hera_cm import upd_connect

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--find_parts', help="If set, find the parts (csv list).", default=None)
ap.add_argument('-n', '--node_csv', help="For testing: flag for read/write of gsheet (r/w/n)",
                choices=['read', 'write', 'none', 'r', 'w', 'n'], default='n')
ap.add_argument('-v', '--verbose', help="Turn verbosity on.", action='store_true')
args = ap.parse_args()

update = upd_connect.UpdateConnect(script_type='no_signal_chain', script_path='.',
                                   disable_err=True, verbose=args.verbose)

print("Checking duplicate active parts...")
update.check_active()

update.load_gsheet(args.node_csv)
update.make_sheet_connections()
if args.find_parts is not None:
    args.find_parts = args.find_parts.split(',')
    update.find_parts(args.find_parts, show=True)
