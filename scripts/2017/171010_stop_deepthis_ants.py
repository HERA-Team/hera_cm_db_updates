#! /usr/bin/env python

from __future__ import print_function

log_file = 'scripts.log'
do_it_this_time = True

ants_to_stop = [
               ['HH24', 'RI8B1', '2017/10/10'],
               ['HH25', 'RI8B2', '2017/10/10'],
               ['HH26', 'RI8B3', '2017/10/10'],
               ['HH27', 'RI8B4', '2017/10/10'],
               ['HH52', 'RI8A5', '2017/10/10'],
               ['HH53', 'RI8A6', '2017/10/10'],
               ['HH54', 'RI8A7', '2017/10/10'],
               ['HH55', 'RI5B3', '2017/10/10'],
               ['HH84', 'RI8A1', '2017/10/10'],
               ['HH85', 'RI8A2', '2017/10/10'],
               ['HH86', 'RI8A3', '2017/10/10'],
               ['HH87', 'RI8A4', '2017/10/10']
]

fp = open('171010_stop_deepthis_ants', 'w')

s = '#! /usr/bin/env bash\n'
fp.write(s)
s = 'echo 171010_stop_deepthis_ants >> {}\n'.format(log_file)
fp.write(s)


def disconnect(up, dn, cdate, ctime, do_it):
    s = 'stop_connection.py -u {} --uprev {} --upport {} -d {} --dnrev {} --dnport {} --date {} --time {}'.format(
        up[0], up[1], up[2], dn[0], dn[1], dn[2], cdate, ctime)
    if do_it:
        s += ' --actually_do_it'
    s += '\n'
    return s


for a in ants_to_stop:
    hhno = a[0][2:]
    cable = 'C7F' + hhno
    riE = a[1] + 'E'
    riN = a[1] + 'N'
    ctime = '15:00'
    cdate = a[2]

    fp.write(disconnect([cable, 'A', 'eb'], [riE, 'A', 'a'], cdate, ctime, do_it_this_time))
    fp.write(disconnect([cable, 'A', 'nb'], [riN, 'A', 'a'], cdate, ctime, do_it_this_time))

fp.close()
