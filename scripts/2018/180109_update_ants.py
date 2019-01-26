#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

log_file = 'scripts.log'
do_it_this_time = True

fems_to_add = ['75053', '75054', '75055', '75056', '75057', '75058', '75059', '75060', '75068']
pams_to_add = ['75123', '75124', '75125', '75126', '75127', '75128', '75129', '75130', '75131']
ants_to_add = [
              ['HH99', '36', 'S/N58', 'FEM75057', 'RI3A7', 'PAM75123', '2018/01/08'],
              ['HH100', '37', 'S/N59', 'FEM75056', 'RI3A8', 'PAM75124', '2018/01/08'],
              ['HH101', '38', 'S/N60', 'FEM75055', 'RI3B1', 'PAM75125', '2018/01/08'],
              ['HH102', '39', 'S/N61', 'FEM75054', 'RI3B2', 'PAM75126', '2018/01/08'],
              ['HH103', '40', 'S/N62', 'FEM75053', 'RI3B3', 'PAM75127', '2018/01/08'],
              ['HH104', '41', 'S/N63', 'FEM75068', 'RI3B4', 'PAM75128', '2018/01/08'],
              ['HH105', '42', 'S/N64', '2018/01/08'],
              ['HH106', '44', 'S/N65', '2018/01/08'],
              ['HH117', '45', 'S/N66', 'FEM75060', 'RI3B5', 'PAM75129', '2018/01/08'],
              ['HH118', '46', 'S/N67', 'FEM75059', 'RI3B6', 'PAM75130', '2018/01/08'],
              ['HH119', '47', 'S/N68', 'FEM75058', 'RI3B7', 'PAM75131', '2018/01/08'],
              ['HH125', '56', 'S/N69', '2018/01/08']
]
ants_to_stop = ['100', '101', '102', '103', '106', '109', '110', '111', '113', '114', '115', '116', '117',
                '118', '119', '120', '121', '122', '123', '124', '125', '12', '17', '21', '30', '32', '34',
                '44', '45', '46', '47', '49', '50', '5', '57', '58', '59', '60', '61', '62', '63', '66',
                '73', '74', '76', '77', '78', '79', '7', '82', '83', '90', '93', '94', '95', '98', '99']

fp = pc.init_script(sys.argv, log_file)
# Stop all old rev P antennas
cdate = '2016/10/01'
ctime = '10:00'
for a in ants_to_stop:
    hpn = 'A' + a
    rev = 'P'
    part = [hpn, rev]
    fp.write(pc.part('stop', part, cdate, ctime, do_it_this_time))

# Add FEM/PAM to parts
cdate = '2017/11/23'
ctime = '10:00'
for f in fems_to_add:
    hpn = 'FEM' + f
    rev = 'A'
    htype = 'front-end'
    serno = f
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))
for p in pams_to_add:
    hpn = 'PAM' + p
    rev = 'B'
    htype = 'post-amp'
    serno = p
    part = [hpn, rev, htype, serno]
    fp.write(pc.part('add', part, cdate, ctime, do_it_this_time))

for a in ants_to_add:
    new_station = a[0]
    hhno = a[0][2:]
    new_ant = 'A' + hhno
    new_feed = 'FDA' + a[1]
    feed_mfg = 'P' + a[1]
    nrao_frend = 'FEA' + a[1]  # Keeping this just for information
    new_cable = 'C7F' + hhno
    serno = a[2]
    if len(a) > 4:
        new_fem = a[3]
        new_rator_in = a[4]
        new_rator_out = new_rator_in[0] + 'O' + new_rator_in[2:]
        new_pam = a[5]
    else:
        new_pam = 'NOTCONNECTED'
    cdate = a[-1]
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
    fp.write(pc.part('add', [new_ant, 'H', 'antenna', serno], cdate, ctime, do_it_this_time))
    fp.write(pc.part('add', [new_feed, 'B', 'feed', feed_mfg], cdate, ctime, do_it_this_time))
    if val_na > 127:
        fp.write(pc.part('add', [new_cable, 'A', 'cable-feed75', new_cable], cdate, ctime, do_it_this_time))
    fp.write(pc.connect('add', [new_station, 'A', 'ground'], [new_ant, 'H', 'ground'], cdate, ctime, do_it_this_time))
    fp.write(pc.connect('add', [new_ant, 'H', 'focus'], [new_feed, 'B', 'input'], cdate, ctime, do_it_this_time))
    if len(a) > 4:
        fp.write(pc.connect('add', [new_feed, 'B', 'terminals'], [new_fem, 'A', 'input'], cdate, ctime, do_it_this_time))
        fp.write(pc.connect('add', [new_fem, 'A', 'e'], [new_cable, 'A', 'ea'], cdate, ctime, do_it_this_time))
        fp.write(pc.connect('add', [new_fem, 'A', 'n'], [new_cable, 'A', 'na'], cdate, ctime, do_it_this_time))
        fp.write(pc.connect('add', [new_cable, 'A', 'eb'], [new_rator_in + 'E', 'A', 'a'], cdate, ctime, do_it_this_time))
        fp.write(pc.connect('add', [new_cable, 'A', 'nb'], [new_rator_in + 'N', 'A', 'a'], cdate, ctime, do_it_this_time))

fp.close()
