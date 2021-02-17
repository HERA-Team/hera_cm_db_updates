#! /usr/bin/env python
import sys
from hera_cm import signal_chain, hpngen
hera = signal_chain.Update(sys.argv[0], chmod=True)

macpre = '08:00:30:'
ippre = '10.80.2'

wrs = [157, 99, 98, 88, 155, 156, 100, 158, 95]
mfgs = ['S10.486', 'S10.495', 'S10.490', 'S9.393', 'S10.475', 'S10.474', 'S10.483',
        'S10.487', 'S10.488']
ncms = [23, 24, 25, 26, 27, 28, 29, 30, 31]
macs = ['6e:b8:f5', '6e:a7:8b', '6e:cd:a4', 'b2:55:30', '6e:6c:bc', '6e:6e:f0',
        '6e:7d:ca', '6e:b8:fa', '6e:b9:75']
ips = [-1, -1, -1, -1, -1, -1, -1, -1, -1]

for _wr, _mf, _nc, _mc, _ip in zip(wrs, mfgs, ncms, macs, ips):
    wrhpn, wrev = hpngen.wr(_wr, 'A')
    part = [wrhpn, wrev, 'white-rabbit', _mf]
    hera.update_part('add', part, '2021/02/01', '9:00')
    nchpn, nrev = hpngen.ncm(_nc)
    if isinstance(_nc, str) and _nc[0] == 'P':
        oe = 'e'
    else:
        oe = 'o'
    mfg = 'NCM-Pr{}{}'.format(oe, _nc)
    part = [nchpn, nrev, 'node-control-module', mfg]
    hera.update_part('add', part, '2021/02/01', '10:00')
    up = [wrhpn, wrev, 'mnt']
    dn = [nchpn, nrev, 'mnt1']
    hera.update_connection('add', up, dn, '2021/02/01', '11:00')
    note = 'MAC - {}{}'.format(macpre, _mc)
    hera.add_part_info(wrhpn, wrev, note, '2021/02/01', '11:00', ref=None)
    # note = 'IP - {}{}'.format(ippre, _ip)
    # hera.add_part_info(wrhpn, wrev, note, '2021/0/0', '11:01', ref=None)
hera.done()
