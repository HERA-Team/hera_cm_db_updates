#! /usr/bin/env python
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

connections_to_stop = []

parts_to_stop = []

parts_to_add = [
               [['PAM024', 'A', 'post-amp', 'PAM024'], '2019/02/23', '12:00']
]

connections_to_add = [
                     [['CRF001', 'A', 'eb'], ['PAM024', 'A', 'ea'], '2019/02/23', '12:10'],
                     [['CRF001', 'A', 'nb'], ['PAM024', 'A', 'na'], '2019/02/23', '12:10'],
                     [['PAM024', 'A', 'eb'], ['SNPC000057', 'A', 'e10'], '2019/02/23', '12:10'],
                     [['PAM024', 'A', 'nb'], ['SNPC000057', 'A', 'n8'], '2019/02/23', '12:10']
]

for c in connections_to_stop:
    hera.update_connection('stop', c[0], c[1], c[2], c[3])

for p in parts_to_stop:
    hera.update_part('stop', p[0], p[1], p[2])

for p in parts_to_add:
    hera.update_part('add', p[0], p[1], p[2])

for c in connections_to_add:
    hera.update_connection('add', c[0], c[1], c[2], c[3])

hera.done()
