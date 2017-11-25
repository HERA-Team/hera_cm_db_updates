#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import sys
import def_pc as pc

log_file = 'scripts.log'
do_it_this_time = True

connections_to_stop = [
                      [['C7F142', 'A', 'eb'], ['RI4B7E', 'A', 'a'], '2017/11/19'],
                      [['C7F142', 'A', 'nb'], ['RI4B7N', 'A', 'a'], '2017/11/19'],
                      [['FEA32', 'A', 'e'], ['C7F142', 'A', 'ea'], '2017/11/19'],
                      [['FEA32', 'A', 'n'], ['C7F142', 'A', 'na'], '2017/11/19'],
                      [['FDA32', 'B', 'terminals'], ['FEA32', 'A', 'input'], '2017/11/19']
]
connections_to_strt = [
                      [['FDA32', 'B', 'terminals'], ['FEM75041', 'A', 'input'], '2017/11/23'],
                      [['FEM75041', 'A', 'e'], ['C7F142', 'A', 'ea'], '2017/11/23'],
                      [['FEM75041', 'A', 'n'], ['C7F142', 'A', 'na'], '2017/11/23'],
                      [['C7F142', 'A', 'eb'], ['RI3A6E', 'A', 'a'], '2017/11/23'],
                      [['C7F142', 'A', 'nb'], ['RI3A6N', 'A', 'a'], '2017/11/23'],
                      [['RI3A6E', 'A', 'b'], ['PAM75122', 'B', 'ea'], '2017/11/23'],
                      [['RI3A6N', 'A', 'b'], ['PAM75122', 'B', 'na'], '2017/11/23'],
                      [['PAM75122', 'B', 'eb'], ['RO3A6E', 'A', 'b'], '2017/11/23'],
                      [['PAM75122', 'B', 'nb'], ['RO3A6N', 'A', 'b'], '2017/11/23']
]
fems_to_add = ['75041']
pams_to_add = ['75122']
cdate = '2017/11/23'
ctime = '9:00'

fp = pc.init_script(sys.argv, log_file)
for f in fems_to_add:
    hpn = 'FEM' + f
    rev = 'A'
    htype = 'front-end'
    serno = f
    part = [hpn, rev, htype, serno]
    fp.write(pc.part(part, cdate, ctime, do_it_this_time))
for p in pams_to_add:
    hpn = 'PAM' + p
    rev = 'B'
    htype = 'post-amp'
    serno = p
    part = [hpn, rev, htype, serno]
    fp.write(pc.part(part, cdate, ctime, do_it_this_time))
for c in connections_to_stop:
    fp.write(pc.connect('stop', c[0], c[1], c[2], ctime, do_it_this_time))

for c in connections_to_strt:
    fp.write(pc.connect('add', c[0], c[1], c[2], ctime, do_it_this_time))

fp.close()
