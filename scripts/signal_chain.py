#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import sys
import os.path
import six
from hera_mc import cm_health, cm_handling


def as_part(add_or_stop, p, cdate, ctime, do_it):
    s = '{}_part.py -p {} -r {} '.format(
        add_or_stop, p[0], p[1])
    if add_or_stop == 'add':
        s += '-t {} -m {} '.format(p[2], p[3])
    s += '--date {} --time {}'.format(cdate, ctime)
    if do_it:
        s += ' --actually_do_it'
    s += '\n'
    return s


def as_connect(add_or_stop, up, dn, cdate, ctime, do_it):
    s = '{}_connection.py -u {} --uprev {} --upport {} -d {} --dnrev {} --dnport {} --date {} --time {}'.format(
        add_or_stop, up[0], up[1], up[2], dn[0], dn[1], dn[2], cdate, ctime)
    if do_it:
        s += ' --actually_do_it'
    s += '\n'
    return s


class Chain:
    def __init__(self, exename, log_file='scripts.log'):
        self.init_script(exename, log_file)

    def init_script(self, exename, log_file):
        input_script = os.path.basename(exename)
        self.output_script = input_script.split('.')[0]
        print("starting {}".format(self.output_script))
        self.fp = open(self.output_script, 'w')
        s = '#! /usr/bin/env bash\n'
        s += 'echo {} >> {}\n'.format(self.output_script, log_file)
        self.fp.write(s)
        print('-----------------\n')

    def add(self, ant, feed, fem, pam, snap, snap_input, cdate, ctime=['10:00', '11:00'], do_it=True):
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
                'HH:MM' for part/connection at 'HH:MM'
        do_it:  flag to set the 'actually_do_it' flag <True>
        """
        handle = cm_handling.Handling()
        health = cm_health.Connections()
        if isinstance(ctime, list):
            partadd_time = ctime[0]
            connadd_time = ctime[1]
        else:
            partadd_time = ctime
            connadd_time = ctime

        # Set up parts
        part = {}
        part['ant'] = ('A{}'.format(ant), 'H', 'antenna')
        part['feed'] = ('FDV{}'.format(feed), 'A', 'feed')
        part['fem'] = ('FEM{:03d}'.format(fem), 'A', 'front-end')
        part['cable'] = ('CRF{:03d}'.format(ant), 'A', 'cable-rfof')
        part['pam'] = ('PAM{:03d}'.format(pam), 'A', 'post-amp')
        part['snap'] = ('SNP{}{:06d}'.format(snap[0], int(snap[1:])), 'A', 'snap')
        snap_port = {'e': snap_input.split(',')[0].strip(), 'n': snap_input.split(',')[1].strip()}

        # Check for parts to add and add them
        parts_to_add = []
        for p in six.itervalues(part):
            x = handle.get_part_dossier(p[0], p[1], 'now')
            if not len(x):
                self.fp.write(as_part('add', [p[0], p[1], p[2], p[0]], cdate, partadd_time, do_it))
            else:
                print("Part {} is already added".format(p))
        # Set up connections
        connections_to_add = []
        up = [part['ant'][0], part['ant'][1], 'focus']
        dn = [part['feed'][0], part['feed'][1], 'input']
        connections_to_add.append([up, dn, cdate, connadd_time])

        up = [part['feed'][0], part['feed'][1], 'terminals']
        dn = [part['fem'][0], part['fem'][1], 'input']
        connections_to_add.append([up, dn, cdate, connadd_time])

        up = [part['fem'][0], part['fem'][1], 'e']
        dn = [part['cable'][0], part['cable'][1], 'ea']
        connections_to_add.append([up, dn, cdate, connadd_time])
        up = [part['fem'][0], part['fem'][1], 'n']
        dn = [part['cable'][0], part['cable'][1], 'na']
        connections_to_add.append([up, dn, cdate, connadd_time])

        up = [part['cable'][0], part['cable'][1], 'eb']
        dn = [part['pam'][0], part['pam'][1], 'ea']
        connections_to_add.append([up, dn, cdate, connadd_time])
        up = [part['cable'][0], part['cable'][1], 'nb']
        dn = [part['pam'][0], part['pam'][1], 'na']
        connections_to_add.append([up, dn, cdate, connadd_time])

        up = [part['pam'][0], part['pam'][1], 'eb']
        dn = [part['snap'][0], part['snap'][1], snap_port['e']]
        connections_to_add.append([up, dn, cdate, connadd_time])
        up = [part['pam'][0], part['pam'][1], 'nb']
        dn = [part['snap'][0], part['snap'][1], snap_port['n']]
        connections_to_add.append([up, dn, cdate, connadd_time])

        # Check for connections to add and add them
        for up, down, codate, cotime in connections_to_add:
            exco = health.check_for_existing_connection(up + down, 'now', display_results=True)
            if not exco:
                self.fp.write(as_connect('add', up, down, codate, cotime, do_it))
        print('\n')

    def done(self):
        print("=======>If OK, 'chmod u+x {}' and run that script.\n".format(self.output_script))
        self.fp.close()

    def add_node(self):
        print("This will add the @ parts of PCH, PAM, SNP (and N)")
