#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys
import six

print("Updates antennas per googlesheet email")

log_file = 'scripts.log'
do_it_this_time = True

stations_to_add = {'10': ['2018/12/03', 153],
                   '22': ['2018/12/03', 154],
                   '47': ['2018/12/03', 155],
                   '78': ['2018/12/03', 156],
                   '34': ['2018/12/03', 157],
                   '95': ['2018/12/03', 158]
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
