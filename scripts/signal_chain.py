#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys
from hera_mc import cm_handling, cm_health


class Chain:
    def __init__(self, script_file, log_file='scripts.log'):
        self.script_file = script_file
        self.fp = pc.init_script([script_file], log_file)
        print("Opening script file:  {}".format(script_file))

    def add(self, ant, feed, fem, pam, snap, snap_input, cdate, ctime=['10:00', '11:00'], do_it_this_time=True):
        """
        Parameters:
        -----------
        ant:  antenna number (int)
        feed: feed number (int)
        fem: fem number (int)
        pam: pam number (int)
        snap:  snap designation (string: e.g. 'A27')
        snap_input: inputs (string: e.g. 'e10,n8')
        cdate:  YYYY/MM/DD - date of mods (one for all)
        ctime:  time of mods <'10:00', '11:00'>
                ['HH:MM', 'HH:MM'] for part at [0], connection at [1]
                'x' for part/connection at 'x'
        do_it_this_time:  flag to set the 'actually_do_it' flag <True>
        """
        handle = cm_handling.Handling()
        health = cm_health.Connections()
        if isinstance(ctime, list):
            patime = ctime[0]
            cotime = ctime[1]
        else:
            patime = ctime
            cotime = ctime

        # Set up parts
        part = {}
        part['ant'] = ('A{}'.format(ant), 'H', 'antenna')
        part['feed'] = ('FDV{}'.format(feed), 'A', 'feed')
        part['fem'] = ('FEM{:03d}'.format(fem), 'A', 'front-end')
        part['cable'] = ('CRF{:03d}'.format(ant), 'A', 'cable-rfof')
        part['pam'] = ('PAM{:03d}'.format(pam), 'A', 'post-amp')
        part['snap'] = ('SNP{}{:06d}'.format(snap[0], int(snap[1:])), 'A', 'snap')
        snap_port = {'e': snap_input.split(',')[0].strip(), 'n': snap_input.split(',')[1].strip()}
        # Check for parts to add
        parts_to_add = []
        for p in part:
            x = handle.get_part_dossier(part[p][0], part[p][1], 'now')
            if not len(x):
                self.fp.write(pc.part('add', [part[p][0], part[p][1], part[p][2], part[p][0]],
                              cdate, patime, do_it_this_time))
            else:
                print("Part {} is already added".format(part[p]))

        # Set up connections
        connections_to_add = []
        up = [part['ant'][0], part['ant'][1], 'focus']
        dn = [part['feed'][0], part['feed'][1], 'input']
        connections_to_add.append([up, dn, cdate, cotime])
        up = [part['feed'][0], part['feed'][1], 'terminals']
        dn = [part['fem'][0], part['fem'][1], 'input']
        connections_to_add.append([up, dn, cdate, cotime])
        up = [part['fem'][0], part['fem'][1], 'e']
        dn = [part['cable'][0], part['cable'][1], 'ea']
        connections_to_add.append([up, dn, cdate, cotime])
        up = [part['fem'][0], part['fem'][1], 'n']
        dn = [part['cable'][0], part['cable'][1], 'na']
        connections_to_add.append([up, dn, cdate, cotime])
        up = [part['cable'][0], part['cable'][1], 'eb']
        dn = [part['pam'][0], part['pam'][1], 'ea']
        connections_to_add.append([up, dn, cdate, cotime])
        up = [part['cable'][0], part['cable'][1], 'nb']
        dn = [part['pam'][0], part['pam'][1], 'na']
        connections_to_add.append([up, dn, cdate, cotime])
        up = [part['pam'][0], part['pam'][1], 'eb']
        dn = [part['snap'][0], part['snap'][1], snap_port['e']]
        connections_to_add.append([up, dn, cdate, cotime])
        up = [part['pam'][0], part['pam'][1], 'nb']
        dn = [part['snap'][0], part['snap'][1], snap_port['n']]
        connections_to_add.append([up, dn, cdate, cotime])

        # Check for connections to add
        for c in connections_to_add:
            v = [c[0][0], c[0][1], c[0][2], c[1][0], c[1][1], c[1][2]]
            exco = health.check_for_existing_connection(v, cdate, display_results=True)
            if not exco:
                self.fp.write(pc.connect('add', c[0], c[1], c[2], c[3], do_it_this_time))

        print("\n\n{} written.".format(self.script_file))
        print("If OK, 'chmod u+x {}' and run that script.".format(self.script_file))
