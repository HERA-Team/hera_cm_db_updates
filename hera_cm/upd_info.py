#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
This class generates the script to update comments and "apriori" info from the configuration
googlesheet
"""
from hera_mc import cm_utils, cm_active, mc

import cm_gsheet
import signal_chain
import upd_util

import os
import datetime
from argparse import Namespace


class UpdateInfo:
    def __init__(self, com_script='input_update', output_script_path='./'):
        self.today = datetime.datetime.now()
        self.cdate = '{}/{:02d}/{:02d}'.format(self.today.year, self.today.month, self.today.day)
        self.ctime = '{:02d}:{:02d}'.format(self.today.hour, self.today.minute)
        self.hera = signal_chain.Update(com_script, output_script_path=output_script_path, chmod=True)
        self.update_counter = 0

    def load_gsheet(self):
        self.gsheet = cm_gsheet.SheetData()
        self.gsheet.load_sheet()

    def load_active(self):
        self.active = cm_active.ActiveData()
        self.active.load_info()
        self.active.load_apriori()

    def add_apriori(self):
        """
        Write out for apriori differences.
        """
        for key in self.gsheet.ants:
            E = self.gsheet.data[key + '-E'][11]
            N = self.gsheet.data[key + '-N'][11]
            ant, rev = cm_utils.split_part_key(key)
            if E != N:
                print("{} and {} should be the same.".format(E, N))
                continue
            if len(E) == 0:
                continue
            if E != self.active.apriori[key].status:
                print("Updating {}   {}".format(E, self.active.apriori[key].status))
                self.hera.update_apriori(ant, E, self.cdate, self.ctime)
                self.update_counter += 1

    def add_sheet_commands(self):
        """
        Searches the relevant fields in the googlesheets and generates the
        appropriate script commands.
        """
        primary_keys = []
        for sheet_key in self.gsheet.data.keys():
            tab = 'node{}'.format(self.gsheet.data[sheet_key][0])
            antrev_key, pol = sheet_key.split('-')
            ant, rev = cm_utils.split_part_key(antrev_key)
            # Process sheet data
            pdate = self.cdate + ''
            ptime = self.ctime + ''
            for i, col in enumerate(self.gsheet.header[tab]):
                if col in cm_gsheet.com_ignore or len(col) == 0:
                    continue
                try:
                    col_data = self.gsheet.data[sheet_key][i]
                except IndexError:
                    continue
                if len(col_data) == 0:
                    continue
                pkey, pdate, ptime = upd_util.get_unique_pkey(ant, rev, pdate, ptime, primary_keys)
                # ##Get prefix for entry
                if col in cm_gsheet.no_prefix:
                    prefix = ''
                elif col in cm_gsheet.pol_comments:
                    prefix = '{} {}: '.format(col, pol)
                else:
                    prefix = '{}: '.format(col)
                statement = '{}{}'.format(prefix, col_data)
                if not self.is_duplicate(ant, rev, statement):
                    self.hera.add_part_info(ant, rev, statement, pdate, ptime)
                    self.update_counter += 1
                    primary_keys.append(pkey)

    def is_duplicate(self, ant, rev, statement):
        return False

    def finish(self, keep_dated=False):
        """
        Process the command queue from the "add" functions above and write out the script.
        It writes a local script cm_script and if keep_dated writes a dated version to the
        output_script_path

        Parameters
        ----------
        keep_dated : bool
            If True, it will keep the dated version of the script in output_script_path
        output_script_path : str
            The relative path for the script files.
        """
        hera.done()
        script_filename = os.path.join(output_script_path, script_filename)
        mvcp = 'cp' if keep_dated else 'mv'
        print("Writing ./{}   ({})".format(self.com_script, mvcp))
        os.system('{} {} {}'.format(mvcp, script_filename, self.com_script))
