#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

# Sample to add part information
hera.add_part_info(hpn='HH11', rev='A', note="Add braid on coax cable to feed", cdate="2019/03/12", ctime="10:00")
hera.add_part_info(hpn='HH23', rev='A', note="Add braid on coax cable to feed", cdate="2019/03/12", ctime="10:00")
hera.add_part_info(hpn='HH24', rev='A', note="Add braid on coax cable to feed", cdate="2019/03/12", ctime="10:00")
hera.add_part_info(hpn='HH39', rev='A', note="Add braid on coax cable to feed", cdate="2019/03/12", ctime="10:00")


hera.done()
