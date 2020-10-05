#! /usr/bin/env python
import sys
from hera_cm import signal_chain, hpngen
hera = signal_chain.Update(sys.argv[0], chmod=True)

macpre = '02:02:0a:01:01:'
ippre = '10.80.2.'

arduinos = [2]
ncm = ['P1']
macs = ['ca']
ips = [202]

for _rd, _nc, _mc, _ip in zip(arduinos, ncm, macs, ips):
    rdhpn, rrev = hpngen.rd(_rd)
    part = [rdhpn, rrev, 'arduino', rdhpn]
    hera.update_part('add', part, '2020/03/01', '10:00')
    nchpn, nrev = hpngen.ncm(_nc)
    mfg = 'NCM-Pro{}'.format(_nc)
    part = [nchpn, nrev, 'node-control-module', mfg]
    hera.update_part('add', part, '2020/03/01', '10:00')
    up = [rdhpn, rrev, 'mnt']
    dn = [nchpn, nrev, 'mnt2']
    hera.update_connection('add', up, dn, '2020/03/01', '11:00')
    note = 'MAC - {}{}'.format(macpre, _mc)
    hera.add_part_info(rdhpn, rrev, note, '2020/03/01', '11:00', ref=None)
    note = 'IP - {}{}'.format(ippre, _ip)
    hera.add_part_info(rdhpn, rrev, note, '2020/03/01', '11:01', ref=None)
hera.done()
