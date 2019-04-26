#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
print("note that this gets some older antennas, so serial numbers are somewhat out of sequence")
hera.add_station(stn=110, ser_num=228, cdate='2019/02/18')
hera.add_station(stn=208, ser_num=229, cdate='2019/02/19')
hera.add_station(stn=226, ser_num=230, cdate='2019/02/19')
hera.add_station(stn=227, ser_num=231, cdate='2019/02/19')
hera.add_station(stn=244, ser_num=232, cdate='2019/02/19')
hera.add_station(stn=109, ser_num=233, cdate='2019/02/20')
hera.add_station(stn=187, ser_num=234, cdate='2019/02/20')
hera.add_station(stn=207, ser_num=235, cdate='2019/02/20')
hera.add_station(stn=166, ser_num=236, cdate='2019/02/21')
hera.add_station(stn=111, ser_num=237, cdate='2019/04/25')
hera.add_station(stn=112, ser_num=238, cdate='2019/04/25')
hera.add_station(stn=150, ser_num=239, cdate='2019/04/25')

nextstations = [261, 229, 245, 246, 247]

hera.done()
