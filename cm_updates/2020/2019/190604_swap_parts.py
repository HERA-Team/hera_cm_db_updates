#! /usr/bin/env python
import sys
import signal_chain


hera = signal_chain.Update(sys.argv[0], do_it=True)

parts_to_swap = [
                [['PAM023', 'A'], ['PAM048', 'A'], '2019/05/17', '11:00'],
                [['FEM019', 'A'], ['FEM045', 'A'], '2019/05/17', '11:00'],
                [['PAM025', 'A'], ['PAM052', 'A'], '2019/05/17', '11:00'],
                [['PAM026', 'A'], ['PAM050', 'A'], '2019/05/17', '11:00'],
                [['PAM031', 'A'], ['PAM051', 'A'], '2019/05/17', '11:00'],
                [['FEM027', 'A'], ['FEM042', 'A'], '2019/05/17', '11:00'],
                [['FEM026', 'A'], ['FEM027', 'A'], '2019/05/17', '11:00']
]

for pswap in parts_to_swap:
    hera.swap(pswap[0], pswap[1], pswap[2], pswap[3])

hera.done()
