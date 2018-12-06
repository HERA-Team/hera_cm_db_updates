#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys
import six

print("Updates antennas per googlesheet")

log_file = 'scripts.log'
do_it_this_time = True

year = '2018/'
stations_to_add = {'4': ['11/21', 159],
                   '5': ['11/21', 160],
                   '6': ['11/23', 161],
                   '7': ['11/26', 162],
                   '16': ['11/21', 163],
                   '17': ['11/23', 164],
                   '18': ['11/23', 165],
                   '19': ['11/22', 166],
                   '29': ['11/21', 167],
                   '30': ['11/21', 168],
                   '43': ['11/22', 169],
                   '44': ['11/22', 170],
                   '75': ['11/20', 171],
                   '92': ['11/20', 172],
                   '107': ['11/20', 173],
                   '108': ['11/20', 174],
                   '126': ['11/19', 175],
                   '145': ['11/19', 176],
                   '157': ['11/12', 177],
                   '158': ['11/12', 178],
                   '159': ['11/13', 179],
                   '160': ['11/13', 180],
                   '161': ['11/13', 181],
                   '162': ['11/14', 182],
                   '163': ['11/14', 183],
                   '164': ['11/15', 184],
                   '165': ['11/19', 185],
                   '206': ['11/16', 206]
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
