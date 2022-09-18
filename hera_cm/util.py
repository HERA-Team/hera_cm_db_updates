# -*- mode: python; coding: utf-8 -*-
# Copyright 2022 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
"""
import datetime
import argparse


def include_this_line_in_log(line):
    if 'date' in line and 'time' in line:
        return True
    return False


command_args = {'add_part_info': [['-p', '--hpn',
                                   {'help': "HERA part number", 'default': None}],
                                  ['-r', '--rev',
                                   {'help': "Revision of part", 'default': "last"}],
                                  ['-c', '--comment',
                                   {'help': "Comment on part", 'default': None}],
                                  ['-l', '--reference',
                                   {'help': "Library filename", 'default': None}]],
                'add_part': [['-p', '--hpn',
                              {'help': "HERA part number", 'default': None}],
                             ['-r', '--rev',
                              {'help': "Revision of part", 'default': "last"}],
                             ['-t', '--hptype',
                              {'help': "HERA part type", 'default': None}],
                             ['-m', '--mfg',
                              {'help': "Manufacturers number for part", 'default': None}]
                             ],
                'stop_part': [['-p', '--hpn',
                               {'help': "HERA part number", 'default': None}],
                              ['-r', '--rev',
                               {'help': "Revision of part", 'default': "last"}]
                              ],
                'add_connection': [['-u', '--uppart',
                                    {'help': "Upstream part number", 'default': None}],
                                   ['--uprev',
                                    {'help': "Upstream part revision", 'default': None}],
                                   ['--upport',
                                    {'help': "Upstream output port", 'default': None}],
                                   ['-d', '--dnpart',
                                    {'help': "Downstream part number", 'default': None}],
                                   ['--dnrev',
                                    {'help': "Downstream part revision", 'default': None}],
                                   ['--dnport',
                                    {'help': "Downstream input port", 'default': None}],
                                   ],
                'stop_connection': [['-u', '--uppart',
                                     {'help': "Upstream part number", 'default': None}],
                                    ['--uprev',
                                     {'help': "Upstream part revision", 'default': None}],
                                    ['--upport',
                                     {'help': "Upstream output port", 'default': None}],
                                    ['-d', '--dnpart',
                                     {'help': "Downstream part number", 'default': None}],
                                    ['--dnrev',
                                     {'help': "Downstream part revision", 'default': None}],
                                    ['--dnport',
                                     {'help': "Downstream input port", 'default': None}],
                                    ],
                'update_apriori': [['-p', '--hpn',
                                    {'help': "HERA part number", 'default': None}],
                                   ['-s', '--status',
                                    {'help': "New apriori status", 'default': "last"}]
                                   ]
                }


arglist = ['hpn', 'hptype', 'comment', 'uppart', 'upport', 'dnpart', 'dnport', 'status']


def parse_log_line(line):
    from hera_mc import cm_utils
    import csv
    ap = argparse.ArgumentParser()
    command = line.split()[0].split('.')[0]
    try:
        cargs = command_args[command]
    except KeyError:
        return line + '\n'
    show_text = {}
    for ca in cargs:
        cnttyp = [type(x) for x in ca]
        if cnttyp.count(str) == 1:
            ap.add_argument(ca[0], **ca[1])
            show_text[ca[0].strip('-')] = ca[1]['help']
        elif cnttyp.count(str) == 2:
            ap.add_argument(ca[0], ca[1], **ca[2])
            show_text[ca[1].strip('-')] = ca[2]['help']
    cm_utils.add_date_time_args(ap)
    try:
        linarg = list(csv.reader([line.replace("'", '"')], delimiter=' '))
        argdict = vars(ap.parse_args(linarg[0][1:]))
    except:  # noqa
        return line + '\n'
    ret = f"-- {' '.join(command.split('_'))} -- {argdict['date']} {argdict['time']}\n"
    for key in arglist:
        if key in argdict and argdict[key] is not None:
            show = show_text[key]
            ret += f"\t{show}:  {argdict[key]}\n"
    return ret


def YMD_HM(dt, offset=0.0):
    dt += datetime.timedelta(offset)
    return dt.strftime('%Y/%m/%d'), dt.strftime('%H:%M')


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
    if isinstance(val, (int, float)):
        return str(val)
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
    return argparse.Namespace(isstmt=isstmt, entry=entry, date=edate)


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
    if pnum is None:
        return None
    ptype = ptype.upper()
    if isinstance(pnum, str):
        pnum = pnum.upper()
    try:
        number_part = int(get_num(pnum))
    except ValueError:
        return None
    if ptype in ['NBP/PAMloc', 'SNAPloc']:
        return number_part
    if ptype in ['SNP', 'SNAP']:
        snpletter = 'C'
        try:
            _ = int(pnum)
        except ValueError:
            snpletter = pnum[0]
        return f'SNP{snpletter}{number_part:06d}'
    if ptype in ['PAM', 'FEM']:
        return f'{ptype}{number_part:03d}'
    if ptype in ['NODESTATION']:
        return f'ND{number_part:02d}'
    if ptype in ['NODE', 'ND']:
        return f'N{number_part:02d}'
    if ptype in ['NBP']:
        return f'NBP{number_part:02d}'
    if ptype in ['FEED', 'FDV']:
        return f'FDV{number_part}'
    if ptype in ['ANT', 'ANTENNA']:
        return f'A{number_part}'
    if ptype in ['STATION']:
        from hera_mc.geo_sysdef import region
        if number_part in region['heraringa']:
            pre = 'HA'
        elif number_part in region['heraringb']:
            pre = 'HB'
        elif number_part > 9999:
            pre = 'EE'
        else:
            pre = 'HH'
        return f'{pre}{number_part}'
    if ptype in ['FPS']:
        return f'FPS{number_part:02d}'
    if ptype in ['PCH']:
        return f'PCH{number_part:02d}'
    if ptype in ['NCM']:
        return f'NCM{number_part:02d}'
