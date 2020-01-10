#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
hera.add_station(stn=135, ser_num=222, cdate='2019/03/14')
hera.add_station(stn=146, ser_num=221, cdate='2019/03/13')
hera.add_station(stn=147, ser_num=220, cdate='2019/03/13')
hera.add_station(stn=168, ser_num=217, cdate='2019/02/15')
hera.add_station(stn=169, ser_num=218, cdate='2019/02/15')
hera.add_station(stn=188, ser_num=219, cdate='2019/02/15')


hera.done()
