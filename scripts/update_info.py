#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

import argparse
from hera_cm import upd_info

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--arc-path', dest='arc_path', help="Path for update archive.", default=None)
    ap.add_argument('--script-path', dest='script_path', help="Path for cron script", default='./')
    ap.add_argument('-n', '--node_csv', help="Flag for read/write of gsheet (r/w/n)", default='n')
    ap.add_argument('-v', '--verbose', help="Turn verbosity on.", action='store_true')
    ap.add_argument('-d', '--duplication_window',
                    help="Number of days to use for duplicate comments.", default=90.0)
    ap.add_argument('--view_duplicate',
                    help='In verbose, only show duplicates after this many days', default=0.0)
    ap.add_argument('--look_only', help='Flag to only look at data.', action='store_true')
    args = ap.parse_args()
else:
    args = argparse.Namespace(arc_path=None, script_path='./', node_csv='n', verbose=True,
                              duplication_window=90.0, view_duplicate=0.0, look_only=True)

if args.look_only:
    script_nom = None
    cron_nom = None
else:
    script_nom = 'infoupd'
    cron_nom = 'info_update.sh'

args.duplication_window = float(args.duplication_window)
args.view_duplicate = float(args.view_duplicate)
update = upd_info.UpdateInfo(script_nom=script_nom, script_path=args.script_path,
                             verbose=args.verbose)
update.load_gsheet(node_csv=args.node_csv)
update.load_active()
update.add_apriori()
update.add_sheet_notes(duplication_window=args.duplication_window, view_duplicate=args.view_duplicate)  # noqa
if args.look_only:
    print(update.new_apriori)
    print(update.new_notes)
else:
    update.finish(arc_path=args.arc_path, cron_script=cron_nom)
