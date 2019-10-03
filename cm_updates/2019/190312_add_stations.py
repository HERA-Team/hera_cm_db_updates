#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
hera.add_station(stn=130, ser_num=213, cdate='2019/03/06')
hera.add_station(stn=129, ser_num=214, cdate='2019/03/07')
hera.add_station(stn=127, ser_num=215, cdate='2019/03/08')
hera.add_station(stn=128, ser_num=216, cdate='2019/03/08')


hera.done()
