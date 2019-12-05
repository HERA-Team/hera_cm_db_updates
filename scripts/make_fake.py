#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Script to make a fake hookup for test purposes.
"""
from hera_mc import cm_utils
from hera_cm import signal_chain
from argparse import Namespace

# ###########VALUES HERE##############
cofa = 'COFA_FAKE,cofa,WGS84,34J,6601181,541007,1051.69,'
node = 'ND700,node,WGS84,34J,6601162.28,540868.96,1050.0,'
geo_loc = 'herahexw,WGS84,34J,6601070.74,540901.6,1052.63'
stations = [700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712]
A = Namespace(node=700, fps=700, pch=700, ncm=700,
              pams=[701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712],
              snaps=['A000701', 'B000702', 'C000703', 'D000704'])
cdate = '2019/01/01'
ctime = ['10:00', '11:00']
# ####################################
part_add_time = str(int(cm_utils.get_astropytime(cdate, ctime[0]).gps))

fake = signal_chain.Update('make_fake', log_file=None)

added_stn = {}
added_ant = {}
for i, stn in enumerate(stations):
    added_stn[stn] = fake.add_antenna_station(stn, stn, cdate, ctime[0])
    added_ant[stn] = fake.add_antenna_to_node(ant=stn, feed=stn, fem=stn, node=A.node, nbp_port=i,
                                              cdate=cdate, ctime=ctime)
added_node = fake.add_node(node=A.node, fps=A.fps, pch=A.pch, ncm=A.ncm, pams=A.pams,
                           snaps=A.snaps, cdate=cdate, ctime=ctime)

print("Cut-and-paste into test 'initialization_geolocation.csv'")
print(">-----------------------------------------------------<\n")
print(cofa + part_add_time)
print(node + part_add_time)
for stn in stations:
    for addstn in added_stn[stn]['station']:
        print(','.join([addstn[0], geo_loc, addstn[1]]))
print("\n>-----------------------------------------------------<\n\n\n")

print("Cut-and-paste into test 'initialization_data_parts.csv'")
print(">-----------------------------------------------------<\n")
for stn in stations:
    for addprt in added_stn[stn]['part']:
        print(','.join(addprt))
for addprt in added_node['part']:
    print(','.join(addprt))
for ant in stations:
    for addprt in added_ant[ant]['part']:
        print(','.join(addprt))
print("\n>---------------------------------------------------<\n\n\n")

print("Cut-and-paste into test 'initialization_data_connections.csv'")
print(">-----------------------------------------------------------<\n")
for stn in stations:
    for addconn in added_stn[stn]['connection']:
        print(','.join(addconn))
for addconn in added_node['connection']:
    print(','.join(addconn))
for ant in stations:
    for addconn in added_ant[ant]['connection']:
        print(','.join(addconn))
print("\n>-----------------------------------------------------------<\n\n\n")
