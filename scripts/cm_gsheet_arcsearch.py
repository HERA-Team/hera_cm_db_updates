#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2022 the HERA Collaboration
# Licensed under the 2-clause BSD license.

from hera_cm import cm_gsheet
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('parts', help="part(s) to check.")
ap.add_argument('values', help='part number(s) to check')
ap.add_argument('-b', '--show_blame', help='Show git blame for gsheet files', action='store_true')
args = ap.parse_args()

kwargs = {}
for _x, _y in zip(args.parts.split(','), args.values.split(',')):
    kwargs[_x] = _y

if args.show_blame:
    args.show_blame = 'gitpython'  # hard-code to use gitpython method, as opposed to commandline
gsheetarc = cm_gsheet.ArchiveGsheet()
gsheetarc.find(blame=args.show_blame, **kwargs)