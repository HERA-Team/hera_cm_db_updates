#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys
import six

print("Updates antennas per googlesheet email")

log_file = 'scripts.log'
do_it_this_time = True

stations_to_add = {'8': ['2018/11/27', 139],
                   '9': ['2018/11/29', 148],
                   '20': ['2018/11/28', 142],
                   '21': ['2018/11/29', 149],
                   '31': ['2018/11/27', 140],
                   '32': ['2018/11/28', 143],
                   '33': ['2018/11/29', 150],
                   '45': ['2018/11/28', 144],
                   '46': ['2018/11/29', 151],
                   '59': ['2018/11/27', 141],
                   '60': ['2018/11/28', 145],
                   '76': ['2018/11/28', 146],
                   '93': ['2018/11/28', 147],
                   '94': ['2018/11/29', 152],
                   }

fp = pc.init_script(sys.argv, log_file)


def add_part(hpn, rev, htype, serno, cdate, ctime, do_it_this_time):
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))


ctime = '10:00'
for s, cdate in six.iteritems(stations_to_add):
    fp.write('add_station.py {} --date {} --time {}\n'.format('HH' + s, cdate[0], ctime))
for a, cdate in six.iteritems(stations_to_add):
    add_part('A' + a, 'H', 'antenna', 'S/N' + str(cdate[1]), cdate[0], ctime, do_it_this_time)

ctime = '12:00'
for s, cdate in six.iteritems(stations_to_add):
    c = [['HH' + s, 'A', 'ground'], ['A' + s, 'H', 'ground']]
    fp.write(pc.connect('add', c[0], c[1], cdate[0], ctime, do_it_this_time))
fp.close()
