#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2023 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Script to get notes within a given day."""

import argparse
from hera_mc import cm_active, cm_utils
from tabulate import tabulate

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--days', help="Number of days (+/-) around date to look.", type=float, default=1.0)
cm_utils.add_date_time_args(ap)
args = ap.parse_args()

date = cm_utils.get_astropytime(args.date)

active = cm_active.get_active(date, loading=['info'])

found = {}
for hpn, notes in active.info.items():
    for note in notes:
        diff = abs(note.posting_gpstime - date.gps)
        print(diff / (3600*24))
        if diff < args.days * 3600 * 24:
            note.date = cm_utils.get_astropytime(note.posting_gpstime, float_format='gps')
            found[note.date.datetime] = note

table_header = ['Date', 'HPN', 'Note']
table_data = []
for this in sorted(found.keys()):
    table_data.append([found[this].date.datetime, found[this].hpn, found[this].comment])

print(tabulate(table_data, headers=table_header))
