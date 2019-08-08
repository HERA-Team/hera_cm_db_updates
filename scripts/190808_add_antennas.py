#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0])

ant = 84
feed = 35
fem = 54
node = 8
nbp_port = 10
ser_num = {'node': 3}
hera.add_antenna_to_node(ant, feed, fem, node, nbp_port, cdate='2019/08/07', ctime=['10:00', '11:00'], ser_num={})

hera.done()
