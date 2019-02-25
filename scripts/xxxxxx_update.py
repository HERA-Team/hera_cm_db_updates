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
connections_to_stop = []
parts_to_stop = []
parts_to_add = []
connections_to_add = [
                     [['CRF001', 'A', 'eb'], ['PAM024', 'A', 'ea'], '2019/02/23', '12:10'],
                     [['CRF001', 'A', 'nb'], ['PAM024', 'A', 'na'], '2019/02/23', '12:10'],
                     [['PAM024', 'A', 'eb'], ['SNPC000057', 'A', 'e10'], '2019/02/23', '12:10'],
                     [['PAM024', 'A', 'nb'], ['SNPC000057', 'A', 'n8'], '2019/02/23', '12:10']
]

for c in connections_to_stop:
    hera.update_connection('stop', c[0], c[1], c[2], c[3])

for p in parts_to_stop:
    hera.update_part('stop', p[0], p[1], p[2])

for p in parts_to_add:
    hera.update_part('add', p[0], p[1], p[2])

for c in connections_to_add:
    hera.update_connection('add', c[0], c[1], c[2], c[3])


hera.done()
