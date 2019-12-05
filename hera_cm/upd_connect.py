#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
"""
from hera_mc import cm_hookup, cm_utils, cm_sysdef, mc
from . import util, cm_gsheet

import os
import csv
import requests
import datetime
from argparse import Namespace

cm_req = Namespace(hpn=cm_sysdef.hera_zone_prefixes, pol='all',
                   at_date='now', exact_match=False, hookup_type=None)


class Update:
    pols = ['E', 'N']
    com_script = 'connupdate'  # name of processing script file
    NotFound = "Not Found"

    def __init__(self):
        db = mc.connect_to_mc_db(None)
        self.session = db.sessionmaker()
        self.commands = {}

    def get_hookup(self):
        """
        Gets the hookup data from the hera_mc database.
        """
        self.hookup = cm_hookup.Hookup(self.session)
        self.hookup_dict = self.hookup.get_hookup(hpn=cm_req.hpn, pol=cm_req.pol, at_date=cm_req.at_date,
                                                  exact_match=cm_req.exact_match, hookup_type=cm_req.hookup_type)

    def get_sheets(self):
        """
        Gets the googlesheet information from the internet
        """
        self.sheets = cm_gsheet.SheetData()
        self.sheets.load_sheet()

    def compare(self):
        """
        Compares the hookup data with the spreadsheet.  Writes self.mismatches keyed on
        'ant:rev-pol' then 'sheet', 'diff', 'date', ''
        e.g. self.mismatches['HH30:A-E']['diff']
             self.mismatches['HH30:A-N']['sheet']
             self.mismatches['HH29:A-E']['date']

        """
        self.mismatches = {}
        for antkey in self.sheets.ants:
            for pol in self.pols:
                sheet_key = "{}-{}".format(antkey, pol)
                tab = 'node{}'.format(self.sheets.data[sheet_key][0])
                header = self.sheets.header[tab]
                sheet_row = util.get_row_dict(header, self.sheets.data[sheet_key])
                for i, col in enumerate(header):
                    val = self._get_val_from_cmdb(antkey, pol, col)
                    if val is not None:
                        sheet_val = self.sheets.data[sheet_key][i]
                        if val.upper() != sheet_val.upper():
                            if val != self.NotFound or len(sheet_val.strip()):
                                self.mismatches.setdefault(sheet_key, {'sheet': sheet_row,
                                                                       'diff': [], 'date': self.sheets.date[tab]})
                                self.mismatches[sheet_key]['diff'].append([col, val, sheet_val])

    def make_sheet_connections(self):
        print("NOT DOING THIS YET.")
        self.sheet_connections = {}
        for sant in self.sheet_ants:
            self.sheet_connections[sant] = []
            for part in self.sheet_data[sant]:
                print(part)

    def view_compare(self):
        """
        Views the comparison with hookup data and spreadsheet.

        Returns
        -------
        str
            output string
        """
        antkeys = cm_utils.put_keys_in_order(list(self.mismatches.keys()), sort_order='NPR')
        output_string = ''
        for antkey in antkeys:
            key, pol = antkey.split('-')
            output_string += "\n{:10s}----------    cm       <--->  sheet\n".format(antkey)
            for diff in self.mismatches[antkey]['diff']:
                output_string += "{:18s}  {:10s}   <--->   {}\n".format(diff[0], diff[1], diff[2])
        return output_string

    def _get_val_from_cmdb(self, antkey, pol, sheet_col):
        """
        Bunch of ad hoc stuff to map the hookup_dict to the googlesheet column for comparison.
        """
        if sheet_col not in cm_gsheet.hu_col.keys():
            return None
        if sheet_col.lower() == 'apriori':
            return None
        hu = self.hookup_dict[antkey]
        pol = pol.upper()
        for ppkey in hu.hookup.keys():
            if ppkey.upper().startswith(pol.upper()):
                break
        try:
            pam_slot = util.get_num(hu.hookup[ppkey][cm_gsheet.hu_col['Bulkhead-PAM_Slot']].downstream_input_port)
        except IndexError:
            return self.NotFound
        try:
            snap_slot = str(int(util.get_num(hu.hookup[ppkey][cm_gsheet.hu_col['Node']].downstream_input_port)))
        except IndexError:
            return self.NotFound
        i2c = (int(pam_slot) + 2) % 3 + 1

        if sheet_col.lower() == 'i2c_bus':
            return str(i2c)
        if sheet_col.lower() == 'bulkhead-pam_slot':
            return pam_slot
        if sheet_col.lower() == 'snap_slot':
            return snap_slot
        if sheet_col.lower() == 'port' or sheet_col.lower() == 'pol':
            try:
                return hu.hookup[ppkey][cm_gsheet.hu_col[sheet_col]].downstream_input_port.upper()
            except IndexError:
                return self.NotFound
        try:
            part = hu.hookup[ppkey][cm_gsheet.hu_col[sheet_col]].downstream_part
        except IndexError:
            return self.NotFound
        num = str(int(util.get_num(part)))

        if sheet_col.lower() == 'snap':
            return "{}{}".format(part[3], num)

        return num
