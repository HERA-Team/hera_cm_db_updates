#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

parts_to_add = [
               [['FPS02', 'A', 'fem-power-supply', 'FPS02'], '2019/05/14', '12:00'],
               [['NCMC000196', 'A', 'node-control-module', 'C000196'], '2019/05/14', '12:00'],
               [['PCH02', 'A', 'pam-chassis', 'PCH02'], '2019/05/14', '12:00'],
               [['PAM036', 'A', 'post-amp', 'PAM036'], '2019/05/15', '12:00'],
               [['PAM037', 'A', 'post-amp', 'PAM037'], '2019/05/15', '12:00'],
               [['PAM038', 'A', 'post-amp', 'PAM038'], '2019/05/15', '12:00'],
               [['PAM039', 'A', 'post-amp', 'PAM039'], '2019/05/15', '12:00'],
               [['PAM040', 'A', 'post-amp', 'PAM040'], '2019/05/15', '12:00'],
               [['PAM041', 'A', 'post-amp', 'PAM041'], '2019/05/15', '12:00']
]
connections_to_add = [
                     [['PCH02', 'A', '@rack'], ['N9', 'A', '@loc0'], '2019/05/14', '12:30'],
                     [['PAM035', 'A', '@slot'], ['PCH02', 'A', '@slot1'], '2019/05/14', '12:30'],
                     [['PAM036', 'A', '@slot'], ['PCH02', 'A', '@slot2'], '2019/05/14', '12:30'],
                     [['PAM037', 'A', '@slot'], ['PCH02', 'A', '@slot3'], '2019/05/14', '12:30'],
                     [['PAM038', 'A', '@slot'], ['PCH02', 'A', '@slot4'], '2019/05/14', '12:30'],
                     [['PAM039', 'A', '@slot'], ['PCH02', 'A', '@slot5'], '2019/05/14', '12:30'],
                     [['PAM040', 'A', '@slot'], ['PCH02', 'A', '@slot6'], '2019/05/14', '12:30'],
                     [['PAM041', 'A', '@slot'], ['PCH02', 'A', '@slot7'], '2019/05/14', '12:30'],
                     [['PAM042', 'A', '@slot'], ['PCH02', 'A', '@slot8'], '2019/05/14', '12:30'],
                     [['PAM043', 'A', '@slot'], ['PCH02', 'A', '@slot9'], '2019/05/14', '12:30'],
                     [['PAM044', 'A', '@slot'], ['PCH02', 'A', '@slot10'], '2019/05/14', '12:30'],
                     [['PAM045', 'A', '@slot'], ['PCH02', 'A', '@slot11'], '2019/05/14', '12:30'],
                     [['PAM046', 'A', '@slot'], ['PCH02', 'A', '@slot12'], '2019/05/14', '12:30'],
                     [['NCMC000196', 'A', '@rack'], ['N9', 'A', '@loc5'], '2019/05/14', '12:30'],
                     [['FPS02', 'A', '@rack'], ['N9', 'A', '@loc6'], '2019/05/14', '12:30'],
                     [['FEM044', 'A', '@pwr'], ['FPS02', 'A', '@pwr9'], '2019/05/14', '12:30'],
                     [['FEM030', 'A', '@pwr'], ['FPS02', 'A', '@pwr10'], '2019/05/14', '12:30'],
                     [['FEM031', 'A', '@pwr'], ['FPS02', 'A', '@pwr1'], '2019/05/14', '12:30'],
                     [['FEM032', 'A', '@pwr'], ['FPS02', 'A', '@pwr8'], '2019/05/14', '12:30'],
                     [['FEM029', 'A', '@pwr'], ['FPS02', 'A', '@pwr12'], '2019/05/14', '12:30'],
                     [['FEM028', 'A', '@pwr'], ['FPS02', 'A', '@pwr11'], '2019/05/14', '12:30']
]

for part, cdate, ctime in parts_to_add:
    hera.update_part('add', part, cdate, ctime)

for up, down, cdate, ctime in connections_to_add:
    hera.update_connection('add', up, down, cdate, ctime)


hera.done()
