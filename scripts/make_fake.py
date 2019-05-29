#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Script to make a fake hookup for test purposes.
"""

from __future__ import absolute_import, division, print_function
from hera_mc import cm_sysdef, cm_utils
import signal_chain
import six

# ###########VALUES HERE##############
ant = 706
feed = 714
fem = 721
bulkhead = 4
pam = 727
snap = 'Z64'
snap_input = 'e2,n0'
snap_loc = 2
node = 700
cdate = '2019/02/20'
ctime = '10:00'
# ####################################

part_add_time = int(cm_utils.get_astropytime(cdate, ctime).gps)

fake = signal_chain.Update(log_file=None)
parts, connections = fake.add_full(ant=ant, feed=feed, fem=fem, bulkhead=bulkhead, pam=pam, snap=snap, snap_input=snap_input,
                                   snap_loc=snap_loc, node=node, cdate=cdate, include_HH=True, include_ND=True)
print("Cut-and-paste into test 'initialization_data_parts.csv'")
print("-------------------------------------------------------\n")
for p, x in six.iteritems(parts):
    print('{},{},{},{},{},'.format(x[0], x[1], x[2], x[3], part_add_time))
print("\n-------------------------------------------------------\n")

print("Cut-and-paste into test 'initialization_data_connections.csv'")
print("-------------------------------------------------------------\n")
for c in connections:
    conn_add_time = int(cm_utils.get_astropytime(c[2], c[3]).gps)
    print("{},{},{},{},{},{},{},".format(c[0][0], c[0][1], c[1][0], c[1][1], c[0][2], c[1][2], conn_add_time))
print("\n-------------------------------------------------------------")
