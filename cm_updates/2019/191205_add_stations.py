#! /usr/bin/env python
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")

hera.add_antenna_station(stn=288, ser_num=287, cdate='2019/11/28')
hera.add_antenna_station(stn=289, ser_num=288, cdate='2019/11/29')
hera.add_antenna_station(stn=290, ser_num=290, cdate='2019/12/02')
hera.add_antenna_station(stn=291, ser_num=262, cdate='2019/12/03')
hera.add_antenna_station(stn=292, ser_num=275, cdate='2019/12/03')

hera.done()
