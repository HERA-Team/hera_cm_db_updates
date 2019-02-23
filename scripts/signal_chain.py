from __future__ import absolute_import, division, print_function
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


class Update:
    def __init__(self, exename, do_it, log_file='scripts.log'):
        """
        exename:  the name of the script executed (argv[0])
        do_it:  flag to actually enable changes
        log_file:  name of log_file
        """
        self.do_it = do_it
        self.log_file = log_file
        input_script = os.path.basename(exename)
        self.output_script = input_script.split('.')[0]
        print("Writing script {}".format(self.output_script))
        self.fp = open(self.output_script, 'w')
        s = '#! /usr/bin/env bash\n'
        s += 'echo {} (do_it = {}) >> {} \n'.format(self.output_script, self.do_it, self.log_file)
        self.fp.write(s)
        print('-----------------\n')

    def add_full(self, ant, feed, fem, pam, snap, snap_input, cdate, ctime=['10:00', '11:00'], ser_num={}):
        """
        Parameters:
        -----------
        ant:  antenna number (int)
        feed: feed number (int)
        fem: fem number (int)
        pam: pam number (int)
        snap:  snap designation (string: e.g. 'A27')
        snap_input: inputs (string: e.g. 'e10,n8')
        ser_no:  dictionary of serial numbers (keyed by part-type, uses hpn if not included
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
        self.ser_num_dict = ser_num

        # Set up parts
        part = {}

        hpn = 'A{}'.format(ant)
        sn = self.get_ser_num(hpn, 'antenna')
        part['ant'] = (hpn, 'H', 'antenna', sn)

        hpn = 'FDV{}'.format(feed)
        sn = self.get_ser_num(hpn, 'feed')
        part['feed'] = (hpn, 'A', 'feed', sn)

        hpn = 'FEM{:03d}'.format(fem)
        sn = self.get_ser_num(hpn, 'front-end')
        part['fem'] = (hpn, 'A', 'front-end', sn)

        hpn = 'CRF{:03d}'.format(ant)
        sn = self.get_ser_num(hpn, 'cable-rfof')
        part['cable'] = (hpn, 'A', 'cable-rfof', sn)

        hpn = 'PAM{:03d}'.format(pam)
        sn = self.get_ser_num(hpn, 'post-amp')
        part['pam'] = (hpn, 'A', 'post-amp', sn)

        hpn = 'SNP{}{:06d}'.format(snap[0], int(snap[1:]))
        sn = self.get_ser_num(hpn, 'snap')
        part['snap'] = (hpn, 'A', 'snap', sn)
        snap_port = {'e': snap_input.split(',')[0].strip(), 'n': snap_input.split(',')[1].strip()}

        # Check for parts to add and add them
        parts_to_add = []
        for p in six.itervalues(part):
            x = handle.get_part_dossier(p[0], p[1], 'now')
            if not len(x):
                self.update_part('add', p, cdate, partadd_time)
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
                self.update_connection('add', up, down, codate, cotime)
        print('\n')

    def get_ser_num(self, hpn, part_type):
        sn = hpn
        if part_type in self.ser_num_dict.keys():
            sn = self.ser_num_dict[part_type]
        return sn

    def update_part(self, add_or_stop, part, cdate, ctime):
        self.fp.write(as_part(add_or_stop, part, cdate, ctime, self.do_it))

    def update_connection(self, add_or_stop, up, down, cdate, ctime):
        self.fp.write(as_connect(add_or_stop, up, down, cdate, ctime, self.do_it))

    def done(self):
        print("=======>If OK, 'chmod u+x {}' and run that script.".format(self.output_script))
        print("\t do_it flag set to {}".format(self.do_it))
        self.fp.close()

    def add_node(self):
        print("This will add the @ parts of PCH, PAM, SNP (and N)")
