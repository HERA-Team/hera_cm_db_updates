#! /usr/bin/env python
import sys
from hera_cm import signal_chain, hpngen
hera = signal_chain.Update(sys.argv[0], chmod=True)

macpre = '08:00:30:'
ippre = '10.80.2.'

wrs = ['len4p0']
mfgs = ['S8.313']
ncms = ['P1']
macs = ['50:e8:17']
ips = [138]

for _wr, _mf, _nc, _mc, _ip in zip(wrs, mfgs, ncms, macs, ips):
    wrhpn, wrev = hpngen.wr(_wr)
    part = [wrhpn, wrev, 'white-rabbit', _mf]
    hera.update_part('add', part, '2020/03/01', '10:00')
    nchpn, nrev = hpngen.ncm(_nc)
    if isinstance(_nc, str) and _nc[0] == 'P':
        oe = 'e'
    else:
        oe = 'o'
    mfg = 'NCM-Pr{}{}'.format(oe, _nc)
    part = [nchpn, nrev, 'node-control-module', mfg]
    hera.update_part('add', part, '2020/03/01', '10:00')
    up = [wrhpn, wrev, 'mnt']
    dn = [nchpn, nrev, 'mnt1']
    hera.update_connection('add', up, dn, '2020/03/01', '11:00')
    note = 'MAC - {}{}'.format(macpre, _mc)
    hera.add_part_info(wrhpn, wrev, note, '2020/03/01', '11:00', ref=None)
    note = 'IP - {}{}'.format(ippre, _ip)
    hera.add_part_info(wrhpn, wrev, note, '2020/03/01', '11:01', ref=None)
hera.done()
