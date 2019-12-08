# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
"""
from hera_mc import cm_hookup, cm_utils, cm_sysdef, cm_partconnect
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
    proc_script = 'connupdate'  # name of processing script file
    NotFound = "Not Found"

    def __init__(self):
        self.commands = {}
        self.mismatches = Namespace(hookup={}, connection={})

    def get_hpn_from_col(self, col, key, header):
        return util.gen_hpn(col, self.sheets.data[key][header.index(col)])

    def get_hookup(self):
        """
        Gets the hookup data from the hera_mc database.
        """
        self.hookup = cm_hookup.Hookup()
        self.hookup_dict = self.hookup.get_hookup(hpn=cm_req.hpn, pol=cm_req.pol, at_date=cm_req.at_date,
                                                  exact_match=cm_req.exact_match, hookup_type=cm_req.hookup_type)

    def get_sheets(self, test_state='read'):
        """
        Gets the googlesheet information from the internet
        """
        self.sheets = cm_gsheet.SheetData()
        self.sheets.load_sheet(test_state=test_state)

    def make_sheet_connections(self):
        """
        Go through all of the sheet and make cm_partconnect.Connections for comparison
        """
        self.sheets.connection = {}
        for sant in self.sheets.ants:
            for pol in self.pols:
                key = '{}-{}'.format(sant, pol)
                node_num = self.sheets.data[key][0]
                tab = 'node{}'.format(node_num)
                header = self.sheets.header[tab]
                self.sheets.connection[key] = []
                for i, col in enumerate(header):
                    if self.sheets.data[key][i] is not None:
                        tc_ = cm_partconnect.Connections()
                        if col == 'Ant':
                            ant = self.get_hpn_from_col('Ant', key, header)
                            feed = self.get_hpn_from_col('Feed', key, header)
                            tc_.connection(upstream_part=ant, up_part_rev='H', upstream_output_port='focus',
                                           downstream_part=feed, down_part_rev='A', downstream_input_port='input')
                        elif col == 'Feed':
                            feed = self.get_hpn_from_col('Feed', key, header)
                            fem = self.get_hpn_from_col('FEM', key, header)
                            tc_.connection(upstream_part=feed, up_part_rev='A', upstream_output_port='terminals',
                                           downstream_part=fem, down_part_rev='A', downstream_input_port='input')
                        elif col == 'FEM':
                            fem = self.get_hpn_from_col('FEM', key, header)
                            nbp = util.gen_hpn('NBP', node_num)
                            port = '{}{}'.format(pol, self.sheets.data[key][header.index('Bulkhead-PAM_Slot')])
                            if port is not None:
                                port = port.lower()
                            tc_.connection(upstream_part=fem, up_part_rev='A', upstream_output_port=pol.lower(),
                                           downstream_part=nbp, down_part_rev='A', downstream_input_port=port)
                        elif col == 'Bulkhead-PAM_Slot':
                            nbp = util.gen_hpn('NBP', node_num)
                            port = '{}{}'.format(pol, self.sheets.data[key][header.index('Bulkhead-PAM_Slot')])
                            if port is not None:
                                port = port.lower()
                            pam = self.get_hpn_from_col('PAM', key, header)
                            tc_.connection(upstream_part=nbp, up_part_rev='A', upstream_output_port=port,
                                           downstream_part=pam, down_part_rev='A', downstream_input_port=pol.lower())
                        elif col == 'PAM':
                            pam = self.get_hpn_from_col('PAM', key, header)
                            snap = self.get_hpn_from_col('SNAP', key, header)
                            port = self.sheets.data[key][header.index('Port')]
                            if len(port) == 0:
                                port = None
                            if port is not None:
                                port = port.lower()
                                if port[0] != pol[0].lower():
                                    msg = "{} port ({}) and pol ({}) don't match".format(snap, port, pol)
                                    print(msg)
                            tc_.connection(upstream_part=pam, up_part_rev='A', upstream_output_port=pol.lower(),
                                           downstream_part=snap, down_part_rev='A', downstream_input_port=port)
                        elif col == 'I2C_bus':  # extra to get @slot
                            pam = self.get_hpn_from_col('PAM', key, header)
                            try:
                                pamkey = cm_utils.make_part_key(pam, 'A')
                                pch = self.hookup.active.connections['up'][pamkey]['@SLOT'].downstream_part
                            except KeyError:
                                print("{} is not an active connection!  No pam from {}".format(pam, key))
                                pch = None
                            slot = '{}{}'.format('@SLOT', self.sheets.data[key][header.index('Bulkhead-PAM_Slot')])
                            if slot is not None:
                                slot = slot.lower()
                            tc_.connection(upstream_part=pam, up_part_rev='A', upstream_output_port='@slot',
                                           downstream_part=pch, down_part_rev='A', downstream_input_port=slot)
                        elif col == 'SNAP':
                            snap = self.get_hpn_from_col('SNAP', key, header)
                            node = util.gen_hpn("Node", node_num)
                            loc = "loc{}".format(self.sheets.data[key][header.index('SNAP_Slot')])
                            tc_.connection(upstream_part=snap, up_part_rev='A', upstream_output_port='rack',
                                           downstream_part=node, down_part_rev='A', downstream_input_port=loc)
                        if tc_.upstream_part is None or tc_.up_part_rev is None or tc_.upstream_output_port is None or\
                           tc_.downstream_part is None or tc_.down_part_rev is None or tc_.downstream_input_port is None:
                            continue
                        self.sheets.connection[key].append(tc_)

    def compare_connection(self):
        """
        Step through all of the sheet Connections and make sure they are all there and the same.
        """
        for sckey, scvals in self.sheets.connection.items():
            for scval in scvals:
                ackey = cm_utils.make_part_key(scval.downstream_part, scval.down_part_rev)
                acport = scval.downstream_input_port.upper()
                try:
                    acval = self.hookup.active.connections['down'][ackey][acport]
                except KeyError:
                    acval = None
                if acval is None or acval != scval:
                    self.mismatches.connection.setdefault(sckey, {'sheet': scvals, 'diff': []})
                    self.mismatches.connection[sckey]['diff'].append([acval, scval])

    def compare_hookup(self):
        """
        ## Note that this is left in for sanity/double-checking purposes.
        Compares the hookup data with the spreadsheet.  Writes self.mismatches.hookup
        keyed on 'ant:rev-pol' then 'sheet' and 'diff
        e.g. self.mismatches.hookup['HH30:A-E']['diff']
             self.mismatches.hookup['HH30:A-N']['sheet']
        """
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
                                self.mismatches.hookup.setdefault(sheet_key, {'sheet': sheet_row, 'diff': []})
                                self.mismatches.hookup[sheet_key]['diff'].append([col, val, sheet_val])

    def view_compare(self, ctypes=['hookup', 'connection']):
        """
        Views the comparison with cm database and spreadsheet.

        Parameters
        ----------
        ctypes : list, str
            List of strings for compare type:  connection/hookup

        Returns
        -------
        str
            output string
        """
        if isinstance(ctypes, str):
            ctypes = [ctypes]
        antkeys = []
        for ctype in ctypes:
            comp_type = getattr(self.mismatches, ctype)
            antkeys += list(comp_type.keys())
        antkeys = cm_utils.put_keys_in_order(list(set(antkeys)), sort_order='NPR')
        output_string = ''
        for antkey in antkeys:
            key, pol = antkey.split('-')
            output_string += "\n{:10s}----------    cm       <--->  sheet\n".format(antkey)
            for ctype in ctypes:
                comp_type = getattr(self.mismatches, ctype)
                if antkey in comp_type.keys():
                    for diff in comp_type[antkey]['diff']:
                        if len(diff) == 3:  # hookup
                            output_string += "{:18s}  {:10s}   <--->   {}\n".format(diff[0], diff[1], diff[2])
                        else:
                            output_string += "{:30s}   <--->   {}\n".format(str(diff[0]), diff[1])
        return output_string

    # ###########################################################################
    #                               other stuff                                 #
    # ###########################################################################
    def _get_val_from_cmdb(self, antkey, pol, sheet_col):
        """
        Bunch of ad hoc stuff to map the hookup_dict to the googlesheet column for comparison.
        """
        if sheet_col not in cm_gsheet.hu_col.keys():
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
