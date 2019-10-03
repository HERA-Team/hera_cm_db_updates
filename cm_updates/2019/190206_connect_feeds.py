#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys
import six

print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")

log_file = 'scripts.log'
do_it_this_time = True

feeds_to_add = [['A2', 'H', 'FDV8', 'A'],
                ['A11', 'H', 'FDV9', 'A'],
                ['A23', 'H', 'FDV11', 'A'],
                ['A24', 'H', 'FDV12', 'A'],
                ['A39', 'H', 'FDV14', 'A'],
                ['A88', 'H', 'FDV15', 'A'],
                ['A89', 'H', 'FDV16', 'A'],
                ['A90', 'H', 'FDV17', 'A'],
                ['A91', 'H', 'FDV18', 'A'],
                ['A104', 'H', 'FDV10', 'A'],
                ['A105', 'H', 'FDV19', 'A'],
                ['A106', 'H', 'FDV20', 'A'],
                ['A107', 'H', 'FDV21', 'A'],
                ['A108', 'H', 'FDV22', 'A'],
                ['A123', 'H', 'FDV23', 'A'],
                ['A124', 'H', 'FDV24', 'A'],
                ['A125', 'H', 'FDV25', 'A'],
                ['A126', 'H', 'FDV13', 'A']
                ]

fp = pc.init_script(sys.argv, log_file)

cdate = '2019/02/01'
ctime = '12:00'
for v in feeds_to_add:
    c = [[v[0], v[1], 'focus'], [v[2], v[3], 'input']]
    fp.write(pc.connect('add', c[0], c[1], cdate, ctime, do_it_this_time))
fp.close()
