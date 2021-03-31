#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2018 the HERA Collaboration
# Licensed under the 2-clause BSD license.
"""Update the sqlite db from the psql database."""
import argparse
from hera_cm import db_mgmt

ap = argparse.ArgumentParser()
ap.add_argument('--force', help='Force db write.', action='store_true')
args = ap.parse_args()


hash_dict = db_mgmt.get_table_hash_info()

if args.force:
    write_database = True
else:
    write_database = not db_mgmt.same_table_hash_info(hash_dict)


if write_database:
    db_mgmt.update_sqlite()
    db_mgmt.write_table_hash_info(hash_dict)
