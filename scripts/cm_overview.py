#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Builds csv files for configuration_overview googlesheet

Simple commands within the "Actions" column:

<S PAM/FEM/SNAP OLD:NEW YYYY/MM/DD HH:MM>
"""
from __future__ import absolute_import, division, print_function

from hera_mc import cm_hookup, cm_utils, cm_sysutils, cm_handling, mc
import sheet_data as sd

import os
import csv
import requests
from argparse import Namespace

hu_testing = cm_utils.default_station_prefixes
hu_testing = 'cache'

_rq = Namespace(hpn=hu_testing, revision='LAST',
                exact_match=False, force_new_cache=True, force_db=False,
                hookup_type=None, port='all', at_date='now')


def get_num(val):
    return ''.join(c for c in val if c.isnumeric())


class Overview:
    def __init__(self):
        # Start session
        db = mc.connect_to_mc_db(None)
        self.session = db.sessionmaker()

    def get_hookup(self):
        # ############################ Get hookup data ############################
        self.hookup = cm_hookup.Hookup(self.session)
        self.hookup_dict = self.hookup.get_hookup(hpn_list=_rq.hpn, rev=_rq.revision, port_query=_rq.port,
                                                  at_date=_rq.at_date, exact_match=_rq.exact_match,
                                                  force_new_cache=_rq.force_new_cache, force_db=_rq.force_db,
                                                  hookup_type=_rq.hookup_type)
        self.connected = []
        for ant in self.hookup_dict.keys():
            for pol in ['e', 'n']:
                if self.hookup_dict[ant].fully_connected[pol]:
                    self.connected.append(ant)
                    break
        self.connected = cm_utils.put_keys_in_numerical_order(self.connected)

    def get_apriori(self):
        # ############################ Get apriori data ############################
        sys = cm_sysutils.Handling(self.session)
        self.apriori_data = {}
        for antkey in self.connected:
            hh = antkey.split(':')[0]
            self.apriori_data[antkey] = sys.get_apriori_status_for_antenna(hh, at_date=_rq.at_date)

    def get_sheets(self):
        # ############################ Get previous sheet ############################
        self.sheet_data = {}
        self.sheet_header = []
        self.sheet_date = {}
        self.tabs = sorted(list(sd.gsheet.keys()))
        for tab in self.tabs:
            xxx = requests.get(sd.gsheet[tab])
            csv_tab = b''
            for line in xxx:
                csv_tab += line
            csv_tab = csv.reader(csv_tab.decode('utf-8').splitlines())
            for data in csv_tab:
                if data[0].startswith('Ant'):
                    self.sheet_header = data
                    continue
                elif data[0].startswith('Date:'):
                    self.sheet_date[tab] = data[1]
                    break
                try:
                    antnum = int(data[0])
                except ValueError:
                    continue
                key = 'HH{}:A-{}'.format(antnum, data[1].upper())
                self.sheet_data[key] = data

    def get_part_info(self):
        # ############################ Get part info ###########################
        part = cm_handling.Handling(self.session)
        self.part_data = {}
        for k in self.connected:
            ant = k.split(':')[0]
            part_dossier = part.get_part_dossier(hpn=ant, rev='ACTIVE', at_date=_rq.at_date, exact_match=True, full_version=True)
            if len(part_dossier):
                key = list(part_dossier.keys())[0]
                info = part_dossier[key].table_entry_row(['part_info', 'post_date', 'lib_file'])
                self.part_data[k] = []
                for pi in info:
                    self.part_data[k].append([pi[2], pi[3]])

    def get_RF_power(self):
        # ############################ Get RF power ############################
        print("Need to still get RF power from db")

    def find_mismatches(self):
        # ################### Check that cm and googlesheet match ##############
        self.mismatches = []
        for antkey in self.connected:
            for pol in ['e', 'n']:
                for i, col in enumerate(self.sheet_header):
                    val = self.__get_val(antkey, pol, col)
                    if val is not None:
                        sheet_key = "{}-{}".format(antkey, pol.upper())
                        sheet_val = self.sheet_data[sheet_key][i]
                        if val != sheet_val:
                            self.mismatches.append("\t<{} {} {}>    {}   |   {}".format(antkey, pol, col, val, sheet_val))

    def dump_data(self):
        print("Sheet header:  ", self.sheet_header)
        for k in self.connected:
            print("\n\n----{}----------------------------------------".format(k))
            print(self.hookup_dict[k])
            print('\n')
            print(self.apriori_data[k])
            print(self.part_data[k])
            print('\n')
            for pol in ['E', 'N']:
                sdkey = '{}-{}'.format(k, pol)
                print(self.sheet_data[sdkey])

        if len(self.mismatches):
            print("\nThese {} entries do not match:".format(len(self.mismatches)))
            for mm in self.mismatches:
                print(mm)
        else:
            print("All entries match.")

    def __get_val(self, antkey, pol, sheet_col):
        """
        Bunch of ad hoc stuff to map the hookup_dict to the googlesheet column
        """
        if sheet_col not in list(sd.hu_col.keys()):
            return None
        hu = self.hookup_dict[antkey]
        pol = pol.lower()
        pos = get_num(hu.hookup[pol][sd.hu_col['Position']].downstream_input_port)
        i2c = (int(pos) + 2) % 3 + 1

        if sheet_col == 'I2C_bus':
            return str(i2c)
        if sheet_col == 'Position':
            return pos
        if sheet_col == 'Port':
            return hu.hookup[pol][sd.hu_col[sheet_col]].downstream_input_port

        part = hu.hookup[pol][sd.hu_col[sheet_col]].downstream_part
        num = str(int(get_num(part)))

        if sheet_col == 'SNAP':
            loc = str(int(get_num(hu.hookup[pol][sd.hu_col['Node']].downstream_input_port)))
            return "SNAP{} ({}{})".format(loc, part[3], num)
        return num
