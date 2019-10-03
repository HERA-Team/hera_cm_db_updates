#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0])

parts_to_add = [
               [['FEM038', 'A', 'front-end', 'FEM038'], '2019/09/01', '12:00'],
               [['FEM039', 'A', 'front-end', 'FEM039'], '2019/09/01', '12:00'],
               [['FEM035', 'A', 'front-end', 'FEM035'], '2019/09/01', '12:00'],
               [['FEM036', 'A', 'front-end', 'FEM036'], '2019/09/01', '12:00']
]
connections_to_add = [
                     [['FEM038', 'A', 'e'], ['NBP09', 'A', 'e3'], '2019/09/01', '12:30'],  # 88
                     [['FEM039', 'A', 'e'], ['NBP09', 'A', 'e2'], '2019/09/01', '12:30'],  # 90
                     [['FEM035', 'A', 'e'], ['NBP09', 'A', 'e6'], '2019/09/01', '12:30'],  # 91
                     [['FEM036', 'A', 'e'], ['NBP09', 'A', 'e4'], '2019/09/01', '12:30'],  # 105
                     [['FEM038', 'A', 'n'], ['NBP09', 'A', 'n3'], '2019/09/01', '12:30'],  # 88
                     [['FEM039', 'A', 'n'], ['NBP09', 'A', 'n2'], '2019/09/01', '12:30'],  # 90
                     [['FEM035', 'A', 'n'], ['NBP09', 'A', 'n6'], '2019/09/01', '12:30'],  # 91
                     [['FEM036', 'A', 'n'], ['NBP09', 'A', 'n4'], '2019/09/01', '12:30'],  # 105
                     [['FDV15', 'A', 'terminals'], ['FEM038', 'A', 'input'], '2019/09/01', '12:30'],  # 88
                     [['FDV17', 'A', 'terminals'], ['FEM039', 'A', 'input'], '2019/09/01', '12:30'],  # 90
                     [['FDV18', 'A', 'terminals'], ['FEM035', 'A', 'input'], '2019/09/01', '12:30'],  # 91
                     [['FDV19', 'A', 'terminals'], ['FEM036', 'A', 'input'], '2019/09/01', '12:30'],  # 105
                     [['PAM037', 'A', 'e'], ['SNPC000010', 'A', 'e10'], '2019/09/01', '12:30'],  # 88
                     [['PAM037', 'A', 'n'], ['SNPC000010', 'A', 'n8'], '2019/09/01', '12:30'],  # 88
                     [['PAM036', 'A', 'e'], ['SNPC000010', 'A', 'e6'], '2019/09/01', '12:30'],  # 90
                     [['PAM036', 'A', 'n'], ['SNPC000010', 'A', 'n4'], '2019/09/01', '12:30'],  # 90
                     [['PAM040', 'A', 'e'], ['SNPC000011', 'A', 'e10'], '2019/09/01', '12:30'],  # 91
                     [['PAM040', 'A', 'n'], ['SNPC000011', 'A', 'n8'], '2019/09/01', '12:30'],  # 91
                     [['PAM038', 'A', 'e'], ['SNPC000011', 'A', 'e2'], '2019/09/01', '12:30'],  # 105
                     [['PAM038', 'A', 'n'], ['SNPC000011', 'A', 'n0'], '2019/09/01', '12:30'],  # 105
]

for part, cdate, ctime in parts_to_add:
    hera.update_part('add', part, cdate, ctime)

for up, down, cdate, ctime in connections_to_add:
    hera.update_connection('add', up, down, cdate, ctime)


hera.done()
