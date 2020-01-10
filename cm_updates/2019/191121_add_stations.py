#! /usr/bin/env python
import sys
sys.path.insert(1, '../hera_cm')
import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")

hera.add_antenna_station(stn=249, ser_num=279, cdate='2019/9/6')
hera.add_antenna_station(stn=232, ser_num=280, cdate='2019/9/6')
hera.add_antenna_station(stn=213, ser_num=281, cdate='2019/10/22')
hera.add_antenna_station(stn=154, ser_num=282, cdate='2019/11/4')
hera.add_antenna_station(stn=175, ser_num=283, cdate='2019/11/5')
hera.add_antenna_station(stn=214, ser_num=284, cdate='2019/11/6')
hera.add_antenna_station(stn=174, ser_num=285, cdate='2019/11/7')
hera.add_antenna_station(stn=194, ser_num=286, cdate='2019/11/7')

hera.done()
