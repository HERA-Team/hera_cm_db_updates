#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)


macpre = '08:00:30:'
ippre = '10.80.2.'

wrs = [6, 28, 79, 80, 85, 87, 90]
mac = ['13:0f:a3', '50:e0:56', 'b2:74:88', 'b2:17:81', 'b1:81:7e', 'b2:2e:07', 'b1:e9:92']
ip = [134, 144, 160, 161, 172, 178, 170]
for i, wr in enumerate(wrs):
    if wr < 150:
        p = 'A'
    else:
        p = 'C'
    wrhpn = 'WR{}{:06d}'.format(p, wr)
    note = 'MAC - {}{}'.format(macpre, mac[i])
    hera.add_part_info(wrhpn, 'A', note, '2020/03/01', '11:00', ref=None)
    note = 'IP - {}{}'.format(ippre, ip[i])
    hera.add_part_info(wrhpn, 'A', note, '2020/03/01', '11:01', ref=None)


wrs = [101, 102, 151, 152, 153, 154]
ncm = [18, 22, 20, 17, 21, 19]
wrmfg = ['S10.484', 'S10.485', 'S10.477', 'S10.481', 'S10.482', 'S10.476']
mac = ['6e:d7:5e', '6e:d7:5d', '6e:b8:22', '6e:2c:d0', '6e:2c:db', '6e:b9:69']
ip = [187, 188, 189, 190, 191, 192]
for i, (wr, nc) in enumerate(zip(wrs, ncm)):
    if wr < 150:
        p = 'A'
    else:
        p = 'C'
    wrhpn = 'WR{}{:06d}'.format(p, wr)
    part = [wrhpn, 'A', 'white-rabit', wrmfg[i]]
    hera.update_part('add', part, '2020/03/01', '10:00')
    note = 'MAC - {}{}'.format(macpre, mac[i])
    hera.add_part_info(wrhpn, 'A', note, '2020/03/01', '11:00', ref=None)
    note = 'IP - {}{}'.format(ippre, ip[i])
    hera.add_part_info(wrhpn, 'A', note, '2020/03/01', '11:01', ref=None)
    nchpn = 'NCM{:02d}'.format(nc)
    mfg = 'NCM-Pro{}'.format(nc)
    part = [nchpn, 'A', 'node-control-module', mfg]
    hera.update_part('add', part, '2020/03/01', '10:00')
    up = [wrhpn, 'A', 'mnt']
    dn = [nchpn, 'A', 'mnt1']
    hera.update_connection('add', up, dn, '2020/03/01', '11:00')
hera.done()
