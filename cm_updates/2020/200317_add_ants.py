#! /usr/bin/env python
"""Add antennas."""
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)
override = {'date': None}

ser_num = {}
node = 10
ant = [109, 112]
feed = [89, 81]
fem = [145, 144]
nbp_port = [4, 7]

for i in range(len(ant)):
    hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2020/02/12',
                             ctime=['10:00', '11:00'], ser_num=ser_num, override=override)


ser_num = {}
node = 14
ant = [165, 166, 184, 185, 186, 187, 163, 164, 143, 144, 145]
feed = [108, 105, 107, 125, 112, 115, 110, 106, 139, 127, 111]
fem = [181, 198, 180, 178, 184, 177,  173, 174, 175, 179, 183]
nbp_port = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

for i in range(len(ant)):
    hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2020/03/16',
                             ctime=['10:00', '11:00'], ser_num=ser_num, override=override)

hera.done()
