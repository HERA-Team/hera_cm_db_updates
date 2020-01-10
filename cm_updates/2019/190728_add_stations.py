#! /usr/bin/env python
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
hera.add_station(stn=79, ser_num=263, cdate='2019/07/18')
hera.add_station(stn=96, ser_num=264, cdate='2019/07/19')

hera.done()
