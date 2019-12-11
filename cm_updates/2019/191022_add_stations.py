#! /usr/bin/env python
import sys
sys.path.insert(1, '../hera_cm')
import signal_chain

hera = signal_chain.Update(sys.argv[0])

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")

hera.add_antenna_station(stn=115, ser_num=269, cdate='2019/10/14')
hera.add_antenna_station(stn=131, ser_num=270, cdate='2019/10/14')
hera.add_antenna_station(stn=132, ser_num=271, cdate='2019/10/15')
hera.add_antenna_station(stn=133, ser_num=272, cdate='2019/10/15')
hera.add_antenna_station(stn=151, ser_num=273, cdate='2019/10/15')
hera.add_antenna_station(stn=134, ser_num=274, cdate='2019/10/16')
hera.add_antenna_station(stn=152, ser_num=275, cdate='2019/10/17')
hera.add_antenna_station(stn=153, ser_num=276, cdate='2019/10/17')
hera.add_antenna_station(stn=171, ser_num=277, cdate='2019/10/18')
hera.add_antenna_station(stn=172, ser_num=278, cdate='2019/10/18')

hera.done()
