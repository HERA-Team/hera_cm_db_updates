#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)

nodes = [28]
sns = ['2#22']
cdate = '2020/08/01'
for node, sn in zip(nodes, sns):
    sn = 'H0030-2601.' + sn
    hera.just_add_node(node, sn, cdate=cdate, ctime='10:00')

hera.done()
