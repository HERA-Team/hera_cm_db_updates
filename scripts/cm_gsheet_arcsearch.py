#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2022 the HERA Collaboration
# Licensed under the 2-clause BSD license.

from hera_cm import cm_gsheet
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('parts', help="part(s) to check.")
ap.add_argument('values', help='part number(s) to check')
args = ap.parse_args()

kwargs = {}
for _x, _y in zip(args.parts.split(','), args.values.split(',')):
    kwargs[_x] = _y

gsheetarc = cm_gsheet.ArchiveGsheet()
gsheetarc.find(**kwargs)