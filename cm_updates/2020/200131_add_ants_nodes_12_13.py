#! /usr/bin/env python
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)
override = {'date': None}

ser_num = {}
node = 12
ant = [176, 177, 178, 179, 135, 136, 155, 156, 157, 158]
feed = [101, 102, 103, 104, 96, 82, 97, 98, 99, 100]
fem = [160, 159, 149, 155, 150, 151, 152, 163, 161, 162]
nbp_port = [1, 2, 3, 4, 7, 8, 9, 10, 11, 12]

for i in range(len(ant)):
    hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2020/01/31',
                             ctime=['10:00', '11:00'], ser_num=ser_num, override=override)


node = 13
ant = [140, 141, 142, 160, 161, 162, 180, 181, 182, 183]
feed = [114, 117, 121, 118, 113, 122, 119, 120, 123, 109]
fem = [166, 164, 170, 172, 168, 165, 167, 169, 171, 182]
nbp_port = [7, 8, 9, 10, 1, 2, 11, 12, 3, 4]

for i in range(len(ant)):
    hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2020/01/31',
                             ctime=['10:00', '11:00'], ser_num=ser_num, override=override)

# node = 14
# ant = [144, 145, 163, 164, 165, 166, 184, 185, 186, 187]
# feed = [127, 111, 110, 106, 108, 105, 107, 125, 112, 115]
# fem = []
# nbp_port = []
#
# for i in range(len(ant)):
#     hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2020/01/31',
#                              ctime=['10:00', '11:00'], ser_num=ser_num, override=override)

hera.done()
