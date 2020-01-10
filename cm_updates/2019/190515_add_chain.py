#! /usr/bin/env python
import sys
import signal_chain


hera = signal_chain.Update(sys.argv[0], do_it=True)

hera.add_full(ant=106, feed=20, fem=30, pam=44, snap='C33', snap_input='e2,n0', snap_loc='3', node='9', cdate='2019/05/15')
hera.add_full(ant=107, feed=21, fem=31, pam=35, snap='C10', snap_input='e2,n0', snap_loc='0', node='9', cdate='2019/05/15', dont_add_part=['node'])
hera.add_full(ant=125, feed=25, fem=29, pam=46, snap='C33', snap_input='e10,n8', snap_loc='3', node='9', cdate='2019/05/15', dont_add_part=['node', 'snap'])

hera.done()
