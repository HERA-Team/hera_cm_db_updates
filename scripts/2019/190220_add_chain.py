#! /usr/bin/env python
import sys
import signal_chain


hera = signal_chain.Update(sys.argv[0], do_it=True)

hera.add_full(ant=2, feed=8, fem=17, pam=23, snap='C57', snap_input='e6,n4', cdate='2019/02/20')
hera.add_full(ant=11, feed=9, fem=19, pam=25, snap='A8', snap_input='e2,n0', cdate='2019/02/20')
hera.add_full(ant=12, feed=3, fem=20, pam=26, snap='A8', snap_input='e6,n4', cdate='2019/02/20')
hera.add_full(ant=14, feed=5, fem=22, pam=28, snap='A24', snap_input='e2,n0', cdate='2019/02/20')
hera.add_full(ant=23, feed=11, fem=23, pam=29, snap='A24', snap_input='e6,n4', cdate='2019/02/20')
hera.add_full(ant=24, feed=12, fem=24, pam=30, snap='A24', snap_input='e10,n8', cdate='2019/02/20')
hera.add_full(ant=26, feed=7, fem=26, pam=32, snap='A20', snap_input='e6,n4', cdate='2019/02/20')
hera.add_full(ant=39, feed=14, fem=27, pam=33, snap='A20', snap_input='e10,n8', cdate='2019/02/20')

hera.done()
