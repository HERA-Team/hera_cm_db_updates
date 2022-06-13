#! /usr/bin/env python

# -*- mode: python; coding: utf-8 -*-
# Copyright 2022 the HERA Collaboration
# Licensed under the 2-clause BSD license.

import argparse
from tabulate import tabulate
from node_control import hosts_ethers
from hera_cm import cm_gsheet

ap = argparse.ArgumentParser()
ap.add_argument('hosts', help="Name of hosts file.")
ap.add_argument('ethers', help="Name of ethers file.")
ap.add_argument('-c', '--check-mac', dest='check_mac', action='store_true',
                help='Flag to indicate different mac addresses')
args = ap.parse_args()


def he(key, ethers, hosts):
    try:
        e = ethers.by_alias[key]
    except KeyError:
        e = ''
    try:
        hlist = hosts.by_id[hosts.by_alias[key]]
        if hlist[-1].startswith('hera'):
            h = hlist[-1]
        else:
            h = '-'
    except KeyError:
        h = ''
    return e, h


ncms = cm_gsheet.SheetData()
ncms.load_ncm()


hosts = hosts_ethers.HostsEthers(args.hosts)
ethers = hosts_ethers.HostsEthers(args.ethers)

header = ['NCM', 'arduino', 'mac', 'mac (ethers)', 'node (hosts)', ' ',
          'white-rabbit', 'mac', 'mac (ethers)', 'node (hosts)']
table = []
for ncm in sorted(ncms.ncm.keys()):
    x = ncms.ncm[ncm]
    row = [ncm, x.rd, x.rdmac]
    this_e, this_h = he(x.rd, ethers, hosts)
    if args.check_mac and x.rdmac.lower() != this_e.lower():
        this_e = f"**{this_e}**"
    row += [this_e, this_h]
    row += ['|', x.wr, x.wrmac]
    this_e, this_h = he(x.wr, ethers, hosts)
    if args.check_mac and x.wrmac.lower() != this_e.lower():
        this_e = f"**{this_e}**"
    row += [this_e, this_h]
    table.append(row)
print(tabulate(table, headers=header))
