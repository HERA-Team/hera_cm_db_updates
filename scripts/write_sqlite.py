#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2018 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Update the sqlite db from the psql database."""
from . import db_mgmt

hash_dict = db_mgmt.get_table_hash_info()

if not db_mgmt.same_table_hash_info(hash_dict):
    db_mgmt.update_sqlite()
