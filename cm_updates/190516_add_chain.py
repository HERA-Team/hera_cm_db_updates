#! /usr/bin/env python
import sys
import signal_chain


hera = signal_chain.Update(sys.argv[0], do_it=True)

hera.add_full(ant=89, feed=16, fem=44, pam=43, snap='C13', snap_input='e10,n8', snap_loc='2', node='9', cdate='2019/05/16')
hera.add_full(ant=124, feed=24, fem=32, pam=42, snap='C13', snap_input='e6,n4', snap_loc='2', node='9', cdate='2019/05/16', dont_add_part=['snap'])
hera.add_full(ant=126, feed=13, fem=28, pam=45, snap='C33', snap_input='e6,n4', snap_loc='3', node='9', cdate='2019/05/16')

hera.done()
