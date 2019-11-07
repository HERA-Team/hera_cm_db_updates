#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
"""
from hera_mc import cm_hookup, cm_utils, cm_sysutils, cm_sysdef, mc
import sheet_data as gsheet
import signal_chain

import os
import csv
import requests
import datetime
from argparse import Namespace

cm_req = Namespace(hpn=cm_sysdef.hera_zone_prefixes, pol='all',
                   at_date='now', exact_match=False, hookup_type=None)


def get_num(val):
    """
    Makes digits in alphanumeric string into a number as string
    """
    return ''.join(c for c in val if c.isnumeric())


def _get_bracket(input_string, bracket_type='{}'):
    """
    Breaks out stuff as <before, in, after>.
    If no starting bracket, it returns <None, input_string, None>
    Used in parse_stmt below.
    """
    start_ind = input_string.find(bracket_type[0])
    if start_ind == -1:
        return None, input_string, None
    end_ind = input_string.find(bracket_type[1])
    prefix = input_string[:start_ind].strip()
    statement = input_string[start_ind + 1: end_ind].strip()
    postfix = input_string[end_ind + 1:].strip()
    return prefix, statement, postfix


def parse_stmt(col):
    """
    Parses the full command payload.
    """
    prefix, stmt, postfix = _get_bracket(col, '{}')
    isstmt = prefix is not None
    edate = False
    prefix, entry, postfix = _get_bracket(stmt, '[]')
    if prefix is not None:
        edate = entry
        entry = prefix
    return Namespace(isstmt=isstmt, entry=entry, date=edate)


def get_info_pkey(ant, rev, pdate, ptime, old_timers):
    """
    Generate unique info_pkey by advancing the time tag a second at a time if needed.
    """
    if ptime.count(':') == 1:
        ptime = ptime + ':00'
    pkey = '|'.join([ant, rev, pdate, ptime])
    while pkey in old_timers:
        newdt = datetime.datetime.strptime('-'.join([pdate, ptime]), '%Y/%m/%d-%H:%M:%S') + datetime.timedelta(seconds=1)
        pdate = newdt.strftime('%Y/%m/%d')
        ptime = newdt.strftime('%H:%M:%S')
        pkey = '|'.join([ant, rev, pdate, ptime])
    return pkey, pdate, ptime


def get_row_dict(hdr, data):
    """
    Makes a dictionary providing mapping of column headers and column numbers to data.
    """
    row = {}
    for i, h in enumerate(hdr):
        row[h] = data[i]
        row[i] = data[i]
    return row


def gen_hpn(ptype, pnum):
    """
    From the sheet data (via ptype, pnum) it will generate a HERA Part Number
    """
    ptype = ptype.upper()
    if isinstance(pnum, str):
        pnum = pnum.upper()
    if ptype == 'SNP':
        return 'SNP{}{:06d}'.format(pnum[0], int(pnum[1:]))
    if ptype in ['PAM', 'FEM']:
        return '{}{:03d}'.format(ptype, int(pnum))
    return '{}{}'.format(ptype, pnum)


class Overview:
    pols = ['E', 'N']
    com_script = 'overview_update'  # name of processing script file
    NotFound = "Not Found"
    allowed_getlist = ['hookup', 'sheets', 'apriori']

    def __init__(self):
        # Start session
        db = mc.connect_to_mc_db(None)
        self.session = db.sessionmaker()
        self.commands = {}
        self.connected = []
        self.sheet_ants = []

    def get(self, getlist=['hookup', 'sheets', 'apriori']):
        for gl in getlist:
            if gl in self.allowed_getlist:
                getattr(self, 'get_' + gl)()
            else:
                print("{} get method not found.".format(gl))

    def get_hookup(self):
        """
        Gets the hookup data from the hera_mc database.
        """
        self.hookup = cm_hookup.Hookup(self.session)
        self.hookup_dict = self.hookup.get_hookup(hpn=cm_req.hpn, pol=cm_req.pol, at_date=cm_req.at_date,
                                                  exact_match=cm_req.exact_match, hookup_type=cm_req.hookup_type)
        self.all = cm_utils.put_keys_in_order(list(self.hookup_dict.keys()), sort_order='NPR')
        self.connected = []
        for ant in self.hookup_dict.keys():
            for pol in self.pols:
                for ppkey in self.hookup_dict[ant].fully_connected.keys():
                    if ppkey.upper().startswith(pol.upper()):
                        break
                if self.hookup_dict[ant].fully_connected[ppkey]:
                    self.connected.append(ant)
                    break
        self.connected = cm_utils.put_keys_in_order(self.connected, sort_order='NPR')

    def get_sheets(self):
        """
        Gets the googlesheet information from the internet
        """
        self.sheet_data = {}
        self.sheet_header = {}
        self.sheet_date = {}
        self.sheet_ants = set()
        self.tabs = sorted(list(gsheet.gsheet.keys()))
        for tab in self.tabs:
            xxx = requests.get(gsheet.gsheet[tab])
            csv_tab = b''
            for line in xxx:
                csv_tab += line
            csv_tab = csv.reader(csv_tab.decode('utf-8').splitlines())
            for data in csv_tab:
                if data[0].startswith('Ant'):
                    self.sheet_header[tab] = ['Node'] + data
                    continue
                elif data[0].startswith('Date:'):
                    self.sheet_date[tab] = data[1]
                    break
                try:
                    antnum = int(data[0])
                except ValueError:
                    continue
                hpn = gen_hpn('HH', antnum)
                hkey = cm_utils.make_part_key(hpn, 'A')
                self.sheet_ants.add(hkey)
                dkey = '{}-{}'.format(hkey, data[1].upper())
                self.sheet_data[dkey] = [get_num(tab)] + data
        self.sheet_ants = cm_utils.put_keys_in_order(list(self.sheet_ants), sort_order='NPR')

    def get_apriori(self):
        """
        Gets the apriori status information from the hera_mc database.  Must be after
        get_sheet
        """
        sys = cm_sysutils.Handling(self.session)
        self.apriori_data = {}
        use_keys = set(self.connected + self.sheet_ants)
        for antkey in use_keys:
            hh = antkey.split(':')[0]
            self.apriori_data[antkey] = sys.get_apriori_status_for_antenna(hh, at_date=cm_req.at_date)

    def add_mismatch_commands(self, add_hookup=True, add_apriori=True):
        """
        Add commands to self.commands to handle the mismatch data found between the googlesheet and the database.

        Parameters
        ----------
        add_hookup : bool
            Flag to include hookup mismatches
        add_apriori : bool
            Flag to includes apriori mismatches
        """
        for key, data in self.mismatches.items():
            antrev_key, pol = key.split('-')
            ant, rev = antrev_key.split(':')
            self.commands.setdefault(antrev_key, [])
            entry_date = data['date']
            if '-' not in entry_date:
                entry_date = entry_date + '-12:00:00'
            for payload in data['diff']:
                command_code = None
                if payload[0] in ['PAM', 'FEM', 'SNAP']:
                    if payload[0] == 'SNAP':
                        payload[0] = 'SNP'
                    prefix = '{}'.format(payload[0])
                    if payload[1] == self.NotFound:
                        command_code = 'ADD'
                        stmt = '{}'.format(payload[2])
                    else:
                        command_code = 'SWAP'
                        stmt = '{}:{}'.format(payload[1], payload[2])
                elif payload[0] == 'APriori':
                    command_code = 'APRIORI'
                    prefix = ''
                    stmt = payload[2]
                add_it = (command_code is not None) and\
                         (add_apriori and command_code == 'APRIORI') or\
                         (add_hookup and command_code != 'APRIORI')
                if add_it:
                    stmt = '{}|{}{}|{}'.format(command_code, prefix, stmt, entry_date)
                    if stmt not in self.commands[antrev_key]:
                        self.commands[antrev_key] = self.commands[antrev_key] + [stmt]
            if not len(self.commands[antrev_key]):
                del self.commands[antrev_key]

    def add_sheet_commands(self):
        """
        Searches the relevant fields in the googlesheets and generates the
        appropriate script commands.
        """
        for sheet_key in self.sheet_data.keys():
            tab = 'node{}'.format(self.sheet_data[sheet_key][0])
            antrev_key, pol = sheet_key.split('-')
            header = {}
            # Sort out header entries (if any)
            for col in self.sheet_header[tab]:
                header[col] = parse_stmt(col)
            # Process sheet data
            for i, col in enumerate(self.sheet_header[tab]):
                if header[col].entry in gsheet.com_ignore or len(col) == 0:
                    continue
                try:
                    col_data = self.sheet_data[sheet_key][i]
                except IndexError:
                    continue
                entry = parse_stmt(col_data)
                if not (header[col].isstmt or entry.isstmt):
                    continue  # Nothing to process.
                # ##Get date for entry
                entry_date = self.sheet_date[tab]  # Defaults to page date
                if header[col].date:
                    entry_date = header[col].date
                if entry.date:
                    entry_date = entry.date
                if '-' not in entry_date:
                    entry_date = entry_date + '-12:00'
                # ##Get prefix for entry
                if header[col].entry in gsheet.no_prefix:
                    prefix = ''
                elif col in gsheet.pol_comments:
                    prefix = '{} {}: '.format(col, pol)
                else:
                    prefix = '{}: '.format(col)
                # ##Process Action
                if header[col].entry == 'Actions':
                    _x = [a.strip() for a in entry.entry.split('|')]
                    command_code, stmt = _x if len(_x) == 2 else ['INFO', _x[0]]
                else:
                    command_code = 'INFO'
                    stmt = entry.entry
                if len(stmt):
                    self.commands.setdefault(antrev_key, [])
                    self.commands[antrev_key].append('{}|{}{}|{}'.format(command_code, prefix, stmt, entry_date))

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

    def compare(self, antkeys='sheet'):
        """
        Compares the hookup data with the spreadsheet.  Writes self.mismatches

        Parameters
        ----------
        antkeys : csv-str or list or ('all', 'connected', 'sheet')
            Antenna keys to display.  If None displays 'sheet'
        """
        if isinstance(antkeys, str):
            if antkeys.lower() == 'all':
                antkeys = self.all
            elif antkeys.lower() == 'connected':
                antkeys = self.connected
            elif antkeys.lower() == 'sheet':
                antkeys = self.sheet_ants
            else:
                antkeys = antkeys.split(',')
        self.mismatches = {}
        for antkey in antkeys:
            for pol in self.pols:
                sheet_key = "{}-{}".format(antkey, pol)
                tab = 'node{}'.format(self.sheet_data[sheet_key][0])
                header = self.sheet_header[tab]
                sheet_row = get_row_dict(header, self.sheet_data[sheet_key])
                for i, col in enumerate(header):
                    val = self._get_val_from_cmdb(antkey, pol, col)
                    if val is not None:
                        sheet_val = self.sheet_data[sheet_key][i]
                        if val.upper() != sheet_val.upper():
                            if val != self.NotFound or len(sheet_val.strip()):
                                self.mismatches.setdefault(sheet_key, {'sheet': sheet_row,
                                                                       'diff': [], 'date': self.sheet_date[tab]})
                                self.mismatches[sheet_key]['diff'].append([col, val, sheet_val])

    def _get_val_from_cmdb(self, antkey, pol, sheet_col):
        """
        Bunch of ad hoc stuff to map the hookup_dict to the googlesheet column for comparison.
        """
        if sheet_col not in gsheet.hu_col.keys():
            return None
        if sheet_col == 'APriori':
            if antkey in self.apriori_data.keys():
                return self.apriori_data[antkey]
            else:
                return None
        hu = self.hookup_dict[antkey]
        pol = pol.upper()
        for ppkey in hu.hookup.keys():
            if ppkey.upper().startswith(pol.upper()):
                break
        try:
            pam_slot = get_num(hu.hookup[ppkey][gsheet.hu_col['Bulkhead-PAM_Slot']].downstream_input_port)
        except IndexError:
            return self.NotFound
        try:
            snap_slot = str(int(get_num(hu.hookup[ppkey][gsheet.hu_col['Node']].downstream_input_port)))
        except IndexError:
            return self.NotFound
        i2c = (int(pam_slot) + 2) % 3 + 1

        if sheet_col == 'I2C_bus':
            return str(i2c)
        if sheet_col == 'Bulkhead-PAM_Slot':
            return pam_slot
        if sheet_col == 'SNAP_Slot':
            return snap_slot
        if sheet_col == 'Port' or sheet_col == 'Pol':
            try:
                return hu.hookup[ppkey][gsheet.hu_col[sheet_col]].downstream_input_port.upper()
            except IndexError:
                return self.NotFound
        if sheet_col == 'APriori':
            return self.apriori_data[antkey]

        try:
            part = hu.hookup[ppkey][gsheet.hu_col[sheet_col]].downstream_part
        except IndexError:
            return self.NotFound
        num = str(int(get_num(part)))

        if sheet_col == 'SNAP':
            return "{}{}".format(part[3], num)

        return num

    def process_commands(self, keep_dated=False, output_script_path='../cm_updates/'):
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
        today = datetime.datetime.now()
        sdate = '{}{:02d}{:02d}'.format(str(today.year)[2:], today.month, today.day)
        script_filename = '{}_{}_{:02d}{:02d}'.format(sdate, self.com_script, today.hour, today.minute)
        hera = signal_chain.Update(script_filename, output_script_path=output_script_path, chmod=True)
        primary_keys = {'INFO': []}
        for antkey, commands in self.commands.items():
            ant, rev = antkey.split(':')
            for payload in commands:
                command, statement, dtmp = payload.split('|')
                pdate, ptime = dtmp.split('-')
                if command == 'INFO':
                    pkey, pdate, ptime = get_info_pkey(ant, rev, pdate, ptime, primary_keys['INFO'])
                    hera.add_part_info(ant, rev, statement, pdate, ptime)
                    primary_keys['INFO'].append(pkey)
                elif command == 'SWAP' or command == 'REPLACE':
                    ptype, old_num, new_num = statement.split(':')
                    old_one = [gen_hpn(ptype, old_num), 'A']
                    new_one = [gen_hpn(ptype, new_num), 'A']
                    if command == 'REPLACE':
                        hera.replace(new_one, None, pdate, ptime)
                    hera.replace(old_one, new_one, pdate, ptime)
                elif command == 'APRIORI':
                    hera.update_apriori(ant, statement, pdate, ptime)
                elif command == 'ADD':
                    hera.to_implement(command, ant, rev, statement, pdate, ptime)
                else:
                    print("UNKOWN COMMAND------>", payload)
        hera.done()
        script_filename = os.path.join(output_script_path, script_filename)
        mvcp = 'cp' if keep_dated else 'mv'
        print("Writing ./{}   ({})".format(self.com_script, mvcp))
        os.system('{} {} {}'.format(mvcp, script_filename, self.com_script))
