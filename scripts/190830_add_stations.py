#! /usr/bin/env python
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0])

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
hera.add_antenna_station(stn=80, ser_num=265, cdate='2019/08/13')
hera.add_antenna_station(stn=97, ser_num=266, cdate='2019/08/13')
hera.add_antenna_station(stn=113, ser_num=267, cdate='2019/08/13')

hera.done()
