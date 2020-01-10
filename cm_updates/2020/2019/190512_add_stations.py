#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
hera.add_station(stn=268, ser_num=240, cdate='2019/05/03')
hera.add_station(stn=269, ser_num=241, cdate='2019/05/03')
hera.add_station(stn=167, ser_num=242, cdate='2019/02/21')

hera.done()
