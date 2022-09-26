#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Script to run the hookup check between gsheet and database."""

import argparse
from hera_cm import upd_connect

ap = argparse.ArgumentParser()
ap.add_argument('--script-path', dest='script_path', help="Path for active script",
                default='default')
ap.add_argument('--archive-path', dest='archive_path', help="Path for script archive.",
                default='___cm_updates')
ap.add_argument('-n', '--node_csv', help="For testing: flag for read/write of gsheet (r/w/n)",
                choices=['read', 'write', 'none', 'r', 'w', 'n'], default='n')
ap.add_argument('-v', '--verbose', help="Turn verbosity on.", action='store_true')
ap.add_argument('--enable-err', dest='enable_err', action='store_false',
                help='Enable erroring out for some errors')
ap.add_argument('-s', '--show', help='show comparisons', action='store_true')
ap.add_argument('--skip-stop', dest='skip_stop', default='H,W',
                help="Don't stop connections that start with these.")
ap.add_argument('--alert', help="Email addresses for alerts.", default='ddeboer@berkeley.edu')
args = ap.parse_args()
cron_script = 'conn_update.sh'
args.skip_stop = args.skip_stop.split(',')
if '@' in args.alert:
    args.alert = args.alert.split(',')
else:
    args.alert = None

script_type = 'connupd'

update = upd_connect.UpdateConnect(script_type=script_type, script_path=args.script_path,
                                   disable_err=args.enable_err, verbose=args.verbose)
if args.archive_path.startswith('___'):
    import os.path
    args.archive_path = os.path.join(update.script_path, args.archive_path[3:])

update.pipe(args.node_csv, args.skip_stop, args.show,
            cron_script=cron_script, archive_to=args.archive_path, alert=args.alert)
