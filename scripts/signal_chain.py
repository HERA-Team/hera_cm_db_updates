from __future__ import absolute_import, division, print_function
import os.path
import six
import copy
from hera_mc import cm_health, cm_handling, cm_utils


def as_part(add_or_stop, p, cdate, ctime):
    s = '{}_part.py -p {} -r {} '.format(
        add_or_stop, p[0], p[1])
    if add_or_stop == 'add':
        s += '-t {} -m {} '.format(p[2], p[3])
    s += '--date {} --time {}'.format(cdate, ctime)
    s += '\n'
    return s


def as_connect(add_or_stop, up, dn, cdate, ctime):
    s = '{}_connection.py -u {} --uprev {} --upport {} -d {} --dnrev {} --dnport {} --date {} --time {}\n'.format(
        add_or_stop, up[0], up[1], up[2], dn[0], dn[1], dn[2], cdate, ctime)
    return s


class Update:
    def __init__(self, exename=None, log_file='scripts.log'):
        """
        exename:  the name of the script executed (argv[0])
        log_file:  name of log_file
        """
        self.log_file = log_file
        self.handle = cm_handling.Handling()
        self.health = cm_health.Connections()
        if log_file is not None:
            input_script = os.path.basename(exename)
            self.output_script = input_script.split('.')[0]
            print("Writing script {}".format(self.output_script))
            self.fp = open(self.output_script, 'w')
            s = '#! /usr/bin/env bash\n'
            s += 'echo "{}" >> {} \n'.format(self.output_script, self.log_file)
            self.fp.write(s)
            print('-----------------\n')
        self.snap_ports = [{'e': 'e2', 'n': 'n0'}, {'e': 'e6', 'n': 'n4'}, {'e': 'e10', 'n': 'n8'}]

    def add_full(self, ant, feed, fem, bulkhead, pam, snap, snap_input, snap_loc, node, cdate, ctime=['10:00', '11:00'], ser_num={}, **kwargs):
        """
        Parameters:
        -----------
        ant:  antenna number (int)
        feed: feed number (int)
        fem: fem number (int)
        bulkhead:  node bulkhead plate input port number (int)
        pam: pam number (int)
        snap:  snap designation (string: e.g. 'A27', i.e. skip the 4 0's)
        snap_input: inputs (string: e.g. 'e10,n8')
        snap_loc:  location of snap (int)
        node:  node number (int)
        ser_no:  dictionary of serial numbers (keyed by part-type, uses hpn if not included
        cdate:  YYYY/MM/DD - date of mods (one for all)
        ctime:  time of mods <'10:00', '11:00'>
                ['HH:MM', 'HH:MM'] for part at [0], connection at [1]
                'HH:MM' for part/connection at 'HH:MM'
        **kwargs:  dont_add_part is for parts that may be duplicated within a single script
        """
        # Process kwargs
        dont_add_part = None
        if 'dont_add_part' in kwargs.keys():
            dont_add_part = kwargs['dont_add_part']

        if isinstance(ctime, list):
            partadd_time = ctime[0]
            connadd_time = ctime[1]
        else:
            partadd_time = ctime
            connadd_time = ctime
        self.ser_num_dict = ser_num

        # Set up parts
        part_to_add = {}

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

        hpn = 'NBP{:02d}'.format(node)
        sn = '{}'.format(node)
        part_to_add['bulkhead'] = (hpn, 'A', 'node-bulkhead', sn)

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

        hpn = 'N{:02d}'.format(node)
        sn = self.get_ser_num(hpn, 'node')
        part_to_add['node'] = (hpn, 'A', 'node', sn)
        snap_loc = "loc{}".format(snap_loc)

        hpn = 'ND{:02d}'.format(node)
        sn = self.get_ser_num(hpn, 'node-station')
        part_to_add['node-station'] = (hpn, 'A', 'station', sn)

        # Perform some checks
        print("GET THE PAM SLOT NUMBER AND MAKE SURE IT MATCHES THE SUPPLIED BULKHEAD NUMBER")

        # Check for parts to add and add them
        if self.log_file is not None:
            for k, p in six.iteritems(part_to_add):
                if self.exists('part', p[0], p[1], 'now'):
                    print("{} {} is already added".format(k, p[0]))
                elif dont_add_part is not None and k in dont_add_part:
                    print("Skip {} {}".format(k, p[0]))
                else:
                    self.update_part('add', p, cdate, partadd_time)

        # Set up connections
        connection_to_add = []
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

        up = [part_to_add['fem'][0], part_to_add['fem'][1], '@pwr']
        port = '@pwr{:02d}'.format(bulkhead)
        dn = [part_to_add['bulkhead'][0], part_to_add['bulkhead'][1], port]
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

        up = [part_to_add['node'][0], part_to_add['node'][1], '@ground']
        dn = [part_to_add['node-station'][0], part_to_add['node-station'][1], '@ground']
        connection_to_add.append([up, dn, cdate, connadd_time])

        # Check for connections to add and add them
        if self.log_file is not None:
            for up, down, codate, cotime in connection_to_add:
                if not self.exists('connection', hpn=up[0], rev=up[1], port=up[2], side='up', at_date=cdate):
                    self.update_connection('add', up, down, codate, cotime)
            print('\n')
        if self.log_file is None:
            return part_to_add, connection_to_add

    def get_ser_num(self, hpn, part_type):
        """
        Pull the serial number out of the class dictionary.  If none, just use the hpn
        """
        sn = hpn
        if part_type in self.ser_num_dict.keys():
            sn = self.ser_num_dict[part_type]
        return sn

    def update_part(self, add_or_stop, part, cdate, ctime):
        """
        add_or_stop:  'add' or 'stop'
        part:  [hpn, rev, <type>, <mfg num>] (last two only for 'add')
        cdate:  date of update YYYY/MM/DD
        ctime:  time of update HH:MM
        """
        self.fp.write(as_part(add_or_stop, part, cdate, ctime))

    def update_connection(self, add_or_stop, up, down, cdate, ctime):
        """
        add_or_stop:  'add' or 'stop'
        up:  upstream connection
        down:  downstream connection
        cdate:  date of update YYYY/MM/DD
        ctime:  time of update HH:MM
        """
        self.fp.write(as_connect(add_or_stop, up, down, cdate, ctime))

    def exists(self, atype, hpn, rev='active', port=None, side='both', at_date='now'):
        """
        Check if a part or connection exists for hpn

        Parameters
        ----------
        atype :  string
              'part' or connection
        hpn : string or list of strings
              HERA part number to check.  Can be a list of strings or a csv-list
        rev : None or string or list of strings.
              Revision(s) to check.  If None it checks all/any.  Default='active'
        port : None or string or list of strings
               name of port to check.  If None (default) it checks all/any (atype='connection' only)
        side : string
               "side" of part to check.  Options are:  up, down, or both (default)
        at_date : string, float, int, Time, or datetime
                  date for the connection to be active.  Default is 'now'

        Return
        ------
        boolean
                 True if existing corresponding hpn/rev
        """
        if atype == 'part':
            return False
            x = self.handle.get_part_dossier(hpn, rev, at_date)
            if len(x) == 0:
                return False
            return True
        if atype == 'connection':
            return self.health.check_for_existing_connection(hpn=hpn, rev=rev, port=port, side=side, at_date=at_date)

    def add_antenna_station(self, stn, ser_num, cdate, ctime='10:00'):
        """
        Add an antenna station to the database.

        Parameters
        ----------
        stn : string or int
              antenna number (digits only)
        ser_num : string or int
                  installation order number of antenna
        cdate : string
                YYYY/MM/DD format
        ctime : string
                HH:MM format
        """
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
        if not self.exists('connection', hpn=s, rev='A', port='ground', side='up', at_date='now'):
            self.update_connection('add', up, down, cdate, ctime)

    def add_part_info(self, hpn, rev, note, cdate, ctime):
        """
        Add a note/comment for a part to the database

        Parameters
        ----------
        hpn : string
              HERA part number for comment
        rev : string
              Revision for comment.
        note : string
               The desired note.
        cdate : string
                YYYY/MM/DD format
        ctime : string
                HH:MM format
        """
        self.fp.write('add_part_info.py -p {} -r {} -c "{}" --date {} --time {}\n'.format(hpn, rev, note, cdate, ctime))

    def add_node(self, node, fps, pch, ncm, pams, snaps, cdate, ctime=['10:00', '11:00'], ser_num={}, override=False):
        """
        Add a node and interior into database.

        Parameters
        ----------
        node : int
                node number
        fps : int
                fem power supply unit
        pch : int
                pam chassis
        ncm : string or int
                node control module
        pams : list of ints
                list of the 12 pams (less allowed if override['pam'] is True)
        snaps : list of strings
                list of the 4 snaps (less allowed if override['snap'] is True)
        cdate : string
                YYYY/MM/DD format
        ctime : [string, string]
                part-add time, connection-add time in HH:MM format
        ser_num : dict
                dictionary of the serial numbers for the different part types
        override : bool or dict
                allow for non-standard number of pams and/or snaps
        """
        #  Setup/check overrides
        overridable_parts = {'pam': [12, len(pams)], 'snap': [4, len(snaps)]}
        for ox in overridable_parts.keys():
            if isinstance(override, bool):
                ovrd = override
            else:
                ovrd = False if ox not in override.keys() else override[ox]
            if not ovrd and overridable_parts[ox][0] != overridable_parts[ox][1]:
                print("Need {} {}s - you've supplied {}".format(overridable_parts[ox][0], ox, overridable_parts[ox][1]))
                print("If ok, rerun with <override['{}']=True>".format(ox))
                return

        if isinstance(ctime, list):
            partadd_time = ctime[0]
            connadd_time = ctime[1]
        else:
            partadd_time = ctime
            connadd_time = ctime
        self.ser_num_dict = ser_num
        part_to_add = {}
        hpn = 'FPS{:02d}'.format(fps)
        sn = self.get_ser_num(hpn, 'fps')
        part_to_add['fem-power-supply'] = (hpn, 'A', 'fem-power-supply', sn)
        hpn = 'PCH{:02d}'.format(pch)
        sn = self.get_ser_num(hpn, 'pch')
        part_to_add['pam-chassis'] = (hpn, 'A', 'pam-chassis', sn)
        hpn = 'NCM{}'.format(ncm)
        sn = self.get_ser_num(hpn, 'ncm')
        part_to_add['node-control-module'] = (hpn, 'A', 'node-control-module', sn)
        hpn = 'N{:02d}'.format(node)
        sn = self.get_ser_num(hpn, 'node')
        part_to_add['node'] = (hpn, 'A', 'node', sn)
        hpn = 'ND{:02d}'.format(node)
        sn = self.get_ser_num(hpn, 'node-station')
        part_to_add['node-station'] = (hpn, 'A', 'station', sn)
        hpn = 'NBP{:02d}'.format(node)
        sn = self.get_ser_num(hpn, 'node-bulkhead')
        part_to_add['node-bulkhead'] = (hpn, 'A', 'node-bulkhead', sn)
        for _pam in pams:
            hpn = 'PAM{:03d}'.format(_pam)
            sn = '{:03d}'.format(_pam)
            part_to_add[hpn] = (hpn, 'A', 'post-amp', sn)
        for _snap in snaps:
            hpn = 'SNP{}'.format(_snap)
            sn = '{}'.format(_snap)
            part_to_add[hpn] = (hpn, 'A', 'snap', sn)
        # Add node as station
        p = part_to_add['node-station']
        self.fp.write('add_station.py {} --sernum {} --date {} --time {}\n'.format(p[0], p[3], cdate, partadd_time))

        # Check for parts to add and add them
        for p in six.itervalues(part_to_add):
            if not p[0].startswith('ND'):  # Because add_station already added it
                if not self.exists('part', p[0], p[1], 'now'):
                    self.update_part('add', p, cdate, partadd_time)
                else:
                    print("Part {} is already added".format(p))

        # Add connections
        connection_to_add = []
        up = [part_to_add['node'][0], part_to_add['node'][1], '@ground']
        dn = [part_to_add['node-station'][0], part_to_add['node-station'][1], '@ground']
        connection_to_add.append([up, dn, cdate, connadd_time])
        up = [part_to_add['fem-power-supply'][0], part_to_add['fem-power-supply'][1], '@rack']
        dn = [part_to_add['node'][0], part_to_add['node'][1], '@top']
        connection_to_add.append([up, dn, cdate, connadd_time])
        up = [part_to_add['pam-chassis'][0], part_to_add['pam-chassis'][1], '@rack']
        dn = [part_to_add['node'][0], part_to_add['node'][1], '@bottom']
        connection_to_add.append([up, dn, cdate, connadd_time])
        up = [part_to_add['node-control-module'][0], part_to_add['node-control-module'][1], '@rack']
        dn = [part_to_add['node'][0], part_to_add['node'][1], '@middle']
        connection_to_add.append([up, dn, cdate, connadd_time])
        for i, _pam in enumerate(pams):
            hpn = 'PAM{:03d}'.format(_pam)
            up = [part_to_add[hpn][0], part_to_add[hpn][1], '@slot']
            dn = [part_to_add['pam-chassis'][0], part_to_add['pam-chassis'][1], '@slot{}'.format(i + 1)]
            connection_to_add.append([up, dn, cdate, connadd_time])
            for pol in ['e', 'n']:
                nbport = '{}{}'.format(pol, i + 1)
                up = [part_to_add['node-bulkhead'][0], part_to_add['node-bulkhead'][1], nbport]
                dn = [part_to_add[hpn][0], part_to_add[hpn][1], pol]
                connection_to_add.append([up, dn, cdate, connadd_time])
        for i, _snap in enumerate(snaps):
            snap_hpn = 'SNP{}'.format(_snap)
            up = [part_to_add[snap_hpn][0], part_to_add[snap_hpn][1], '@rack']
            dn = [part_to_add['node'][0], part_to_add['node'][1], '@loc{}'.format(i)]
            connection_to_add.append([up, dn, cdate, connadd_time])
            for pol in ['e', 'n']:
                for j in range(3):
                    pam_hpn = 'PAM{:03d}'.format(pams[i * 3 + j])
                    up = [part_to_add[pam_hpn][0], part_to_add[pam_hpn][1], pol]
                    dn = [part_to_add[snap_hpn][0], part_to_add[snap_hpn][1], self.snap_ports[j][pol]]
                    connection_to_add.append([up, dn, cdate, connadd_time])
        for up, down, codate, cotime in connection_to_add:
            if not self.exists('connection', hpn=up[0], rev=up[1], port=up[2], side='up', at_date=cdate):
                self.update_connection('add', up, down, codate, cotime)
            else:
                print("{} - {} are already connected".format(up, dn))

    def swap(self, old, new, cdate, ctime='13:00'):
        ptype = {'PAM': 'post-amp', 'FEM': 'front-end', 'SNP': 'snap'}
        cdt = cm_utils.get_astropytime(cdate, ctime)
        if not self.exists('part', hpn=old[0], rev=old[1], at_date=cdt):
            print("{} does not exist -- aborting swap".format(old[0]))
            return
        if not self.exists('part', hpn=new[0], rev=new[1], at_date=cdt):
            for ptk in ptype.keys():
                if new[0].upper().startswith(ptk):
                    break
            new = new + [ptype[ptk], new[0]]
            print("Adding new part {}".format(new))
            self.update_part('add', new, cdate, ctime)
        else:
            print("{} already added.".format(new[0]))
        old_pd = self.handle.get_part_dossier(hpn=old[0], rev=old[1], at_date=cdt, exact_match=True, full_version=True)
        old_pd_key = list(old_pd.keys())
        if len(old_pd_key) > 1:
            print("Too many connected parts")
            return
        opd = old_pd[old_pd_key[0]]
        print("Stopping connections: ")
        for key, val in six.iteritems(opd.connections.up):
            uppart = [val.upstream_part, val.up_part_rev, val.upstream_output_port]
            dnpart = [val.downstream_part, val.down_part_rev, val.downstream_input_port]
            self.update_connection('stop', uppart, dnpart, cdate, ctime)
        for key, val in six.iteritems(opd.connections.down):
            uppart = [val.upstream_part, val.up_part_rev, val.upstream_output_port]
            dnpart = [val.downstream_part, val.down_part_rev, val.downstream_input_port]
            self.update_connection('stop', uppart, dnpart, cdate, ctime)
        print("Adding connections: ")
        for key, val in six.iteritems(opd.connections.up):
            uppart = [val.upstream_part, val.up_part_rev, val.upstream_output_port]
            dnpart = [new[0], new[1], val.downstream_input_port]
            self.update_connection('add', uppart, dnpart, cdate, ctime)
        for key, val in six.iteritems(opd.connections.down):
            uppart = [new[0], new[1], val.upstream_output_port]
            dnpart = [val.downstream_part, val.down_part_rev, val.downstream_input_port]
            self.update_connection('add', uppart, dnpart, cdate, ctime)

    def done(self):
        print("\n----------------------DONE-----------------------")
        print("\tIf changes OK, 'chmod u+x {}' and run that script.".format(self.output_script))
        self.fp.close()
