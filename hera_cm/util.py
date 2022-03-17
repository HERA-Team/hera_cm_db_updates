# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
"""
import datetime
from argparse import Namespace


def compare_lists(list1, list2, info=None, ignore_length=True):
    """
    Make sure the lists agree.  If ignore_length, then check
    as far as length of list1
    """
    if not ignore_length:
        if len(list1) != len(list2):
            print("List lengths differ")
        return False

    are_same = True
    for i, l1 in enumerate(list1):
        if l1 != list2[i]:
            if info is not None:
                print(info)
            print("\t{} and {} are not the same".format(l1, list2[i]))
            are_same = False
    return are_same


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
        newdt = datetime.datetime.strptime('-'.join([pdate, ptime]),
                                           '%Y/%m/%d-%H:%M:%S') + datetime.timedelta(seconds=2)
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


def gen_hpn(ptype, pnum, verbose=False):
    """
    From the sheet data (via ptype, pnum) etc it will generate a HERA Part Number
    """
    ptype = ptype.upper()
    if isinstance(pnum, str):
        pnum = pnum.upper()
    try:
        if ptype in ['SNP', 'SNAP']:
            snpletter = 'C'
            try:
                snpnum = int(pnum)
            except ValueError:
                snpletter = pnum[0]
                snpnum = int(pnum[1:])
            return 'SNP{}{:06d}'.format(snpletter, snpnum)
        if ptype in ['PAM', 'FEM']:
            return '{}{:03d}'.format(ptype, int(pnum))
        if ptype in ['NODE-STATION']:
            return 'ND{:02d}'.format(int(pnum))
        if ptype in ['NODE', 'ND']:
            return 'N{:02d}'.format(int(pnum))
        if ptype in ['NBP']:
            return 'NBP{:02d}'.format(int(pnum))
        if ptype in ['FEED', 'FDV']:
            return 'FDV{}'.format(int(pnum))
        if ptype in ['ANT', 'ANTENNA']:
            return 'A{}'.format(int(pnum))
        if ptype in ['STATION']:
            HA = [325, 326, 327, 330, 334, 338, 331, 335, 339, 342, 343, 344]
            HB = [320, 321, 322, 323, 324, 328, 329, 333, 337, 332, 336, 340,
                  341, 345, 346, 347, 348, 349]
            if int(pnum) in HA:
                pre = 'HA'
            elif int(pnum) in HB:
                pre = 'HB'
            else:
                pre = 'HH'
            return '{}{}'.format(pre, int(pnum))
        if ptype in ['FPS']:
            return 'FPS{:02d}'.format(int(pnum))
        if ptype in ['PCH']:
            return 'PCH{:02d}'.format(int(pnum))
        if ptype in ['NCM']:
            return 'NCM{:02d}'.format(int(pnum))
    except ValueError:
        if verbose:
            print("ValueError:  util.gen_hpn:  Invalid pnum '{}'".format(pnum))
        return None
    except IndexError:
        if verbose:
            print("IndexError:  util.gen_hpn:  Invalid pnum '{}'".format(pnum))
        return None
    return '{}{}'.format(ptype, pnum)
