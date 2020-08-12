#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Script to run the hookup check between gsheet and database."""

import argparse
from hera_cm import upd_connect

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--arc-path', dest='arc_path', help="Path for update archive.", default=None)
    ap.add_argument('--script-path', dest='script_path', help="Path for cron script", default='./')
    ap.add_argument('-n', '--node_csv', help="For testing: flag for read/write of gsheet (r/w/n)",
                    default='n')
    ap.add_argument('-v', '--verbose', help="Turn verbosity on.", action='store_true')
    ap.add_argument('-l', '--look_only', help="Look at the results only", action='store_true')
    args = ap.parse_args()
else:
    args = argparse.Namespace(arc_path=None, script_path='./', node_csv='n',
                              verbose=True, look_only=True)

if args.look_only:
    script_nom = None
    cron_nom = None
else:
    script_nom = 'connupd'
    cron_nom = 'conn_update.sh'

update = upd_connect.UpdateConnect(script_nom=script_nom, script_path=args.script_path,
                                   verbose=args.verbose)
update.load_gsheet(node_csv=args.node_csv)
update.load_active()
update.make_sheet_connections()
data = update.compare_connections('gsheet-active')
if args.look_only:
    update.view_conn()
    update.view_diff()
else:
    update.gen_compare_script()
    update.finish(arc_path=args.arc_path, cron_script=cron_nom)
