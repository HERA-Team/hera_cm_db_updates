# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.
"""
This class sets up to update the part information database.
"""
from hera_mc import cm_utils, cm_active
from . import cm_gsheet, util, upd_base


class UpdateInfo(upd_base.Update):
    """Generates the script to update comments and "apriori" info from the configuration gsheet."""

    def __init__(self, script_nom='infoupd', script_path='./', verbose=True):
        """Init of base."""
        super(UpdateInfo, self).__init__(script_nom=script_nom, script_path=script_path,
                                         verbose=verbose)

    def load_active(self):
        """Load active data."""
        self.active = cm_active.ActiveData()
        self.active.load_info()
        self.active.load_apriori()

    def add_apriori(self):
        """Write out for apriori differences."""
        self.new_apriori = {}
        for key in self.gsheet.ants:
            ap_col = self.gsheet.header[self.gsheet.ant_to_node[key]].index('APriori')
            E = self.gsheet.data[key + '-E'][ap_col]
            N = self.gsheet.data[key + '-N'][ap_col]
            ant, rev = cm_utils.split_part_key(key)
            if E != N:
                print("{} and {} should be the same.".format(E, N))
                continue
            if len(E) == 0:
                continue
            if E != self.active.apriori[key].status:
                self.new_apriori[key] = "{} -> {}".format(E, self.active.apriori[key].status)
                if self.verbose:
                    print("Updating {}   {}".format(E, self.active.apriori[key].status))
                self.hera.update_apriori(ant, E, self.cdate, self.ctime)
                self.update_counter += 1

    def add_sheet_notes(self, duplication_window=90.0, view_duplicate=0.0):
        """
        Search the relevant fields in the googlesheets and generate appropriate script commands.

        Parameters
        ----------
        duplication_window : float
            time-frame in days over which to check for duplicate comments.
        """
        primary_keys = []
        self.new_notes = {}
        for sheet_key in self.gsheet.data.keys():
            antrev_key, pol = sheet_key.split('-')
            ant, rev = cm_utils.split_part_key(antrev_key)
            tab = self.gsheet.ant_to_node[antrev_key]
            # Process sheet data
            pdate = self.cdate + ''
            ptime = self.ctime + ''
            for i, col in enumerate(self.gsheet.header[tab]):
                if col in cm_gsheet.hu_col.keys() or not len(col) or col == 'APriori':
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
                else:
                    prefix = '{}: '.format(col)
                statement = '{}{}'.format(prefix, col_data)
                if "'" in statement:
                    statement = statement.replace("'", "")
                if not self.is_duplicate(antrev_key, statement, duplication_window, view_duplicate):
                    self.new_notes.setdefault(antrev_key, [])
                    self.new_notes[antrev_key].append(statement)
                    if self.verbose:
                        print("Adding comment: {}:{} - {}".format(ant, rev, statement))
                    self.hera.add_part_info(ant, rev, statement, pdate, ptime, ref='infoupd')
                    self.update_counter += 1
                    primary_keys.append(pkey)

    def add_below_notes(self):
        """Need to do this."""
        print("ADD THE NOTES FROM BELOW THE TABLE")

    def is_duplicate(self, key, statement, duplication_window, view_duplicate=0.0):
        """Check if duplicate."""
        if key in self.active.info.keys():
            for note in self.active.info[key]:
                note_time = cm_utils.get_astropytime(note.posting_gpstime).datetime
                dt = self.now - note_time
                ddays = dt.days + dt.seconds / (3600.0 * 24)
                if ddays < duplication_window and statement == note.comment:
                    node = self.gsheet.ant_to_node[key]
                    if self.verbose and ddays > view_duplicate:
                        print("Duplicate for {:8s}  ({}) - {}  ({:.1f} days)"
                              .format(key, node, statement, ddays))
                    return True
        return False

    def view_info(self):
        """View it."""
        if len(self.new_apriori.keys()):
            print("New Apriori")
            for x, info in sorted(self.new_apriori.items()):
                print("{}:  {}".format(x, info))
        else:
            print("No new apriori")
        if len(self.new_notes.keys()):
            print("New Notes")
            for x, info in sorted(self.new_notes.items()):
                print("{}:  {}".format(x, info))
        else:
            print("No new notes")
