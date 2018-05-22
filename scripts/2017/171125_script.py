#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

log_file = 'scripts.log'
do_it_this_time = True

fems_to_add = ['75042', '75043', '75044', '75045', '75046']
pams_to_add = ['75117', '75118', '75119', '75120', '75121']
ants_to_add = [
              ['HH136', '1', 'S/N53', 'FEM75046', 'RI3A1', 'PAM75117', '2017/11/24'],
              ['HH137', '2', 'S/N54', 'FEM75045', 'RI3A2', 'PAM75118', '2017/11/24'],
              ['HH138', '3', 'S/N55', 'FEM75044', 'RI3A3', 'PAM75119', '2017/11/24'],
              ['HH139', '4', 'S/N56', 'FEM75043', 'RI3A4', 'PAM75120', '2017/11/24'],
              ['HH140', '30', 'S/N57', 'FEM75042', 'RI3A5', 'PAM75121', '2017/11/24']
]

fp = pc.init_script(sys.argv, log_file)
# Add FEM/PAM to parts
cdate = '2017/11/23'
ctime = '10:00'
for f in fems_to_add:
    hpn = 'FEM' + f
    rev = 'A'
    htype = 'front-end'
    serno = f
    part = [hpn, rev, htype, serno]
    fp.write(pc.part(part, cdate, ctime, do_it_this_time))
for p in pams_to_add:
    hpn = 'PAM' + p
    rev = 'B'
    htype = 'post-amp'
    serno = p
    part = [hpn, rev, htype, serno]
    fp.write(pc.part(part, cdate, ctime, do_it_this_time))

for a in ants_to_add:
    new_station = a[0]
    hhno = a[0][2:]
    new_ant = 'A' + hhno
    new_feed = 'FDA' + a[1]
    feed_mfg = 'P' + a[1]
    nrao_frend = 'FEA' + a[1]  # Keeping this just for information
    new_cable = 'C7F' + hhno
    serno = a[2]
    new_fem = a[3]
    new_rator_in = a[4]
    new_rator_out = new_rator_in[0] + 'O' + new_rator_in[2:]
    new_pam = a[5]
    cdate = a[6]
    ctime = '10:00'

    val_na = int(hhno)

    if new_pam[:3] == 'PAM':
        for p in ['E', 'N']:
            ri = new_rator_in + p
            pin = p.lower() + 'a'
            fp.write(pc.connect('add', [ri, 'A', 'b'], [new_pam, 'B', pin], cdate, ctime, do_it_this_time))
            ro = new_rator_out + p
            pout = p.lower() + 'b'
            fp.write(pc.connect('add', [new_pam, 'B', pout], [ro, 'A', 'b'], cdate, ctime, do_it_this_time))

    s = 'add_station.py {}\n'.format(new_station)
    fp.write(s)
    fp.write(pc.part([new_ant, 'H', 'antenna', serno], cdate, ctime, do_it_this_time))
    fp.write(pc.part([new_feed, 'B', 'feed', feed_mfg], cdate, ctime, do_it_this_time))
    if val_na > 127:
        fp.write(pc.part([new_cable, 'A', 'cable-feed75', new_cable], cdate, ctime, do_it_this_time))
    fp.write(pc.connect('add', [new_station, 'A', 'ground'], [new_ant, 'H', 'ground'], cdate, ctime, do_it_this_time))
    fp.write(pc.connect('add', [new_ant, 'H', 'focus'], [new_feed, 'B', 'input'], cdate, ctime, do_it_this_time))
    fp.write(pc.connect('add', [new_feed, 'B', 'terminals'], [new_fem, 'A', 'input'], cdate, ctime, do_it_this_time))
    fp.write(pc.connect('add', [new_fem, 'A', 'e'], [new_cable, 'A', 'ea'], cdate, ctime, do_it_this_time))
    fp.write(pc.connect('add', [new_fem, 'A', 'n'], [new_cable, 'A', 'na'], cdate, ctime, do_it_this_time))
    fp.write(pc.connect('add', [new_cable, 'A', 'eb'], [new_rator_in + 'E', 'A', 'a'], cdate, ctime, do_it_this_time))
    fp.write(pc.connect('add', [new_cable, 'A', 'nb'], [new_rator_in + 'N', 'A', 'a'], cdate, ctime, do_it_this_time))

fp.close()
