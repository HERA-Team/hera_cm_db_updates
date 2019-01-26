#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys
import six

print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")

log_file = 'scripts.log'
do_it_this_time = True

year = '2018/'
stations_to_add = {'283': ['12/11', '195'],
                   '284': ['12/11', '196'],
                   '285': ['12/11', '197'],
                   '308': ['12/12', '198'],
                   '295': ['12/13', '199'],
                   '296': ['12/13', '200'],
                   '310': ['12/13', '201']
                   }

fp = pc.init_script(sys.argv, log_file)


def add_part(hpn, rev, htype, serno, cdate, ctime, do_it_this_time):
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))


ctime = '10:00'
for s, v in six.iteritems(stations_to_add):
    cdate = year + v[0]
    sn = v[1]
    fp.write('add_station.py {} --sernum {} --date {} --time {}\n'.format('HH' + s, sn, cdate, ctime))
for a, v in six.iteritems(stations_to_add):
    cdate = year + v[0]
    sn = v[1]
    add_part('A' + a, 'H', 'antenna', 'S/N' + sn, cdate, ctime, do_it_this_time)

ctime = '12:00'
for s, v in six.iteritems(stations_to_add):
    cdate = year + v[0]
    c = [['HH' + s, 'A', 'ground'], ['A' + s, 'H', 'ground']]
    fp.write(pc.connect('add', c[0], c[1], cdate, ctime, do_it_this_time))
fp.close()
