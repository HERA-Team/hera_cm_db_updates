# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
"""
import datetime
import os
from argparse import Namespace


def finish(arc_path, arc_script, cron_path, cron_script):
    """
    Close out process.
    """
    init_script_file = os.path.join(cron_path, arc_script)
    cron_script_file = os.path.join(cron_path, cron_script)
    if os.path.exists(cron_script_file):
        os.remove(cron_script_file)
    write_blank_cron_file = True
    if self.update_counter:
        if arc_path is not None:
            if self.verbose:
                print("Copying {}  -->  {}".format(init_script_file, arc_path))
                print("Renaming {}  -->  {}".format(init_script_file, cron_script_file))
            os.system('cp {} {}'.format(init_script_file, arc_path))
            os.rename(init_script_file, cron_script_file)
            write_blank_cron_file = False
    else:
        if self.verbose:
            print("Removing {}".format(init_script_file))
        os.remove(init_script_file)
    if write_blank_cron_file:
        with open(cron_script_file, 'w') as fp:
            fp.write('\n')
    os.chmod(cron_script_file, 0o755)


def get_num(val):
    """
    Makes digits in alphanumeric string into a number as string
    """
    return ''.join(c for c in val if c.isnumeric())


def get_bracket(input_string, bracket_type='{}'):
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


def parse_command_payload(col):
    """
    Parses the full command payload.
    """
    prefix, stmt, postfix = get_bracket(col, '{}')
    isstmt = prefix is not None
    edate = False
    prefix, entry, postfix = get_bracket(stmt, '[]')
    if prefix is not None:
        edate = entry
        entry = prefix
    return Namespace(isstmt=isstmt, entry=entry, date=edate)


def get_unique_pkey(hpn, rev, pdate, ptime, old_timers):
    """
    Generate unique info_pkey by advancing the time tag a second at a time if needed.
    """
    if ptime.count(':') == 1:
        ptime = ptime + ':00'
    pkey = '|'.join([hpn, rev, pdate, ptime])
    while pkey in old_timers:
        newdt = datetime.datetime.strptime('-'.join([pdate, ptime]), '%Y/%m/%d-%H:%M:%S') + datetime.timedelta(seconds=2)
        pdate = newdt.strftime('%Y/%m/%d')
        ptime = newdt.strftime('%H:%M:%S')
        pkey = '|'.join([hpn, rev, pdate, ptime])
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
    if ptype in ['SNP', 'SNAP']:
        return 'SNP{}{:06d}'.format(pnum[0], int(pnum[1:]))
    if ptype in ['PAM', 'FEM']:
        return '{}{:03d}'.format(ptype, int(pnum))
    if ptype in ['NODE', 'ND']:
        return 'N{:02d}'.format(int(pnum))
    if ptype in ['NBP']:
        return 'NBP{:02d}'.format(int(pnum))
    if ptype in ['FEED', 'FDV']:
        return 'FDV{}'.format(int(pnum))
    if ptype in ['ANT', 'ANTENNA']:
        return 'A{}'.format(int(pnum))
    return '{}{}'.format(ptype, pnum)
