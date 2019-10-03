#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
hera.add_station(stn=148, ser_num=223, cdate='2019/03/20')
hera.add_station(stn=149, ser_num=224, cdate='2019/03/20')
hera.add_station(stn=170, ser_num=225, cdate='2019/03/20')
hera.add_station(stn=191, ser_num=226, cdate='2019/03/21')
hera.add_station(stn=211, ser_num=227, cdate='2019/03/23')


hera.done()
