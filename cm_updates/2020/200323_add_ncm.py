#! /usr/bin/env python
"""Add wr and arduinos."""
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)

hera.update_part('add', ['NCM11', 'A', 'node-control-module', 'NCM-Pro11'],
                 cdate='2020/03/01', ctime='10:00')
hera.update_part('add', ['NCM12', 'A', 'node-control-module', 'NCM-Pro12'],
                 cdate='2020/03/01', ctime='10:00')
hera.update_part('add', ['NCM15', 'A', 'node-control-module', 'NCM-Pro15'],
                 cdate='2020/03/20', ctime='10:00')
hera.update_part('add', ['NCM16', 'A', 'node-control-module', 'NCM-Pro16'],
                 cdate='2020/03/20', ctime='10:00')
hera.done()
