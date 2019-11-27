#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

import argparse
import upd_info

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--arc-path', dest='arc_path', help="Path for update archive.", default=None)
    ap.add_argument('--exe-path', dest='exe_path', help="Path for cron script", default='./')
    ap.add_argument('--verbose', help="Turn verbosity on.", action='store_true')
    ap.add_argument('-d', '--duplication_window', help="Number of days to use for duplicate comments.",
                    default=30.0)
    args = ap.parse_args()
else:
    args = argparse.Namespace(arc_path=None, exe_path='./', verbose=True, duplication_window=30.0)

args.duplication_window = float(args.duplication_window)
update = upd_info.UpdateInfo(exe_path=args.exe_path, verbose=args.verbose)
update.load_gsheet()
update.load_active()
update.add_apriori()
update.add_sheet_notes(duplication_window=args.duplication_window)
update.finish(arc_path=args.arc_path)
