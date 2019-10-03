#! /usr/bin/env python
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add a station
print("Updates antennas per googlesheet https://docs.google.com/spreadsheets/d/16ZZSD_Wy30Kv_ax5csxlIiGDs5A8Sa8KhmK12LHvHsc/edit#gid=0")
hera.add_station(stn=261, ser_num=253, cdate='2019/07/01')
hera.add_station(stn=274, ser_num=254, cdate='2019/07/09')
hera.add_station(stn=301, ser_num=255, cdate='2019/07/09')
hera.add_station(stn=302, ser_num=256, cdate='2019/07/09')
hera.add_station(stn=303, ser_num=257, cdate='2019/07/09')
hera.add_station(stn=35, ser_num=258, cdate='2019/07/10')
hera.add_station(stn=48, ser_num=259, cdate='2019/07/11')
hera.add_station(stn=63, ser_num=260, cdate='2019/07/12')
hera.add_station(stn=49, ser_num=261, cdate='2019/07/15')
hera.add_station(stn=64, ser_num=262, cdate='2019/07/17')

hera.done()
