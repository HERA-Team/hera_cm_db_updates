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
    ap.add_argument('-v', '--verbose', help="Turn verbosity on.", action='store_true')
    ap.add_argument('-d', '--duplication_window', help="Number of days to use for duplicate comments.",
                    default=60.0)
    args = ap.parse_args()
else:
    args = argparse.Namespace(arc_path=None, script_path='./', verbose=True, duplication_window=60.0)

script_nom = 'infoupd'
cron_nom = 'info_update.sh'

args.duplication_window = float(args.duplication_window)
update = upd_info.UpdateInfo(script_nom=script_nom, script_path=args.script_path, verbose=args.verbose)
update.load_gsheet()
update.load_active()
update.add_apriori()
update.add_sheet_notes(duplication_window=args.duplication_window)
update.finish(arc_path=args.arc_path, cron_script=cron_nom)
