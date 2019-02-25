#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
hera.add_station(stn=19, ser_num=28, cdate='2019/0')

# Sample to add part information
hera.add_part_info(hpn='PAMxxx', rev='A', note="testing", cdate="2019/0", ctime="10:00")

# Sample to add a full signal chain
hera.add_full(ant=2, feed=8, fem=17, pam=23, snap='C57', snap_input='e6,n4', cdate='2019/02/20')

# Sample to start/stop parts/connections
connections_to_stop = [
                      [['CRF001', 'A', 'nb'], ['PAM045', 'A', 'na'], '2019/03/00', '11:00']
]
parts_to_stop = [
                [['PAM028', 'A'], '2019/03/00', '11:30']
]
parts_to_add = [
               [['PAM034', 'A', 'post-amp', '034'], '2019/03/00', '12:00']
]
connections_to_add = [
                     [['CRF001', 'A', 'eb'], ['PAM024', 'A', 'ea'], '2019/02/23', '12:30']
]

for up, down, cdate, ctime in connections_to_stop:
    hera.update_connection('stop', up, down, cdate, ctime)

for part, cdate, ctime in parts_to_stop:
    hera.update_part('stop', part, cdate, ctime)

for part, cdate, ctime in parts_to_add:
    hera.update_part('add', part, cdate, ctime)

for up, down, cdate, ctime in connections_to_add:
    hera.update_connection('add', up, down, cdate, ctime)


hera.done()
