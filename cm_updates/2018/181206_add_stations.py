#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys
import six

print("Updates antennas per googlesheet")

log_file = 'scripts.log'
do_it_this_time = True

year = '2018/'
stations_to_add = {'61': ['12/04', 207],
                   '62': ['12/04', 208],
                   '77': ['12/04', 209]
                   }

fp = pc.init_script(sys.argv, log_file)


def add_part(hpn, rev, htype, serno, cdate, ctime, do_it_this_time):
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))


ctime = '10:00'
for s, v in six.iteritems(stations_to_add):
    cdate = year + v[0]
    fp.write('add_station.py {} --date {} --time {}\n'.format('HH' + s, cdate, ctime))
for a, v in six.iteritems(stations_to_add):
    cdate = year + v[0]
    sn = 'S/N' + str(v[1])
    add_part('A' + a, 'H', 'antenna', 'S/N' + sn, cdate, ctime, do_it_this_time)

ctime = '12:00'
for s, v in six.iteritems(stations_to_add):
    cdate = year + v[0]
    c = [['HH' + s, 'A', 'ground'], ['A' + s, 'H', 'ground']]
    fp.write(pc.connect('add', c[0], c[1], cdate, ctime, do_it_this_time))
fp.close()
