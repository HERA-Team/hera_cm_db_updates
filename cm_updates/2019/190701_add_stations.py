#! /usr/bin/env python
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
hera.add_station(stn=246, ser_num=245, cdate='2019/06/26')
hera.add_station(stn=247, ser_num=246, cdate='2019/06/26')
hera.add_station(stn=271, ser_num=247, cdate='2019/06/26')
hera.add_station(stn=272, ser_num=248, cdate='2019/06/26')
hera.add_station(stn=273, ser_num=249, cdate='2019/06/26')
hera.add_station(stn=287, ser_num=250, cdate='2019/06/26')
hera.add_station(stn=300, ser_num=251, cdate='2019/06/26')
hera.add_station(stn=245, ser_num=252, cdate='2019/06/28')

hera.done()
