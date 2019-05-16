#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to start/stop parts/connections
connections_to_stop = [
                      [['FDV8', 'A', 'terminals'], ['FEM017', 'A', 'input'], '2019/05/13', '10:00'],
                      [['FEM017', 'A', 'e'], ['CRF002', 'A', 'ea'], '2019/05/13', '10:10'],
                      [['FEM017', 'A', 'n'], ['CRF002', 'A', 'na'], '2019/05/13', '10:10'],
                      [['FDV3', 'A', 'terminals'], ['FEM020', 'A', 'input'], '2019/05/13', '10:20'],
                      [['FEM020', 'A', 'e'], ['CRF012', 'A', 'ea'], '2019/05/13', '10:30'],
                      [['FEM020', 'A', 'n'], ['CRF012', 'A', 'na'], '2019/05/13', '10:30'],
                      [['FDV12', 'A', 'terminals'], ['FEM024', 'A', 'input'], '2019/05/13', '10:40'],
                      [['FEM024', 'A', 'e'], ['CRF024', 'A', 'ea'], '2019/05/13', '10:50'],
                      [['FEM024', 'A', 'n'], ['CRF024', 'A', 'na'], '2019/05/13', '10:50']
]
parts_to_add = [
               [['FEM040', 'A', 'front-end', '040'], '2019/05/13', '11:00'],
               [['FEM041', 'A', 'front-end', '041'], '2019/05/13', '11:00'],
               [['FEM043', 'A', 'front-end', '043'], '2019/05/13', '11:00'],
]
connections_to_add = [
                     [['FDV8', 'A', 'terminals'], ['FEM040', 'A', 'input'], '2019/05/13', '11:10'],
                     [['FEM040', 'A', 'e'], ['CRF002', 'A', 'ea'], '2019/05/13', '11:20'],
                     [['FEM040', 'A', 'n'], ['CRF002', 'A', 'na'], '2019/05/13', '11:20'],
                     [['FDV3', 'A', 'terminals'], ['FEM041', 'A', 'input'], '2019/05/13', '11:30'],
                     [['FEM041', 'A', 'e'], ['CRF012', 'A', 'ea'], '2019/05/13', '11:40'],
                     [['FEM041', 'A', 'n'], ['CRF012', 'A', 'na'], '2019/05/13', '11:40'],
                     [['FDV12', 'A', 'terminals'], ['FEM043', 'A', 'input'], '2019/05/13', '11:50'],
                     [['FEM043', 'A', 'e'], ['CRF024', 'A', 'ea'], '2019/05/13', '12:00'],
                     [['FEM043', 'A', 'n'], ['CRF024', 'A', 'na'], '2019/05/13', '12:00']
]

for up, down, cdate, ctime in connections_to_stop:
    hera.update_connection('stop', up, down, cdate, ctime)

for part, cdate, ctime in parts_to_add:
    hera.update_part('add', part, cdate, ctime)

for up, down, cdate, ctime in connections_to_add:
    hera.update_connection('add', up, down, cdate, ctime)

hera.done()
