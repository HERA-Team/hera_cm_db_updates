#! /usr/bin/env python

from hera_mc import cm_partconnect, mc, cm_utils
import os

db = mc.connect_to_mc_db(None)
session = db.sessionmaker()

start_gpstime = cm_utils.get_astropytime('2011/09/14', '01:46:25').gps

with open(os.path.join(mc.data_path, "HERA_350.txt"), 'r') as fp:
    for line in fp:
        ant = line.split()[0].strip()
        cm_partconnect.update_apriori_antenna(antenna=ant, status='not_connected', start_gpstime=start_gpstime, session=session)

g = {}

g[0] = [1188475218, 'passed_checks', [0, 1, 2, 11, 12, 13, 14, 23, 24, 25, 26, 27, 36, 37, 38, 39, 40, 41, 51, 52, 53, 54, 55, 65, 66, 67, 68, 69, 70, 71, 82, 83, 84, 85, 86, 87, 88, 98, 120, 121, 122, 123, 124, 141, 142, 143]]
g[1] = [1196769618, 'passed_checks', [136, 137, 138, 139, 140]]
g[2] = [1201509417, 'passed_checks', [99, 100, 101, 102, 103, 117, 118, 119]]
g[3] = [1201509417, 'known_bad', [68]]
g[4] = [1204416793, 'passed_checks', [81, 116]]

for _x in g.values():
    gstart = _x[0]
    gmsg = _x[1]
    for a in _x[2]:
        ant = 'HH{}'.format(a)
        cm_partconnect.update_apriori_antenna(antenna=ant, status=gmsg, start_gpstime=gstart, session=session)


start_gpstime = cm_utils.get_astropytime('2018/07/01', '12:00').gps

with open(os.path.join(mc.data_path, "HERA_350.txt"), 'r') as fp:
    for line in fp:
        ant = line.split()[0].strip()
        cm_partconnect.update_apriori_antenna(antenna=ant, status='not_connected', start_gpstime=start_gpstime, session=session)

start_gpstime = cm_utils.get_astropytime('2019/03/01', '12:00:00').gps
ants = ['HH0', 'HH1', 'HH2', 'HH11', 'HH12', 'HH13', 'HH23', 'HH24', 'HH25', 'HH26', 'HH30']

for a in ants:
    cm_partconnect.update_apriori_antenna(antenna=a, status='needs_checking', start_gpstime=start_gpstime, session=session)
