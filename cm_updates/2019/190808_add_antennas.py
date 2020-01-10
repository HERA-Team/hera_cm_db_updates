#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0])

ser_num = {'node': 3}
node = 8

ant = [84, 85, 86, 87, 101, 102, 103, 104, 120, 121, 122, 123]
feed = [35, 36, 37, 38, 39, 40, 41, 10, 42, 43, 44, 45]
fem = [54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]
nbp_port = [10, 2, 3, 7, 8, 1, 6, 5, 4, 12, 9, 11]

for i in range(len(ant)):
    hera.add_antenna_to_node(ant[i], feed[i], fem[i], node, nbp_port[i], cdate='2019/08/07', ctime=['10:00', '11:00'], ser_num={})

hera.done()
