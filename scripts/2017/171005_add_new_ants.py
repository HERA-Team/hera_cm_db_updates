#! /usr/bin/env python

from __future__ import print_function

log_file = 'scripts.log'
do_it_this_time = True

ants_to_add = [
              ['HH121', 'A26', 'S/N48', 'RI4B2', '2017/10/05', 'NRAO'],
              ['HH124', 'A27', 'S/N49', 'RI4B5', '2017/10/05', 'NRAO'],
              ['HH141', 'A28', 'S/N50', 'RI4B6', '2017/10/05', 'NRAO'],
              ['HH142', 'A32', 'S/N51', 'RI4B7', '2017/10/05', 'NRAO'],
              ['HH88', 'A34', 'S/N52', 'RI5B8', '2017/10/05', 'FEM75034']
]

fp = open('171005_add_new_ants', 'w')

s = 'echo 171005_add_new_ants >> {}\n'.format(log_file)
fp.write(s)


def part(p, cdate, ctime, do_it):
    s = 'add_part.py -p {} -r {} -t {} -m {} --date {} --time {}'.format(
        p[0], p[1], p[2], p[3], cdate, ctime)
    if do_it:
        s += ' --actually_do_it'
    s += '\n'
    return s


def fem(ano, fno, cdate, ctime, do_it):
    s = 'fem_swap.py -a {} -f {} --rev A --date {} --time {}'.format(ano, fno, cdate, ctime)
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
    hhno = a[0][2:]
    new_ant = 'A' + hhno
    new_feed = 'FD' + a[1]
    feed_mfg = 'P' + a[1][1:]
    new_frend = 'FE' + a[1]
    new_cable = 'C7F' + hhno
    new_rator = a[3]
    chain_type = a[5]
    serno = a[2]
    cdate = a[4]
    ctime = '10:00'

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
    if chain_type[:3] == 'FEM':
        fp.write(fem(hhno, chain_type[3:], cdate, ctime, do_it_this_time))


fp.close()
