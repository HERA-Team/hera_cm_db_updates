#! /usr/bin/env python
import sys
sys.path.insert(1, '../hera_cm')
import signal_chain

hera = signal_chain.Update(sys.argv[0])

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
hera.add_antenna_station(stn=114, ser_num=268, cdate='2019/09/09')

hera.done()
