#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2018 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Update the sqlite db from the database."""

from hera_mc import mc
import subprocess
import os.path

table_dump_list = ['apriori_antenna', 'cm_version', 'connections',
                   'geo_location', 'part_info', 'parts', 'station_type']

cm_csv_path = mc.get_cm_csv_path(None)

subprocess.call('pg_dump -s hera_mc > schema.sql', shell=True)
dump = ('pg_dump --inserts --data-only hera_mc -t {} > inserts.sql'
        .format(' -t '.join(table_dump_list)))
subprocess.call(dump, shell=True)

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

sqlfile = os.path.join(cm_csv_path, 'cm_hera.sql')
dbfile = os.path.join(cm_csv_path, 'hera_mc.db')
with open(sqlfile, 'w') as f:
    f.write(schema)
    f.write(inserts)
    f.write(".save {}\n".format(dbfile))
subprocess.call('sqlite3 < {}'.format(sqlfile), shell=True)

subprocess.call('rm -f schema.sql', shell=True)
subprocess.call('rm -f inserts.sql', shell=True)
subprocess.call('rm -f {}'.format(sqlfile), shell=True)
