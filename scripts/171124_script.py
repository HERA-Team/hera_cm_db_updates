#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc

log_file = 'scripts.log'
do_it_this_time = True

connections_to_stop = [
                      [['C7F142', 'A', 'eb'], ['RI4B7E', 'A', 'a'], '2017/11/19'],
                      [['C7F142', 'A', 'nb'], ['RI4B7N', 'A', 'a'], '2017/11/19'],
                      [['FEA32', 'A', 'e'], ['C7F142', 'A', 'ea'], '2017/11/19'],
                      [['FEA32', 'A', 'n'], ['C7F142', 'A', 'na'], '2017/11/19'],
                      [['FDA32', 'B', 'terminals'], ['FEA32', 'A', 'input'], '2017/11/19']
]
connections_to_strt = [
                      [['FDA32', 'A', 'terminals'], ['FEM75041', 'A', 'input'], '2017/11/23'],
                      [['FEM75041', 'A', 'e'], ['C7F142', 'A', 'ea'], '2017/11/23'],
                      [['FEM75041', 'A', 'n'], ['C7F142', 'A', 'na'], '2017/11/23'],
                      [['C7F142', 'A', 'eb'], ['RI3A6E', 'A', 'a'], '2017/11/23'],
                      [['C7F142', 'A', 'nb'], ['RI3A6N', 'A', 'a'], '2017/11/23']
]
fems_to_add = ['75041', '75042', '75043', '75044', '75045', '75046']
pams_to_add = ['75117', '75118', '75119', '75120', '75121', '75122']
ants_to_add = [
              ['HH136', '1', 'S/N53', 'FEM75046', 'RI3A1', 'PAM75117', '2017/11/24'],
              ['HH137', '2', 'S/N54', 'FEM75045', 'RI3A2', 'PAM75118', '2017/11/24'],
              ['HH138', '3', 'S/N55', 'FEM75044', 'RI3A3', 'PAM75119', '2017/11/24'],
              ['HH139', '4', 'S/N56', 'FEM75043', 'RI3A4', 'PAM75120', '2017/11/24'],
              ['HH140', '30', 'S/N57', 'FEM75042', 'RI3A5', 'PAM75121', '2017/11/24']
]

fp = pc.init_script()
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

for c in connections_to_stop:
    fp.write(pc.connect(['stop']))

for a in ants_to_add:
    new_station = a[0]
    hhno = a[0][2:]
    new_ant = 'A' + hhno
    new_feed = 'FDA' + a[1]
    feed_mfg = 'P' + a[1]
    nrao_frend = 'FEA' + a[1]
    new_cable = 'C7F' + hhno
    serno = a[2]
    new_fem = a[3]
    new_rator = a[4]
    new_pam = a[5]
    cdate = a[6]
    ctime = '10:00'

    val_na = int(hhno)

    if new_fem[:3] == 'FEM':
        new_front_end = new_fem
    else:
        new_front_end = nrao_frend
    if new_pam[:3] == 'PAM':
        print("Need to disconnect, and reconnect PAM")

    s = 'add_station.py {}\n'.format(new_station)
    fp.write(s)
    fp.write(part([new_ant, 'H', 'antenna', serno], cdate, ctime, do_it_this_time))
    fp.write(part([new_feed, 'B', 'feed', feed_mfg], cdate, ctime, do_it_this_time))
    if val_na > 127:
        fp.write(part([new_cable, 'A', 'cable-feed75', new_cable], cdate, ctime, do_it_this_time))
    fp.write(connect(['add', new_station, 'A', 'ground'], [new_ant, 'H', 'ground'], cdate, ctime, do_it_this_time))
    fp.write(connect(['add', new_ant, 'H', 'focus'], [new_feed, 'B', 'input'], cdate, ctime, do_it_this_time))
    fp.write(connect(['add', new_feed, 'B', 'terminals'], [new_front_end, 'A', 'input'], cdate, ctime, do_it_this_time))
    fp.write(connect(['add', new_front_end, 'A', 'e'], [new_cable, 'A', 'ea'], cdate, ctime, do_it_this_time))
    fp.write(connect(['add', new_front_end, 'A', 'n'], [new_cable, 'A', 'na'], cdate, ctime, do_it_this_time))
    fp.write(connect(['add', new_cable, 'A', 'eb'], [new_rator + 'E', 'A', 'a'], cdate, ctime, do_it_this_time))
    fp.write(connect(['add', new_cable, 'A', 'nb'], [new_rator + 'N', 'A', 'a'], cdate, ctime, do_it_this_time))



fp.close()
