#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add part information
hera.add_part_info(hpn='HH1', rev='A', note="Ground springs to feed with solution 2", cdate="2019/03/18", ctime="10:00")
hera.add_part_info(hpn='HH11', rev='A', note="Ground springs to feed with solution 2", cdate="2019/03/18", ctime="10:00")
hera.add_part_info(hpn='HH13', rev='A', note="Ground springs to feed with solution 2", cdate="2019/03/18", ctime="10:00")
hera.add_part_info(hpn='HH39', rev='A', note="Ground springs to feed with solution 2", cdate="2019/03/19", ctime="10:00")


hera.done()
