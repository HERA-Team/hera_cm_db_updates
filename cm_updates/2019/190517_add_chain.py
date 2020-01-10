#! /usr/bin/env python
import sys
import signal_chain


hera = signal_chain.Update(sys.argv[0], do_it=True)

hera.add_full(ant=108, feed=22, fem=33, pam=39, snap='C11', snap_input='e6,n4', snap_loc='1', node='9', cdate='2019/05/17')

hera.done()
