#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
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


def get_bracket(input_string, bracket_type='{}'):
    start_ind = input_string.find(bracket_type[0])
    if start_ind == -1:
        return '', ''
    end_ind = input_string.find(bracket_type[1])
    statement = input_string[start_ind + 1: end_ind]
    output_string = input_string[end_ind + 1:]
    return statement, output_string


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

    def process_commands(self):
        import signal_chain
        import datetime
        today = datetime.datetime.now()
        script_filename = '{}{:02d}{:02d}_overview_update_{:02d}{:02d}'.format(today.year, today.month, today.day, today.hour, today.minute)
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
        hu_keys = list(sd.hu_col.keys())
        for sheet_key in self.sheet_data.keys():
            tab = 'node{}'.format(self.sheet_data[sheet_key][0])
            antrev_key, pol = sheet_key.split('-')
            for i, col in enumerate(self.sheet_header[tab]):
                if col in hu_keys or col.startswith('History') or len(col) == 0:
                    continue
                try:
                    col_data = self.sheet_data[sheet_key][i]
                except IndexError:
                    continue
                header_flag = '{' in col and '}' in col
                entry_flag = '{' in col_data and '}' in col_data
                if not (header_flag or entry_flag):
                    continue
                entry_date = self.sheet_date[tab]
                if '{' in col:
                    col = col.strip('{').strip('}')
                    if '[' in col:
                        entry_date, x = get_bracket(col, bracket_type='[]')
                        col = col.split('[')[0].strip()
                if col.startswith('Comment') or col.startswith('Action'):
                    prefix = ''
                elif col in sd.pol_comments:
                    prefix = '{} {}: '.format(col, pol)
                else:
                    prefix = '{}: '.format(col)

                col_data_list = []
                stmt = '--'
                while len(stmt):
                    if entry_flag:
                        stmt, col_data = get_bracket(col_data)
                    else:
                        stmt = col_data
                    if len(stmt):
                        if '[' in stmt:
                            entry_date, x = get_bracket(stmt, bracket_type='[]')
                            stmt = stmt.split('[')[0].strip()
                        if col.startswith('Action'):
                            command_code = stmt.split('|')[0]
                            try:
                                entry_date = stmt.split('|')[2]
                            except IndexError:
                                pass
                            stmt = stmt.split('|')[1]
                        else:
                            command_code = 'INFO'
                        if '-' not in entry_date:
                            entry_date = entry_date + '-12:00'
                        stmt = '{}|{}{}|{}'.format(command_code, prefix, stmt, entry_date)
                        col_data_list.append(stmt)
                    if not entry_flag:
                        break

                self.commands.setdefault(antrev_key, [])
                self.commands[antrev_key] = self.commands[antrev_key] + col_data_list

    def get_sheets(self):
        # ############################ Get previous sheet ############################
        self.sheet_data = {}
        self.sheet_header = {}
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
            for pol in ['E', 'N']:
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
        if sheet_col not in list(sd.hu_col.keys()):
            return None
        hu = self.hookup_dict[antkey]
        pol = pol.lower()
        pam_slot = get_num(hu.hookup[pol][sd.hu_col['PAM Slot']].downstream_input_port)
        snap_slot = str(int(get_num(hu.hookup[pol][sd.hu_col['Node']].downstream_input_port)))
        i2c = (int(pam_slot) + 2) % 3 + 1

        if sheet_col == 'I2C_bus':
            return str(i2c)
        if sheet_col == 'PAM Slot':
            return pam_slot
        if sheet_col == 'SNAP Slot':
            return snap_slot
        if sheet_col == 'Port' or sheet_col == 'Pol':
            return hu.hookup[pol][sd.hu_col[sheet_col]].downstream_input_port.upper()
        if sheet_col == 'APriori':
            return self.apriori_data[antkey]

        part = hu.hookup[pol][sd.hu_col[sheet_col]].downstream_part
        num = str(int(get_num(part)))

        if sheet_col == 'SNAP':
            return "{}{}".format(part[3], num)

        return num
