#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

import argparse
from hera_cm import upd_connect

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--arc-path', dest='arc_path', help="Path for update archive.", default=None)
    ap.add_argument('--script-path', dest='script_path', help="Path for cron script", default='./')
    ap.add_argument('-v', '--verbose', help="Turn verbosity on.", action='store_true')
    args = ap.parse_args()
else:
    args = argparse.Namespace(arc_path=None, script_path='./', verbose=True)

script_nom = 'connupd'
cron_nom = 'conn_update.sh'

update = upd_connect.UpdateConnect(script_nom=script_nom, script_path=args.script_path, verbose=args.verbose)
update.load_gsheet()
update.load_hookup()
update.make_sheet_connections()
update.compare_connection()
update.gen_compare_script()
update.finish(arc_path=args.arc_path, cron_script=cron_nom)
