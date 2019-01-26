#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys

print("Updates addressing HERA_Commissioning issues #92 and #99")

log_file = 'scripts.log'
do_it_this_time = True

fems_to_add = ['75052', '75051', '75061', '75062', '75063', '75049', '75050']
pams_to_add = ['75132', '75164', '75163', '75162', '75161', '75160']
ants_to_add = [
              ['HH57', '57', 'S/N70', '2018/02/07'],
              ['HH58', '58', 'S/N71', '2018/02/07'],
              ['HH72', '59', 'S/N72', '2018/02/07'],
              ['HH81', '60', 'S/N73', 'FEM75052', 'RI3B8', 'PAM75132', '2018/02/07'],
              ['HH116', '61', 'S/N74', 'FEM75051', 'RI2A1', 'PAM75164', '2018/02/07'],
              ['HH155', '62', 'S/N75', 'FEM75061', 'RI2A2', 'PAM75163', '2018/02/07'],
              ['HH156', '63', 'S/N76', 'FEM75062', 'RI2A3', 'PAM75162', '2018/02/07'],
              ['HA330', '66', 'S/N77', '2018/02/07'],
              ['HA334', '67', 'S/N78', 'FEM75063', 'RI2A4', 'PAM75161', '2018/02/07'],
              ['HA338', '68', 'S/N79', 'FEM75068', 'RI2A5', 'PAM75160', '2018/02/07']
]
connections_to_stop = [
                      [['FDA55', 'B', 'terminals'], ['FEM75025', 'A', 'input']],
                      [['FEM75025', 'A', 'e'], ['C7F68', 'A', 'ea']],
                      [['FEM75025', 'A', 'n'], ['C7F68', 'A', 'na']],
                      [['FDA41', 'B', 'terminals'], ['FEM75068', 'A', 'input']],
                      [['FEM75068', 'A', 'e'], ['C7F104', 'A', 'ea']],
                      [['FEM75068', 'A', 'n'], ['C7F104', 'A', 'na']]
]
connections_to_add = [
                     [['FDA55', 'B', 'terminals'], ['FEM75049', 'A', 'input']],
                     [['FEM75049', 'A', 'e'], ['C7F68', 'A', 'ea']],
                     [['FEM75049', 'A', 'n'], ['C7F68', 'A', 'na']],
                     [['FDA41', 'B', 'terminals'], ['FEM75050', 'A', 'input']],
                     [['FEM75050', 'A', 'e'], ['C7F104', 'A', 'ea']],
                     [['FEM75050', 'A', 'n'], ['C7F104', 'A', 'na']]
]

fp = pc.init_script(sys.argv, log_file)

# Adding missing receiverator input (R3B8)
sigch_to_add = [
               ['RI3B8E', 'A', '"cable-post-amp(in)"', 'RI3B7E'],
               ['RI3B8N', 'A', '"cable-post-amp(in)"', 'RI3B7N'],
               ['PAM75132', 'B', 'post-amp', '75132'],
               ['RO3B8E', 'A', '"cable-post-amp(out)"', 'RO3B7E'],
               ['RO3B8N', 'A', '"cable-post-amp(out)"', 'RO3B7N'],
               ['CR3B8E', 'A', 'cable-receiverator', 'CBLR3B7E'],
               ['CR3B8N', 'A', 'cable-receiverator', 'CBLR3B7N'],
               ['DF1C4', 'A', 'f-engine', 'PF1C4'],
               ['DF1C3', 'A', 'f-engine', 'PF1C3']
]
conns_to_add = [
               [['RI3B8E', 'A', 'b'], ['PAM75132', 'B', 'ea']],
               [['RI3B8N', 'A', 'b'], ['PAM75132', 'B', 'na']],
               [['PAM75132', 'B', 'eb'], ['RO3B8E', 'A', 'a']],
               [['PAM75132', 'B', 'nb'], ['RO3B8N', 'A', 'a']],
               [['RO3B8E', 'A', 'b'], ['CR3B8E', 'A', 'a']],
               [['RO3B8N', 'A', 'b'], ['CR3B8N', 'A', 'a']],
               [['CR3B8E', 'A', 'b'], ['CC2R5C8', 'A', 'a']],
               [['CR3B8N', 'A', 'b'], ['CC2R6C8', 'A', 'a']],
               [['CC2R5C8', 'A', 'b'], ['DF1C4', 'A', 'input']],
               [['CC2R6C8', 'A', 'b'], ['DF1C3', 'A', 'input']]
]
cdate = '2017/10/01'
ctime = '10:00'
for s in sigch_to_add:
    fp.write(pc.part('add', s, cdate, ctime, do_it_this_time))
for c in conns_to_add:
    fp.write(pc.connect('add', c[0], c[1], cdate, ctime, do_it_this_time))

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

# Stop then update old connections per issue 92
cdate = '2018/01/26'
ctime = '10:00'
for c in connections_to_stop:
    fp.write(pc.connect('stop', c[0], c[1], cdate, ctime, do_it_this_time))
for c in connections_to_add:
    fp.write(pc.connect('add', c[0], c[1], cdate, ctime, do_it_this_time))

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
