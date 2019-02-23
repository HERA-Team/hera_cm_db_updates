#! /usr/bin/env python
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)
# Not doing it this time, but to add full signal path:
# hera.add_full(ant=2, feed=8, fem=17, pam=23, snap='C57', snap_input='e6,n4', cdate='2019/02/20')

connections_to_stop = [
                      [['CRF014', 'A', 'eb'], ['PAM028', 'A', 'ea'], '2019/02/23', '10:00'],
                      [['CRF014', 'A', 'nb'], ['PAM028', 'A', 'na'], '2019/02/23', '10:00'],
                      [['PAM028', 'A', 'eb'], ['SNPA000024', 'A', 'e2'], '2019/02/23', '10:00'],
                      [['PAM028', 'A', 'nb'], ['SNPA000024', 'A', 'n0'], '2019/02/23', '10:00']
]

parts_to_stop = [
                [['PAM028', 'A'], '2019/02/23', '10:10']
]

parts_to_add = []
connections_to_add = []

for c in connections_to_stop:
    hera.update_connection('stop', c[0], c[1], c[2], c[3])

for p in parts_to_stop:
    hera.update_part('stop', p[0], p[1], p[2])

for p in parts_to_add:
    hera.update_part('add', p[0], p[1], p[2])

for c in connections_to_add:
    hera.update_connection('add', c[0], c[1], c[2], c[3])

hera.done()
