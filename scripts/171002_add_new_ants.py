#! /usr/bin/env python

from __future__ import print_function

log_file = 'scripts.log'
do_it_this_time = True

ants_to_add = [
              ['HH65', 'A5', 'S/N38', 'RI4A4', '2017/09/28'],
              ['HH66', 'A7', 'S/N39', 'RI4A5', '2017/09/28'],
              ['HH50', 'A12', 'S/N40', 'RI4A3', '2017/09/28'],
              ['HH82', 'A14', 'S/N41', 'RI4A6', '2017/09/28'],
              ['HH83', 'A15', 'S/N42', 'RI4A7', '2017/09/28'],
              ['HH98', 'A17', 'S/N43', 'RI4B1', '2017/09/28'],
              ['HH120', 'A21', 'S/N44', 'RI4B2', '2017/09/29'],
              ['HH122', 'A23', 'S/N45', 'RI4B4', '2017/09/29'],
              ['HH123', 'A24', 'S/N46', 'RI4B5', '2017/09/29'],
              ['HH143', 'A25', 'S/N47', 'RI4B8', '2017/09/29'],
]

fp = open('171002_add_new_ants', 'w')

s = 'echo 171002_add_new_parts >> {}\n'.format(log_file)
fp.write(s)


def part(p, cdate, ctime, do_it):
    s = 'add_part.py -p {} -r {} -t {} -m {} --date {} --time {}'.format(
        p[0], p[1], p[2], p[3], cdate, ctime)
    if do_it:
        s += ' --actually_do_it'
    s += '\n'
    return s


def connect(up, dn, cdate, ctime, do_it):
    s = 'add_connection.py -u {} --uprev {} --upport {} -d {} --dnrev {} --dnport {} --date {} --time {}'.format(
        up[0], up[1], up[2], dn[0], dn[1], dn[2], cdate, ctime)
    if do_it:
        s += ' --actually_do_it'
    s += '\n'
    return s


for a in ants_to_add:
    new_station = a[0]
    new_ant = 'A' + a[0][2:]
    new_feed = 'FD' + a[1]
    feed_mfg = 'P' + a[1][1:]
    new_frend = 'FE' + a[1]
    new_cable = 'C7F' + a[0][2:]
    new_rator = a[3]
    serno = a[2]
    cdate = a[4]
    ctime = '12:00'

    val_na = int(a[0][2:])

    s = 'add_station.py {}\n'.format(new_station)
    fp.write(s)
    fp.write(part([new_ant, 'H', 'antenna', serno], cdate, ctime, do_it_this_time))
    fp.write(part([new_feed, 'B', 'feed', feed_mfg], cdate, ctime, do_it_this_time))
    if val_na > 127:
        fp.write(part([new_cable, 'A', 'cable-feed75', new_cable], cdate, ctime, do_it_this_time))
    fp.write(connect([new_station, 'A', 'ground'], [new_ant, 'H', 'ground'], cdate, ctime, do_it_this_time))
    fp.write(connect([new_ant, 'H', 'focus'], [new_feed, 'B', 'input'], cdate, ctime, do_it_this_time))
    fp.write(connect([new_feed, 'B', 'terminals'], [new_frend, 'A', 'input'], cdate, ctime, do_it_this_time))
    fp.write(connect([new_frend, 'A', 'e'], [new_cable, 'A', 'ea'], cdate, ctime, do_it_this_time))
    fp.write(connect([new_frend, 'A', 'n'], [new_cable, 'A', 'na'], cdate, ctime, do_it_this_time))
    fp.write(connect([new_cable, 'A', 'eb'], [new_rator + 'E', 'A', 'a'], cdate, ctime, do_it_this_time))
    fp.write(connect([new_cable, 'A', 'nb'], [new_rator + 'N', 'A', 'a'], cdate, ctime, do_it_this_time))

fp.close()
