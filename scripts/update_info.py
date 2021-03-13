#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Script to run the info update between the googlesheet and database."""

import argparse
from hera_cm import upd_info

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--script-path', dest='script_path', help="Path for active script",
                    default='default')
    ap.add_argument('--archive-path', dest='archive_path', help="Path for script archive.",
                    default='___cm_updates')
    ap.add_argument('-n', '--node_csv', help="For testing: flag for read/write of gsheet (r/w/n)",
                    choices=['read', 'write', 'none', 'r', 'w', 'n'], default='n')
    ap.add_argument('-v', '--verbose', help="Turn verbosity on.", action='store_true')
    ap.add_argument('-d', '--duplication_window',
                    help="Number of days to use for duplicate comments.", default=180.0)
    ap.add_argument('--view_duplicate',
                    help='In verbose, only show duplicates after this many days', default=0.0)
    ap.add_argument('--look_only', help='Flag to only look at data.', action='store_true')
    args = ap.parse_args()
else:
    args = argparse.Namespace(archive_path=None, script_path='default', node_csv='r', verbose=True,
                              duplication_window=70.0, view_duplicate=10.0, look_only=False)
    print(args)

if args.look_only:
    script_type = None
    cron_script = None
else:
    script_type = 'infoupd'
    cron_script = 'info_update.sh'

args.duplication_window = float(args.duplication_window)
args.view_duplicate = float(args.view_duplicate)
update = upd_info.UpdateInfo(script_type=script_type,
                             script_path=args.script_path,
                             verbose=args.verbose)
if args.archive_path.startswith('___'):
    import os.path
    args.archive_path = os.path.join(update.script_path, args.archive_path[3:])
update.load_gsheet(node_csv=args.node_csv)
update.load_active()
update.add_apriori()
update.add_sheet_notes(duplication_window=args.duplication_window,
                       view_duplicate=args.view_duplicate)
update.log_apriori_notifications()
if args.look_only:
    update.view_info()
else:
    update.finish(cron_script=cron_script, archive_to=args.archive_path)
