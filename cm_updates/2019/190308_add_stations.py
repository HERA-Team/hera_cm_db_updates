#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
hera.add_station(stn=228, ser_num=208, cdate='2019/02/28')
hera.add_station(stn=189, ser_num=209, cdate='2019/02/28')
hera.add_station(stn=190, ser_num=210, cdate='2019/02/28')
hera.add_station(stn=209, ser_num=211, cdate='2019/02/28')
hera.add_station(stn=210, ser_num=212, cdate='2019/02/28')


hera.done()
