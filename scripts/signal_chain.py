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
    def __init__(self, exename=None, do_it=True, log_file='scripts.log'):
        """
        exename:  the name of the script executed (argv[0])
        do_it:  flag to actually enable changes
        log_file:  name of log_file
        """
        self.do_it = do_it
        self.log_file = log_file
        if log_file is not None:
            self.handle = cm_handling.Handling()
            self.health = cm_health.Connections()
            input_script = os.path.basename(exename)
            self.output_script = input_script.split('.')[0]
            print("Writing script {}".format(self.output_script))
            self.fp = open(self.output_script, 'w')
            s = '#! /usr/bin/env bash\n'
            s += 'echo "{} (do_it = {})" >> {} \n'.format(self.output_script, self.do_it, self.log_file)
            self.fp.write(s)
            print('-----------------\n')

    def add_full(self, ant, feed, fem, pam, snap, snap_input, snap_loc, node, cdate, ctime=['10:00', '11:00'], ser_num={}, **kwargs):
        """
        Parameters:
        -----------
        ant:  antenna number (int)
        feed: feed number (int)
        fem: fem number (int)
        pam: pam number (int)
        snap:  snap designation (string: e.g. 'A27')
        snap_input: inputs (string: e.g. 'e10,n8')
        snap_loc:  location of snap (int)
        node:  node number (int)
        ser_no:  dictionary of serial numbers (keyed by part-type, uses hpn if not included
        cdate:  YYYY/MM/DD - date of mods (one for all)
        ctime:  time of mods <'10:00', '11:00'>
                ['HH:MM', 'HH:MM'] for part at [0], connection at [1]
                'HH:MM' for part/connection at 'HH:MM'
        **kwargs:  include_HH, include_ND
        """
        # Process kwargs
        include_HH = False
        if 'include_HH' in kwargs.keys() and kwargs['include_HH']:
            include_HH = True
        include_ND = False
        if 'include_ND' in kwargs.keys() and kwargs['include_ND']:
            include_ND = True
        if isinstance(ctime, list):
            partadd_time = ctime[0]
            connadd_time = ctime[1]
        else:
            partadd_time = ctime
            connadd_time = ctime
        self.ser_num_dict = ser_num

        # Set up parts
        part_to_add = {}

        if include_HH:
            hpn = 'HH{}'.format(ant)
            sn = self.get_ser_num(hpn, 'ant-station')
            part_to_add['ant-station'] = (hpn, 'A', 'station', sn)

        hpn = 'A{}'.format(ant)
        sn = self.get_ser_num(hpn, 'antenna')
        part_to_add['ant'] = (hpn, 'H', 'antenna', sn)

        hpn = 'FDV{}'.format(feed)
        sn = self.get_ser_num(hpn, 'feed')
        part_to_add['feed'] = (hpn, 'A', 'feed', sn)

        hpn = 'FEM{:03d}'.format(fem)
        sn = self.get_ser_num(hpn, 'front-end')
        part_to_add['fem'] = (hpn, 'A', 'front-end', sn)

        hpn = 'CRF{:03d}'.format(ant)
        sn = self.get_ser_num(hpn, 'cable-rfof')
        part_to_add['cable'] = (hpn, 'A', 'cable-rfof', sn)

        hpn = 'PAM{:03d}'.format(pam)
        sn = self.get_ser_num(hpn, 'post-amp')
        part_to_add['pam'] = (hpn, 'A', 'post-amp', sn)

        hpn = 'SNP{}{:06d}'.format(snap[0], int(snap[1:]))
        sn = self.get_ser_num(hpn, 'snap')
        part_to_add['snap'] = (hpn, 'A', 'snap', sn)
        snap_port = {'e': snap_input.split(',')[0].strip(), 'n': snap_input.split(',')[1].strip()}

        hpn = 'N{}'.format(node)
        sn = self.get_ser_num(hpn, 'node')
        part_to_add['node'] = (hpn, 'A', 'node', sn)
        snap_loc = "loc{}".format(snap_loc)

        if include_ND:
            hpn = 'ND{}'.format(node)
            sn = self.get_ser_num(hpn, 'node-station')
            part_to_add['node-station'] = (hpn, 'A', 'station', sn)

        # Check for parts to add and add them
        if self.log_file is not None:
            for p in six.itervalues(part_to_add):
                if not self.exists('part', p[0], p[1], 'now'):
                    self.update_part('add', p, cdate, partadd_time)
                else:
                    print("Part {} is already added".format(p))

        # Set up connections
        connection_to_add = []
        if include_HH:
            up = [part_to_add['ant-station'][0], part_to_add['ant-station'][1], 'ground']
            dn = [part_to_add['ant'][0], part_to_add['ant'][1], 'ground']
            connection_to_add.append([up, dn, cdate, connadd_time])

        up = [part_to_add['ant'][0], part_to_add['ant'][1], 'focus']
        dn = [part_to_add['feed'][0], part_to_add['feed'][1], 'input']
        connection_to_add.append([up, dn, cdate, connadd_time])

        up = [part_to_add['feed'][0], part_to_add['feed'][1], 'terminals']
        dn = [part_to_add['fem'][0], part_to_add['fem'][1], 'input']
        connection_to_add.append([up, dn, cdate, connadd_time])

        up = [part_to_add['fem'][0], part_to_add['fem'][1], 'e']
        dn = [part_to_add['cable'][0], part_to_add['cable'][1], 'ea']
        connection_to_add.append([up, dn, cdate, connadd_time])
        up = [part_to_add['fem'][0], part_to_add['fem'][1], 'n']
        dn = [part_to_add['cable'][0], part_to_add['cable'][1], 'na']
        connection_to_add.append([up, dn, cdate, connadd_time])

        up = [part_to_add['cable'][0], part_to_add['cable'][1], 'eb']
        dn = [part_to_add['pam'][0], part_to_add['pam'][1], 'ea']
        connection_to_add.append([up, dn, cdate, connadd_time])
        up = [part_to_add['cable'][0], part_to_add['cable'][1], 'nb']
        dn = [part_to_add['pam'][0], part_to_add['pam'][1], 'na']
        connection_to_add.append([up, dn, cdate, connadd_time])

        up = [part_to_add['pam'][0], part_to_add['pam'][1], 'eb']
        dn = [part_to_add['snap'][0], part_to_add['snap'][1], snap_port['e']]
        connection_to_add.append([up, dn, cdate, connadd_time])
        up = [part_to_add['pam'][0], part_to_add['pam'][1], 'nb']
        dn = [part_to_add['snap'][0], part_to_add['snap'][1], snap_port['n']]
        connection_to_add.append([up, dn, cdate, connadd_time])

        up = [part_to_add['snap'][0], part_to_add['snap'][1], 'rack']
        dn = [part_to_add['node'][0], part_to_add['node'][1], snap_loc]
        connection_to_add.append([up, dn, cdate, connadd_time])

        if include_ND:
            up = [part_to_add['node'][0], part_to_add['node'][1], '@ground']
            dn = [part_to_add['node-station'][0], part_to_add['node-station'][1], '@ground']
            connection_to_add.append([up, dn, cdate, connadd_time])

        # Check for connections to add and add them
        if self.log_file is not None:
            for up, down, codate, cotime in connection_to_add:
                if not self.exists('connection', up + down, at_date='now'):
                    self.update_connection('add', up, down, codate, cotime)
            print('\n')
        if self.log_file is None:
            return part_to_add, connection_to_add

    def get_ser_num(self, hpn, part_type):
        sn = hpn
        if part_type in self.ser_num_dict.keys():
            sn = self.ser_num_dict[part_type]
        return sn

    def update_part(self, add_or_stop, part, cdate, ctime):
        self.fp.write(as_part(add_or_stop, part, cdate, ctime, self.do_it))

    def update_connection(self, add_or_stop, up, down, cdate, ctime):
        self.fp.write(as_connect(add_or_stop, up, down, cdate, ctime, self.do_it))

    def exists(atype, inp, rev='active', at_date='now'):
        if atype == 'part':
            x = self.handle.get_part_dossier(inp, rev, at_date)
            if len(x) == 0:
                return False
            return True
        if atype == 'connection':
            return self.health.check_for_existing_connection(inp, at_date, display_results=True)

    def add_station(self, stn, ser_num, cdate, ctime='10:00'):
        s = "HH{}".format(stn)
        a = "A{}".format(stn)
        n = "S/N{}".format(ser_num)
        self.fp.write('add_station.py {} --sernum {} --date {} --time {}\n'.format(s, ser_num, cdate, ctime))

        if not self.exists('part', a, 'H', 'now'):
            self.update_part('add', [a, 'H', 'antenna', n], cdate, ctime)
        else:
            print("Part {} is already added".format(a))

        up = [s, 'A', 'ground']
        down = [a, 'H', 'ground']
        if not self.exists('connection', up + down, at_date='now'):
            self.update_connection('add', up, down, cdate, ctime)

    def add_part_info(self, hpn, rev, note, cdate, ctime):
        self.fp.write('add_part_info.py -p {} -r {} -c "{}" --date {} --time {}\n'.format(hpn, rev, note, cdate, ctime))

    def add_node(self, node, pch, ncm, cdate, ctime=['10:00', '11:00'], ser_num={}):
        print("This will add the @ parts of PCH, PAM, SNP (and N)")
        if isinstance(ctime, list):
            partadd_time = ctime[0]
            connadd_time = ctime[1]
        else:
            partadd_time = ctime
            connadd_time = ctime
        self.ser_num_dict = ser_num
        hpn = 'N{}'.format(node)
        sn = self.get_ser_num(hpn, 'node')
        part_to_add['node'] = (hpn, 'A', 'node', sn)
        hpn = 'ND{}'.format(node)
        sn = self.get_ser_num(hpn, 'node-station')
        part_to_add['node-station'] = (hpn, 'A', 'station', sn)

        # Check for parts to add and add them
        for p in six.itervalues(part_to_add):
            if not self.exists('part', p[0], p[1], 'now'):
                self.update_part('add', p, cdate, partadd_time)
            else:
                print("Part {} is already added".format(p))
        print("NOW ADD CONNECTIONS")

    def done(self):
        print("=======>If OK, 'chmod u+x {}' and run that script.".format(self.output_script))
        print("\t 'do_it' flag set to {}".format(self.do_it))
        self.fp.close()
