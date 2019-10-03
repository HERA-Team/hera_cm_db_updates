#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
"""
from __future__ import absolute_import, division, print_function

from hera_mc import cm_hookup, cm_utils, cm_sysutils, cm_handling, mc
import sheet_data as gsheet

import os
import csv
import requests
from argparse import Namespace

hu_testing = cm_utils.default_station_prefixes

_rq = Namespace(hpn=hu_testing, pol='all', at_date='now', exact_match=False,
                force_new_cache=True, force_db=False, hookup_type=None)


def get_num(val):
    return ''.join(c for c in val if c.isnumeric())


def get_bracket(input_string, bracket_type='{}'):
    """
    Breaks out stuff as <before, in, after>.
    If no starting bracket, it returns <None, input_string, None>
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
    prefix, stmt, postfix = get_bracket(col, '{}')
    isstmt = prefix is not None
    edate = False
    prefix, entry, postfix = get_bracket(stmt, '[]')
    if prefix is not None:
        edate = entry
        entry = prefix
    return Namespace(isstmt=isstmt, entry=entry, date=edate)


def increment_time(pkey, old_timers):
    while pkey in old_timers:
        _time = pkey.split('|')[-1]
        hr = int(_time.split(':')[0])
        mn = int(_time.split(':')[1])
        try:
            sc = int(_time.split(':')[2])
        except IndexError:
            sc = 0
        sc = sc + 1
        if sc == 60:
            sc = 0
            mn += 1
        _time = '{:02d}:{:02d}:{:02d}'.format(hr, mn, sc)
        pkey = '{}|{}'.format('|'.join(pkey.split('|')[0:3]), _time)
    return _time


class Overview:
    pols = ['E', 'N']

    def __init__(self):
        # Start session
        db = mc.connect_to_mc_db(None)
        self.session = db.sessionmaker()
        self.commands = {}
        self.get_hookup()
        self.get_apriori()
        self.get_sheets()
        self.get_part_info()

    def get_hookup(self):
        """
        Gets the hookup data from the hera_mc database.
        """
        self.hookup = cm_hookup.Hookup(self.session)
        self.hookup_dict = self.hookup.get_hookup(hpn=_rq.hpn, pol=_rq.pol, at_date=_rq.at_date,
                                                  exact_match=_rq.exact_match, hookup_type=_rq.hookup_type)
        self.connected = []
        for ant in self.hookup_dict.keys():
            for pol in self.pols:
                for ppkey in self.hookup_dict[ant].fully_connected.keys():
                    if ppkey.upper().startswith(pol.upper()):
                        break
                if self.hookup_dict[ant].fully_connected[ppkey]:
                    self.connected.append(ant)
                    break
        self.connected = cm_utils.put_keys_in_order(self.connected)

    def get_apriori(self):
        """
        Gets the apriori status information from the hera_mc database
        """
        sys = cm_sysutils.Handling(self.session)
        self.apriori_data = {}
        for antkey in self.connected:
            hh = antkey.split(':')[0]
            self.apriori_data[antkey] = sys.get_apriori_status_for_antenna(hh, at_date=_rq.at_date)

    def get_sheets(self):
        """
        Gets the googlesheet information from the internet
        """
        self.sheet_data = {}
        self.sheet_header = {}
        self.sheet_date = {}
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
                key = 'HH{}:A-{}'.format(antnum, data[1].upper())
                self.sheet_data[key] = [get_num(tab)] + data

    def get_part_info(self):
        """
        Gets the part_info information from the hera_mc database
        """
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

    def process_commands(self):
        import signal_chain
        import datetime
        today = datetime.datetime.now()
        syr = str(today.year)[2:]
        script_filename = '{}{:02d}{:02d}_overview_update_{:02d}{:02d}'.format(syr, today.month, today.day, today.hour, today.minute)
        hera = signal_chain.Update(script_filename)
        primary_keys = {'INFO': []}
        for antkey, commands in self.commands.items():
            ant, rev = antkey.split(':')
            for payload in commands:
                command, statement, dtmp = payload.split('|')
                _date, _time = dtmp.split('-')
                if command == 'INFO':
                    pkey = '{}|{}|{}|{}'.format(ant, rev, _date, _time)
                    if pkey in primary_keys['INFO']:
                        _time = increment_time(pkey, primary_keys['INFO'])
                    hera.add_part_info(ant, rev, statement, _date, _time)
                    pkey = '{}|{}|{}|{}'.format(ant, rev, _date, _time)
                    primary_keys['INFO'].append(pkey)
                elif command == 'SWAP' or command == 'REPLACE':
                    ptype, old_num, new_num = statement.split(':')
                    if ptype == 'SNP':
                        old_one = ['SNP{}{:06d}'.format(old_num[0], int(old_num[1:])), 'A']
                        new_one = ['SNP{}{:06d}'.format(new_num[0], int(new_num[1:])), 'A']
                    else:
                        old_one = ['{}{:03d}'.format(ptype, int(old_num)), 'A']
                        new_one = ['{}{:03d}'.format(ptype, int(new_num)), 'A']
                    if command == 'SWAP':
                        hera.replace(new_one, None, _date, _time)
                    hera.replace(old_one, new_one, _date, _time)
                elif command == 'APRIORI':
                    hera.update_apriori(ant, statement, _date, _time)
                elif command == 'ADD':
                    print('NOADD ', command, ant, rev, statement, _date, _time)
                else:
                    print("UNKOWN COMMAND------>", payload)
        hera.done()

    def get_mismatch_commands(self):
        for key, data in self.mismatches.items():
            antrev_key, pol = key.split('-')
            ant, rev = antrev_key.split(':')
            self.commands.setdefault(antrev_key, [])
            entry_date = data['date']
            if '-' not in entry_date:
                entry_date = entry_date + '-12:00'
            for payload in data['diff']:
                if payload[0] in ['PAM', 'FEM', 'SNAP']:
                    command_code = 'SWAP'
                    if payload[0] == 'SNAP':
                        payload[0] = 'SNP'
                    prefix = '{}:'.format(payload[0])
                    stmt = '{}:{}'.format(payload[1], payload[2])
                elif payload[0] == 'APriori':
                    command_code = 'APRIORI'
                    prefix = ''
                    stmt = payload[2]
                else:
                    command_code = 'TEST'
                    prefix = 'Test'
                    stmt = '---'

                stmt = '{}|{}{}|{}'.format(command_code, prefix, stmt, entry_date)
                if stmt in self.commands[antrev_key]:
                    continue
                self.commands[antrev_key] = self.commands[antrev_key] + [stmt]

    def get_sheet_commands(self):
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
                if header[col].entry == 'Action':
                    _x = [a.strip() for a in entry.entry.split('|')]
                    command_code, stmt = _x if len(_x) == 2 else ['INFO', _x[0]]
                else:
                    command_code = 'INFO'
                    stmt = entry.entry
                if len(stmt):
                    self.commands.setdefault(antrev_key, [])
                    self.commands[antrev_key].append('{}|{}{}|{}'.format(command_code, prefix, stmt, entry_date))

    def compare(self, antkeys=None, output='mismatch'):
        """
        Compares the hookup data with the spreadsheet.

        Parameters
        ----------
        antkeys : csv-str, list or None (or 'all')
            Antenna keys to display.  If None displays all, as it does if 'all'
        output : str {'mismatch', 'all', 'none', None, False}
            What to print out as it processes.

        Returns
        -------
        list
            List of mismatches
        """
        # ################### Check that cm and googlesheet match ##############
        if antkeys is None or (isinstance(antkeys, str) and antkeys.lower() == 'all'):
            antkeys = self.connected
        elif not isinstance(antkeys, list):
            antkeys = antkeys.split(',')
        self.mismatches = {}
        if not output:
            output = 'none'
        if output.startswith('all'):
            show_hyphens = True
        else:
            show_hyphens = False
        for antkey in antkeys:
            for pol in self.pols:
                if show_hyphens:
                    print("------------------")
                if output.startswith('mis'):
                    show_hyphens = False
                sheet_key = "{}-{}".format(antkey, pol)
                tab = 'node{}'.format(self.sheet_data[sheet_key][0])
                for i, col in enumerate(self.sheet_header[tab]):
                    val = self.__get_val_from_cmdb(antkey, pol, col)
                    if val is not None:
                        indicator = ''
                        sheet_val = self.sheet_data[sheet_key][i]
                        if val.upper() != sheet_val.upper():
                            self.mismatches.setdefault(sheet_key, {'sheet': self.sheet_data[sheet_key], 'diff': [], 'date': self.sheet_date[tab]})
                            self.mismatches[sheet_key]['diff'].append([col, val, sheet_val])
                            indicator = '****'
                            if output.startswith('mis'):
                                show_hyphens = True
                                print("{}:  {}   <--->   {}  {}".format(col, val, sheet_val, self.sheet_data[sheet_key]))
                        if output.startswith('all'):
                            print("{}{}:  {}   <--->   {}{}".format(indicator, col, sheet_val, val, indicator))

    def __get_val_from_cmdb(self, antkey, pol, sheet_col):
        """
        Bunch of ad hoc stuff to map the hookup_dict to the googlesheet column
        """
        if sheet_col not in gsheet.hu_col.keys():
            return None
        hu = self.hookup_dict[antkey]
        pol = pol.upper()
        for ppkey in hu.hookup.keys():
            if ppkey.upper().startswith(pol.upper()):
                break
        pam_slot = get_num(hu.hookup[ppkey][gsheet.hu_col['Bulkhead-PAM_Slot']].downstream_input_port)
        snap_slot = str(int(get_num(hu.hookup[ppkey][gsheet.hu_col['Node']].downstream_input_port)))
        i2c = (int(pam_slot) + 2) % 3 + 1

        if sheet_col == 'I2C_bus':
            return str(i2c)
        if sheet_col == 'Bulkhead-PAM_Slot':
            return pam_slot
        if sheet_col == 'SNAP_Slot':
            return snap_slot
        if sheet_col == 'Port' or sheet_col == 'Pol':
            return hu.hookup[ppkey][gsheet.hu_col[sheet_col]].downstream_input_port.upper()
        if sheet_col == 'APriori':
            return self.apriori_data[antkey]

        part = hu.hookup[ppkey][gsheet.hu_col[sheet_col]].downstream_part
        num = str(int(get_num(part)))

        if sheet_col == 'SNAP':
            return "{}{}".format(part[3], num)

        return num
