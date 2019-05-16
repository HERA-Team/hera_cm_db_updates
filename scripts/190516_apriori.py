#! /usr/bin/env python

from hera_mc import cm_partconnect, mc, cm_utils
import os

db = mc.connect_to_mc_db(None)
session = db.sessionmaker()


start_gpstime = cm_utils.get_astropytime('2019/05/16', '12:00:00').gps
ants = ['HH89', 'HH106', 'HH107', 'HH124', 'HH125', 'HH126']

for a in ants:
    cm_partconnect.update_apriori_antenna(antenna=a, status='needs_checking', start_gpstime=start_gpstime, session=session)
