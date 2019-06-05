#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2017 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Builds csv files for configuration_overview googlesheet

"""
from __future__ import absolute_import, division, print_function

from hera_mc import cm_hookup, cm_utils, cm_sysutils, cm_handling, mc

import os
import csv
import requests


def get_num(val):
    return ''.join(c for c in val if c.isnumeric())


hpn = cm_utils.default_station_prefixes
hpn = 'cache'
print("REMOVE ABOVE LINE WHEN DONE")
revision = 'LAST'
exact_match = False
force_new_cache = True
force_db = False
hookup_type = None
port = 'all'
at_date = 'now'

# Start session
db = mc.connect_to_mc_db(None)
session = db.sessionmaker()

# ############################ Get hookup data ############################
hookup = cm_hookup.Hookup(session)
hookup_dict = hookup.get_hookup(hpn_list=hpn, rev=revision, port_query=port, at_date=at_date,
                                exact_match=exact_match, force_new_cache=force_new_cache,
                                force_db=force_db, hookup_type=hookup_type)
connected = []
for ant in hookup_dict.keys():
    for pol in ['e', 'n']:
        if hookup_dict[ant].fully_connected[pol]:
            connected.append(ant)
            break
connected = cm_utils.put_keys_in_numerical_order(connected)
connected = [x.split(':')[0] for x in connected]

hu_col = {'Ant': 0, 'Feed': 1, 'FEM': 2, 'PAM': 4, 'Position': 3, 'I2C_bus': -1, 'SNAP': 5, 'Port': 5, 'Node': 6}


def get_val(ant, pol, sheet_col):
    """
    Bunch of ad hoc stuff to map the hookup_dict to the googlesheet column
    """
    if sheet_col not in list(hu_col.keys()):
        return None

    hu = get_hu(ant)
    pol = pol.lower()
    pos = get_num(hu.hookup[pol][hu_col['Position']].downstream_input_port)
    i2c = (int(pos) + 2) % 3 + 1

    if sheet_col == 'I2C_bus':
        return str(i2c)
    if sheet_col == 'Position':
        return pos
    if sheet_col == 'Port':
        return hu.hookup[pol][hu_col[sheet_col]].downstream_input_port

    part = hu.hookup[pol][hu_col[sheet_col]].downstream_part
    num = str(int(get_num(part)))

    if sheet_col == 'SNAP':
        loc = str(int(get_num(hu.hookup[pol][hu_col['Node']].downstream_input_port)))
        return "SNAP{} ({}{})".format(loc, part[3], num)
    return num


def get_hu(ant):
    """
    Components of hookup_dossier entry are:
            entry_key = entry_key
            hookup = {}  # actual hookup connection information
            fully_connected = {}  # flag if fully connected
            hookup_type = {}  # name of hookup_type
            columns = {}  # list with the actual column headers in hookup
            timing = {}  # aggregate hookup start and stop
    Dictionaries are keyed on 'e'/'n'
    """
    ant = ant + ':A'
    return hookup_dict[ant]


# ############################ Get apriori data ############################
sys = cm_sysutils.Handling(session)
apriori_data = {}
for hh in connected:
    apriori_data[hh] = sys.get_apriori_status_for_antenna(hh, at_date=at_date)
print("Read 'apriori_data'")

# ############################ Get previous sheet ############################
tabs = ['node0', 'node9']
gsheet = {}
gsheet['node0'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=0&single=true&output=csv"
gsheet['node9'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=59309582&single=true&output=csv"
sheet_data = {}
sheet_header = []
sheet_date = {}
for tab in tabs:
    xxx = requests.get(gsheet[tab])
    csv_tab = b''
    for line in xxx:
        csv_tab += line
    csv_tab = csv.reader(csv_tab.decode('utf-8').splitlines())
    for data in csv_tab:
        if data[0].startswith('Ant'):
            sheet_header = data
            continue
        elif data[0].startswith('Date:'):
            sheet_date[tab] = data[1]
            break
        try:
            antnum = int(data[0])
        except ValueError:
            continue
        key = 'HH{}:{}'.format(antnum, data[1].upper())
        sheet_data[key] = data
print("Read 'sheet_data', 'sheet_header', 'sheet_date'")

# ############################ Get part info ###########################
part = cm_handling.Handling(session)
part_data = {}
for k in connected:
    part_dossier = part.get_part_dossier(hpn=k, rev='ACTIVE', at_date='now', exact_match=True, full_version=True)
    if len(part_dossier):
        key = list(part_dossier.keys())[0]
        info = part_dossier[key].table_entry_row(['part_info', 'post_date', 'lib_file'])
        part_data[k] = []
        for pi in info:
            part_data[k].append([pi[2], pi[3]])
print("Read 'part_data'")

# ############################ Get RF power ############################
print("Need to still get RF power from db")


# ###DO STUFF
mismatches = []
for ant in connected:
    for pol in ['e', 'n']:
        for i, col in enumerate(sheet_header):
            val = get_val(ant, pol, col)
            if val is not None:
                sheet_key = "{}:{}".format(ant, pol.upper())
                if val != sheet_data[sheet_key][i]:
                    mismatches.append("\t<{} {} {}>    {}   |   {}".format(ant, pol, col, val, sheet_data[sheet_key][i]))

if len(mismatches):
    print("\nThese entries do not match:")
    for mm in mismatches:
        print(mm)
else:
    print("All entries match.")


# ############################ Assemble data ###########################
def print_data():
    print("Hookup header:  ", hookup_header)
    print("Sheet header:  ", sheet_header)
    for k in connected:
        print("\n\n----{}----------------------------------------".format(k))
        print(hookup_header)
        print(hookup_data[k])
        print('\n')
        print(apriori_data[k])
        print('\n', sheet_header)
        print(sheet_data[k])
        print(part_data[k])
