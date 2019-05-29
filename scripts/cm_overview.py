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


if __name__ == '__main__':
    parser = mc.get_mc_argument_parser()
    args = parser.parse_args()

    hpn = cm_utils.default_station_prefixes
    revision = 'LAST'
    exact_match = False
    force_new_cache = False
    print("CHANGE FORCE_NEW_CACHE TO TRUE WHEN DONE")
    force_db = False
    hookup_type = None
    hookup_cols = 'all'
    port = 'all'
    ports = True
    revs = False
    state = 'full'
    output_format = 'csv'
    filename = 'cm_overview_status.csv'
    at_date = 'now'

    # Start session
    db = mc.connect_to_mc_db(args)
    session = db.sessionmaker()

    # ############################ Get hookup data ############################
    hookup = cm_hookup.Hookup(session)
    hookup_dict = hookup.get_hookup(hpn_list=hpn, rev=revision, port_query=port, at_date=at_date,
                                    exact_match=exact_match, force_new_cache=force_new_cache,
                                    force_db=force_db, hookup_type=hookup_type)
    hookup.show_hookup(hookup_dict=hookup_dict, cols_to_show=hookup_cols,
                       ports=ports, revs=revs, state=state, filename=filename, output_format=output_format)

    hookup_data = {}
    hookup_header = []
    with open(filename, 'r') as fp:
        hookup_csv = csv.reader(fp)
        for row in hookup_csv:
            if len(row):
                hh = row[0].split()[0]
                if hh.startswith('HH'):
                    hookup_data[hh] = row
                else:
                    hookup_header = row
    sorted_hookup = sorted(hookup_data.keys())
    os.remove(filename)

    # ############################ Get apriori data ############################
    sys = cm_sysutils.Handling(session)
    apriori_data = {}
    for hh in sorted_hookup:
        apriori_data[hh] = sys.get_apriori_status_for_antenna(hh, at_date=at_date)

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
            key = 'HH{}'.format(antnum)
            sheet_data[key] = data

    # ############################ Get part info ###########################
    part = cm_handling.Handling(session)
    part_data = {}
    for k in sorted_hookup:
        part_dossier = part.get_part_dossier(hpn=k, rev='ACTIVE', at_date='now', exact_match=True, full_version=True)
        key = list(part_dossier.keys())[0]
        info = part_dossier[key].table_entry_row(['part_info', 'post_date', 'lib_file'])
        part_data[k] = []
        for pi in info:
            part_data[k].append([pi[2], pi[3]])

    # ############################ Get RF power ############################
    print("read from db")

    # ############################ Assemble data ###########################
    print("Hookup header:  ", hookup_header)
    print("Sheet header:  ", sheet_header)
    for k in sorted_hookup:
        print("\n\n----{}----------------------------------------".format(k))
        print(hookup_header)
        print(hookup_data[k])
        print('\n')
        print(apriori_data[k])
        print('\n', sheet_header)
        print(sheet_data[k])
        print(part_data[k])
