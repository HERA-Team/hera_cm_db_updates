#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)

arduinos = [5, 9, 13, 14, 16, 47, 48]
ncm = [21, 22, 14, 20, 18, 17, 19]

for rd, nc in zip(arduinos, ncm):
    rdhpn = 'RD{:02d}'.format(rd)
    part = [rdhpn, 'A', 'arduino', rdhpn]
    hera.update_part('add', part, '2020/03/01', '10:00')
    nchpn = 'NCM{:02d}'.format(nc)
    mfg = 'NCM-Pro{}'.format(nc)
    part = [nchpn, 'A', 'node-control-module', mfg]
    hera.update_part('add', part, '2020/03/01', '10:00')
    up = [rdhpn, 'A', 'mnt']
    dn = [nchpn, 'A', 'mnt2']
    hera.update_connection('add', up, dn, '2020/03/01', '11:00')
hera.done()
