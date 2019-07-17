#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2018 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Script to handle updating the sqlite db from files.  This is __very__ specific and brittle
"""

from __future__ import absolute_import, division, print_function
from hera_mc import mc
import subprocess

cm_csv_path = mc.get_cm_csv_path(None)

subprocess.call('pg_dump -s hera_mc > schema.sql', shell=True)
subprocess.call('pg_dump --inserts --data-only hera_mc > inserts.sql', shell=True)

schema = ''
creating_table = False
with open('schema.sql', 'r') as f:
    for line in f:
        modline = line.replace('public.', '')
        if 'CREATE TABLE' in modline:
            creating_table = True
            schema += modline
            continue
        if creating_table:
            if 'DEFAULT' in modline:
                dat = modline.split()
                schema += (dat[0] + ' ' + dat[1] + '\n')
            else:
                schema += modline
            if ');' in modline:
                creating_table = False

inserts = ''
with open('inserts.sql', 'r') as f:
    for line in f:
        modline = line.replace('public.', '')
        if 'INSERT' in modline:
            inserts += modline

with open('cm_hera.sql', 'w') as f:
    f.write(schema)
    f.write(inserts)

subprocess.call('rm -f schema.sql', shell=True)
subprocess.call('rm -f inserts.sql', shell=True)

print("""
Now type the following:

$ sqlite3
sqlite> .read cm_hera.sql
sqlite> .save hera_mc.db
sqlite> .quit

then move hera_mc.db to hera_cm_db_updates
and delete cm_hera.sql
""")
