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
                    default='./')
    ap.add_argument('--archive-path', dest='archive_path', help="Path for script archive.",
                    default=None)
    ap.add_argument('-n', '--node_csv', help="For testing: flag for read/write of gsheet (r/w/n)",
                    choices=['read', 'write', 'none', 'r', 'w', 'n'], default='n')
    ap.add_argument('-v', '--verbose', help="Turn verbosity on.", action='store_true')
    args = ap.parse_args()
    cron_script = 'conn_update.sh'
else:
    args = argparse.Namespace(archive_path=None, script_path='./', node_csv='w', verbose=True)
    print(args)
    cron_script = None

script_type = 'connupd'

update = upd_connect.UpdateConnect(script_type=script_type,
                                   script_path=args.script_path,
                                   verbose=args.verbose)
update.load_gsheet(node_csv=args.node_csv)
update.load_active()
update.make_sheet_connections()
data = update.compare_connections('gsheet-active')
update.add_missing_parts()
update.add_missing_connections()
update.finish(cron_script=cron_script, archive_to=args.archive_path)
