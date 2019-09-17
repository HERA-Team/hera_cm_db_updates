#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Script to make a fake hookup for test purposes.
"""

from __future__ import absolute_import, division, print_function
from hera_mc import cm_utils
import signal_chain
import six

# ###########VALUES HERE##############
station = ['HH0', 'HH1', 'HH2']
antenna = ['A0', 'A1', 'A2']
feed = ['FDV1', 'FDV2', 'FDV8']
fem = ['FEM016', 'FEM018', 'FEM040']
nbp = [['NBP00', '1']]
# ####################################

part_add_time = int(cm_utils.get_astropytime(cdate, ctime).gps)

fake = signal_chain.Update(log_file=None)

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
