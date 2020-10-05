#! /usr/bin/env python
import sys
from hera_cm import signal_chain, hpngen
hera = signal_chain.Update(sys.argv[0], chmod=True)

macpre = '02:02:0a:01:01:'
ippre = '10.80.2.'

arduinos = [4, 5, 7, 9, 11, 13, 14, 16, 17, 47, 48]
macs = ['cc', 'cd', 'cf', 'd1', 'd3', 'd5', 'd6', 'd8', 'd9', 'f7', 'f8']
ips = [204, 205, 207, 209, 211, 213, 214, 216, 217, 247, 248]


for rd, mac, ip in zip(arduinos, macs, ips):
    rdhpn, rev = hpngen.rd(rd)
    note = 'MAC - {}{}'.format(macpre, mac)
    hera.add_part_info(rdhpn, rev, note, '2020/03/01', '11:00', ref=None)
    note = 'IP - {}{}'.format(ippre, ip)
    hera.add_part_info(rdhpn, rev, note, '2020/03/01', '11:01', ref=None)

hera.done()
