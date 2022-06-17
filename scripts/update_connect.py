#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Script to run the hookup check between gsheet and database."""

import argparse
from hera_cm import upd_connect

if __name__ == '__main__':
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
    ap.add_argument('-a', '--action', help='what to do [cron, show]', choices=['cron', 'show', 's'],
                    default='cron')
    ap.add_argument('--skip-stop', dest='skip_stop', default='H,W',
                    help="Don't add connections that start with these.")
    args = ap.parse_args()
    if args.action == 'cron':
        cron_script = 'conn_update.sh'
    else:
        cron_script = None
    args.skip_stop = args.skip_stop.split(',')
else:
    args = argparse.Namespace(archive_path=None, script_path='./', node_csv='n', verbose=True)
    print(args)
    cron_script = None

script_type = 'connupd'

update = upd_connect.UpdateConnect(script_type=script_type, script_path=args.script_path,
                                   disable_err=args.enable_err, verbose=args.verbose)
if args.archive_path.startswith('___'):
    import os.path
    args.archive_path = os.path.join(update.script_path, args.archive_path[3:])
update.load_gsheet(node_csv=args.node_csv)
update.load_active()
update.make_sheet_connections()
direction = 'gsheet-active'
update.compare_connections(direction)
update.add_missing_parts()
update.add_missing_connections()
update.add_partial_connections()
update.add_different_connections()
update.add_rosetta()
if args.action.startswith('s'):
    print(f"\n----------Showing comparison for {direction}")
    update.show_summary_of_compare()
direction = 'active-gsheet'
update.compare_connections('active-gsheet')
if args.action.startswith('s'):
    print(f"\n\n----------Showing comparison for {direction}")
    update.show_summary_of_compare()
update.stop_missing_connections(skip=args.skip_stop)
update.finish(cron_script=cron_script, archive_to=args.archive_path)
