# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
This class generates the script to update comments and "apriori" info from the configuration
googlesheet
"""
from hera_mc import cm_utils, cm_active, mc

from . import cm_gsheet, signal_chain, util

import os
import datetime
from argparse import Namespace


class UpdateInfo:
    def __init__(self, exe_path='./', verbose=True):
        self.exe_path = exe_path
        self.verbose = verbose
        self.now = datetime.datetime.now()
        self.cdate = '{}/{:02d}/{:02d}'.format(self.now.year, self.now.month, self.now.day)
        self.ctime = '{:02d}:{:02d}'.format(self.now.hour, self.now.minute)
        self.script = '{}_sheetupdate_{}'.format(self.cdate.replace('/', '')[2:], self.ctime.replace(':', ''))
        self.hera = signal_chain.Update(self.script, output_script_path=exe_path, chmod=True, verbose=verbose)
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
                if self.verbose:
                    print("Updating {}   {}".format(E, self.active.apriori[key].status))
                self.hera.update_apriori(ant, E, self.cdate, self.ctime)
                self.update_counter += 1

    def add_sheet_notes(self, duplication_window=90.0):
        """
        Searches the relevant fields in the googlesheets and generates the
        appropriate script commands.

        Parameters
        ----------
        duplication_window : float
            time-frame in days over which to check for duplicate comments.
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
                pkey, pdate, ptime = util.get_unique_pkey(ant, rev, pdate, ptime, primary_keys)
                # ##Get prefix for entry
                if col in cm_gsheet.no_prefix:
                    prefix = ''
                elif col in cm_gsheet.pol_comments:
                    prefix = '{} {}: '.format(col, pol)
                else:
                    prefix = '{}: '.format(col)
                statement = '{}{}'.format(prefix, col_data)
                if not self.is_duplicate(antrev_key, statement, duplication_window):
                    if self.verbose:
                        print("Adding comment: {}:{} - {}".format(ant, rev, statement))
                    self.hera.add_part_info(ant, rev, statement, pdate, ptime)
                    self.update_counter += 1
                    primary_keys.append(pkey)

    def add_below_notes(self):
        print("ADD THE NOTES FROM BELOW THE TABLE")

    def is_duplicate(self, key, statement, duplication_window):
        if key in self.active.info.keys():
            for note in self.active.info[key]:
                note_time = cm_utils.get_astropytime(note.posting_gpstime).datetime
                dt = self.now - note_time
                ddays = dt.days + dt.seconds / (3600.0 * 24)
                if ddays < duplication_window and statement == note.comment:
                    if self.verbose:
                        print("Duplicate for {} - {}  ({:.1f} days)".format(key, statement, ddays))
                    return True
        return False

    def finish(self, arc_path, cron_script='sheet_update.sh'):
        """
        Close out process.
        """
        self.hera.done()
        apply_updates = self.update_counter > 0
        util.finish(apply_updates=apply_updates,
                    arc_path=arc_path, arc_script=self.script,
                    cron_path=self.exe_path, cron_script=cron_script,
                    verbose=self.verbose)
