import os
from hera_mc import cm_utils, cm_active, cm_handling

current_revs = {'HH': 'A', 'A': 'H', 'FDV': 'V'}
part_types = {'FDV': 'feed', 'FEM': 'front-end', 'NBP': 'node-bulkhead',
              'PAM': 'post-amp', 'SNP': 'snap'}


def as_part(add_or_stop, p, cdate, ctime):
    s = '{}_part.py -p {} -r {} '.format(
        add_or_stop, p[0], p[1])
    if add_or_stop == 'add':
        s += '-t {} -m {} '.format(p[2], p[3])
    s += '--date {} --time {}'.format(cdate, ctime)
    s += '\n'
    return s


def as_connect(add_or_stop, up, dn, cdate, ctime):
    s = '{}_connection.py -u {} --uprev {} --upport {} -d {} --dnrev {} --dnport {}'\
        ' --date {} --time {}\n'.format(add_or_stop, up[0], up[1], up[2],
                                        dn[0], dn[1], dn[2], cdate, ctime)
    return s


class Update:
    snap_ports = [{'e': 'e2', 'n': 'n0'}, {'e': 'e6', 'n': 'n4'}, {'e': 'e10', 'n': 'n8'}]

    def __init__(self, exename, output_script_path=None, chmod=False, cdate='now', ctime='10:00',
                 log_file='scripts.log', verbose=True):
        """
        exename:  the name of the script executed (argv[0])
        log_file:  name of log_file
        """
        self.verbose = verbose
        self.chmod = chmod
        self.log_file = log_file
        self.at_date = cm_utils.get_astropytime(cdate, ctime)
        self.active = cm_active.ActiveData()
        self.load_active(cdate=None)
        self.handle = cm_handling.Handling()
        input_script = os.path.basename(exename)
        if output_script_path is None:
            self.output_script = input_script.split('.')[0]
        else:
            self.output_script = os.path.join(output_script_path, input_script.split('.')[0])
        if self.verbose:
            print("Writing script {}".format(self.output_script))
        self.fp = open(self.output_script, 'w')
        s = '#! /bin/bash\n'
        unameInfo = os.uname()
        if unameInfo.sysname == 'Linux':
            s += 'source ~/.bashrc\n'
        s += 'echo "{}" >> {} \n'.format(exename, self.log_file)
        self.fp.write(s)
        if self.verbose:
            print('-----------------')

    # THESE ARE NEW COMPONENTS - eventually break out with a parent class
    # General order:
    #   add_antenna_station : when it is built
    #   add_node            : when all equipment installed in node
    #   add_antenna_to_node : when a feed/fem etc is installed and hooked into node

    def update__at_date(self, cdate='now', ctime='10:00'):
        self.at_date = cm_utils.get_astropytime(adate=cdate, atime=ctime)

    def no_op_comment(self, comment):
        self.fp.write('# {}\n'.format(comment.strip()))

    def load_active(self, cdate='now', ctime='10:00'):
        if cdate is None:
            at_date = self.at_date
        else:
            at_date = cm_utils.get_astropytime(cdate, ctime)
        self.active.load_parts(at_date=at_date)
        self.active.load_connections(at_date=None)
        self.active.info = []
        self.active.geo = []

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
        added = {'station': [], 'part': [], 'connection': []}
        added['time'] = str(int(cm_utils.get_astropytime(cdate, ctime).gps))
        s = "HH{}".format(stn)
        a = "A{}".format(stn)
        n = "S/N{}".format(ser_num)
        self.fp.write('add_station.py {} --sernum {} --date {} --time {}\n'
                      .format(s, ser_num, cdate, ctime))
        added['station'].append([s, added['time']])
        added['part'].append([s, 'A', 'station', n, added['time']])
        check_date = cm_utils.get_astropytime(cdate=cdate, ctime=ctime)

        if not self.exists('part', a, 'H', check_date=check_date):
            ant = [a, 'H', 'antenna', n]
            self.update_part('add', ant, cdate, ctime)
            ant.append(added['time'])
            added['part'].append(ant)
        else:
            print("Part {} is already added".format(a))

        up = [s, 'A', 'ground']
        down = [a, 'H', 'ground']
        if not self.exists('connection', hpn=s, rev='A', port='ground', side='up',
                           check_date=check_date):
            self.update_connection('add', up, down, cdate, ctime)
            conn = [up[0], up[1], down[0], down[1], up[2], down[2], added['time']]
            added['connection'].append(conn)
        return added

    def add_node(self, node, fps, pch, ncm, pams, snaps, cdate, ctime=['10:00', '11:00'],
                 ser_num={}, override=False):
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
                allow for non-standard number of pams and/or snaps and ignore date
        """
        #  Setup/check overrides
        overridable_parts = {'pam': [12, len(pams)], 'snap': [4, len(snaps)]}
        for ox in overridable_parts.keys():
            if isinstance(override, bool):
                ovrd = override
            else:
                ovrd = False if ox not in override.keys() else override[ox]
            if not ovrd and overridable_parts[ox][0] != overridable_parts[ox][1]:
                print("Need {} {}s - you've supplied {}"
                      .format(overridable_parts[ox][0], ox, overridable_parts[ox][1]))
                print("If ok, rerun with <override['{}']=True>".format(ox))
                return

        if isinstance(ctime, list):
            partadd_time = ctime[0]
            connadd_time = ctime[1]
        else:
            partadd_time = ctime
            connadd_time = ctime
        added = {'part': [], 'connection': []}
        added['time'] = str(int(cm_utils.get_astropytime(cdate, partadd_time).gps))
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
        sn = self.get_ser_num(hpn, 'node')
        part_to_add['node-station'] = (hpn, 'A', 'station', sn)
        hpn = 'NBP{:02d}'.format(node)
        sn = self.get_ser_num(hpn, 'node')
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
        self.fp.write('add_station.py {} --sernum {} --date {} --time {}\n'
                      .format(p[0], p[3], cdate, partadd_time))

        # Check for parts to add and add them
        if isinstance(override, dict) and 'date' in override.keys():
            check_date = override['date']
        else:
            check_date = cm_utils.get_astropytime(adate=cdate, atime=partadd_time)
        for p in part_to_add.values():
            if not p[0].startswith('ND'):  # Because add_station already added it
                if not self.exists('part', p[0], p[1], None, check_date=check_date):
                    self.update_part('add', p, cdate, partadd_time)
                    added['part'].append(list(p) + [added['time']])
                else:
                    print("Part {} is already added".format(p))

        # Add connections
        added['time'] = str(int(cm_utils.get_astropytime(cdate, connadd_time).gps))
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
            dn = [part_to_add['pam-chassis'][0], part_to_add['pam-chassis'][1],
                  '@slot{}'.format(i + 1)]
            connection_to_add.append([up, dn, cdate, connadd_time])
            for pol in ['e', 'n']:
                nbport = '{}{}'.format(pol, i + 1)
                up = [part_to_add['node-bulkhead'][0], part_to_add['node-bulkhead'][1], nbport]
                dn = [part_to_add[hpn][0], part_to_add[hpn][1], pol]
                connection_to_add.append([up, dn, cdate, connadd_time])
        for i, _snap in enumerate(snaps):
            snap_hpn = 'SNP{}'.format(_snap)
            up = [part_to_add[snap_hpn][0], part_to_add[snap_hpn][1], 'rack']
            dn = [part_to_add['node'][0], part_to_add['node'][1], 'loc{}'.format(i)]
            connection_to_add.append([up, dn, cdate, connadd_time])
            for pol in ['e', 'n']:
                for j in range(3):
                    pam_hpn = 'PAM{:03d}'.format(pams[i * 3 + j])
                    up = [part_to_add[pam_hpn][0], part_to_add[pam_hpn][1], pol]
                    dn = [part_to_add[snap_hpn][0], part_to_add[snap_hpn][1],
                          self.snap_ports[j][pol]]
                    connection_to_add.append([up, dn, cdate, connadd_time])
        for up, down, codate, cotime in connection_to_add:
            if isinstance(override, dict) and 'date' in override.keys():
                check_date = override['date']
            else:
                check_date = cm_utils.get_astropytime(adate=codate, atime=cotime)
            if not self.exists('connection', hpn=up[0], rev=up[1], port=up[2], side='up',
                               check_date=check_date):
                self.update_connection('add', up, down, codate, cotime)
                added['connection'].append([up[0], up[1], down[0], down[1],
                                            up[2], down[2], added['time']])
            else:
                print("{} - {} are already connected".format(up, dn))
        return added

    def add_antenna_to_node(self, ant, feed, fem, node, nbp_port,
                            cdate, ctime=['10:00', '11:00'], ser_num={}, override=False):
        """
        Parameters:
        -----------
        ant:  antenna number (int)
        feed: feed number (int)
        fem: fem number (int)
        node:  node number (int)
        nbp_port:  port number on node bulkhead plate (int)
        ser_no:  dictionary of serial numbers (keyed by part-type, uses hpn if not included
        cdate:  YYYY/MM/DD - date of mods (one for all)
        ctime:  time of mods <'10:00', '11:00'>
                ['HH:MM', 'HH:MM'] for part at [0], connection at [1]
                'HH:MM' for part/connection at 'HH:MM'
        override : bool, dict
        """

        if isinstance(ctime, list):
            partadd_time = ctime[0]
            connadd_time = ctime[1]
        else:
            partadd_time = ctime
            connadd_time = ctime
        self.ser_num_dict = ser_num
        added = {'part': [], 'connection': []}

        # Set up parts
        part_to_add = {}

        hpn = 'FDV{}'.format(feed)
        sn = self.get_ser_num(hpn, 'feed')
        part_to_add['feed'] = (hpn, 'A', 'feed', sn)

        hpn = 'FEM{:03d}'.format(fem)
        sn = self.get_ser_num(hpn, 'front-end')
        part_to_add['fem'] = (hpn, 'A', 'front-end', sn)

        # Check for parts to add and add them
        added['time'] = str(int(cm_utils.get_astropytime(cdate, partadd_time).gps))
        if isinstance(override, dict) and 'date' in override.keys():
            check_date = override['date']
        else:
            check_date = cm_utils.get_astropytime(adate=cdate, atime=partadd_time)
        for k, p in part_to_add.items():
            if self.exists('part', p[0], p[1], None, check_date=check_date):
                print("{} {} is already added".format(k, p[0]))
            else:
                self.update_part('add', p, cdate, partadd_time)
                added['part'].append(list(p) + [added['time']])

        # These added after, since already included in add_station/add_node
        hpn = 'A{}'.format(ant)
        part_to_add['ant'] = (hpn, 'H')

        hpn = 'NBP{:02d}'.format(node)
        part_to_add['nbp'] = (hpn, 'A')

        # Set up connections
        connection_to_add = []

        up = [part_to_add['ant'][0], part_to_add['ant'][1], 'focus']
        dn = [part_to_add['feed'][0], part_to_add['feed'][1], 'input']
        connection_to_add.append([up, dn, cdate, connadd_time])

        up = [part_to_add['feed'][0], part_to_add['feed'][1], 'terminals']
        dn = [part_to_add['fem'][0], part_to_add['fem'][1], 'input']
        connection_to_add.append([up, dn, cdate, connadd_time])

        up = [part_to_add['fem'][0], part_to_add['fem'][1], 'e']
        dn = [part_to_add['nbp'][0], part_to_add['nbp'][1], 'e{}'.format(nbp_port)]
        connection_to_add.append([up, dn, cdate, connadd_time])
        up = [part_to_add['fem'][0], part_to_add['fem'][1], 'n']
        dn = [part_to_add['nbp'][0], part_to_add['nbp'][1], 'n{}'.format(nbp_port)]
        connection_to_add.append([up, dn, cdate, connadd_time])

        # Check for connections to add and add them
        added['time'] = str(int(cm_utils.get_astropytime(cdate, connadd_time).gps))
        for up, down, codate, cotime in connection_to_add:
            if isinstance(override, dict) and 'date' in override.keys():
                check_date = override['date']
            else:
                check_date = cm_utils.get_astropytime(cdate=codate, ctime=cotime)
            if not self.exists('connection', hpn=up[0], rev=up[1], port=up[2],
                               side='up', check_date=check_date):
                self.update_connection('add', up, down, codate, cotime)
                added['connection'].append([up[0], up[1], down[0], down[1],
                                            up[2], down[2], added['time']])
        print('\n')

        return added

    # ##########################################################################################

    def get_general_part(self, hpn, rev=None, at_date=None):
        """
        This will return a list to add if the part does not exist or
        None if it does (or rev/type can't be found)
        """
        if rev is None:
            for key, val in current_revs.items():
                if hpn.startswith(key):
                    rev = val
                    break
        ptype = None
        for key, val in part_types.items():
            if hpn.startswith(key):
                ptype = val
                break
        if rev is None or ptype is None:
            return None
        if self.exists('part', hpn=hpn, rev=rev, port=None, side='up,down', check_date=at_date):
            return None
        return (hpn, rev, ptype, hpn)

    def get_ser_num(self, hpn, part_type):
        """
        Pull the serial number out of the class dictionary.  If none, just use the hpn
        """
        sn = hpn
        if part_type in self.ser_num_dict.keys():
            sn = self.ser_num_dict[part_type]
        return sn

    def to_implement(self, command, ant, rev, statement, pdate, ptime):
        stmt = "{} not implemented! {} {} {} {} {} {}\n".format(command, ant, rev,
                                                                statement, pdate, ptime)
        self.fp.write(stmt)
        print("{}".format(stmt.strip()))

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
        up:  upstream connection [part, rev, port]
        down:  downstream connection [part, rev, port]
        cdate:  date of update YYYY/MM/DD
        ctime:  time of update HH:MM
        """
        self.fp.write(as_connect(add_or_stop, up, down, cdate, ctime))

    def exists(self, atype, hpn, rev, port, side='up,down', check_date=None):
        """
        Check if a part or connection exists for hpn

        Parameters
        ----------
        atype :  str
              'part' or 'connection'
        hpn : str
              HERA part number to check.  Can be a list of strings or a csv-list
        rev : str, list or None
              Revisions to check.  If None checks if any rev present.
        port : str, list or None
               Ports to check.  If None checks if any port is present.
        side : str
               "side" of part to check.  Options are:  up, down, or up,down (default)
        check_date : anything for cm_utils.get_astropytime
                     if None, it will warn if class and active don't agree (arb 1sec)
                     if not None, it will raise error if method and active don't agree (arb 1sec)
        Return
        ------
        boolean
                 True if existing corresponding hpn/rev/port
        """
        if check_date is None:
            if abs(self.at_date - self.active.at_date) > 1.0:
                print("Warning:  class and active dates do not agree.")
        else:
            if cm_utils.get_astropytime(check_date) - self.active.at_date < 0.0:
                raise ValueError("Supplied date before active.at_date.")
        if rev is None:
            rev = cm_active.revs(hpn)
        elif isinstance(rev, str):
            rev = [rev]
        active_part = False
        for r in rev:
            part_key = cm_utils.make_part_key(hpn, r)
            if part_key in self.active.parts.keys():
                active_part = True
                break
        if atype.startswith('part') or not active_part:
            return active_part

        if port is not None:
            sides = side.split(',')
            if isinstance(port, str):
                port = [port]
            for r in rev:
                part_key = cm_utils.make_part_key(hpn, r)
                for side in sides:
                    if part_key in self.active.connections[side].keys():
                        if port is None:
                            return True
                        for p in port:
                            if p.upper() in self.active.connections[side][part_key].keys():
                                return True
            return False

    def update_apriori(self, antenna, status, cdate, ctime='12:00'):
        """
        Update the antenna a priori status.

        Parameters
        ----------
        antenna : str
            Antenna part number, e.g. HH24
        status : str
            Antenna apriori enum string.
        cdate : str
            YYYY/MM/DD
        ctime : str, optional
            HH:MM, default is 12:00
        """

        self.fp.write('update_apriori.py -p {} -s {} --date {} --time {}\n'
                      .format(antenna, status, cdate, ctime))

    def add_part_info(self, hpn, rev, note, cdate, ctime, ref=None):
        """
        Add a note/comment for a part to the database

        Parameters
        ----------
        hpn : str
              HERA part number for comment
        rev : str
              Revision for comment.
        note : str
               The desired note.
        cdate : str
                YYYY/MM/DD format
        ctime : str
                HH:MM format
        ref : str
              Reference note.
        """
        if ref is None:
            ref = ''
        else:
            ref = '-l "{}" '.format(ref)
        self.fp.write('add_part_info.py -p {} -r {} -c "{}" {}--date {} --time {}\n'
                      .format(hpn, rev, note, ref, cdate, ctime))

    def replace(self, old, new, cdate, ctime='13:00'):
        """
        Replaces an old PAM, FEM or SNAP part, with a new one.
        If new is None, it just stops the old one.

        Parameters
        ----------
        old : list
            [old_hpn, old_rev]
        new : list
            [new_hpn, old_rev]
        cdate : str
            YYYY/MM/DD
        ctime : str, optional
            HH:MM, default is 13:00
        """
        ptype = {'PAM': 'post-amp', 'FEM': 'front-end', 'SNP': 'snap'}
        cdt = cm_utils.get_astropytime(cdate, ctime)
        if not self.exists('part', hpn=old[0], rev=old[1], check_date=cdt):
            print("{} does not exist -- aborting swap".format(old[0]))
            return
        replace_with_none = False
        if new is None:
            replace_with_none = True
            print("Only stopping old part.")
        else:
            if not self.exists('part', hpn=new[0], rev=new[1], check_date=cdt):
                for ptk in ptype.keys():
                    if new[0].upper().startswith(ptk):
                        break
                new = new + [ptype[ptk], new[0]]
                print("Adding new part {}".format(new))
                self.update_part('add', new, cdate, ctime)
            else:
                print("{} already added.".format(new[0]))
        old_pd = self.handle.get_dossier(hpn=old[0], rev=old[1], at_date=cdt,
                                         active=self.active, exact_match=True)
        old_pd_key = list(old_pd.keys())
        if len(old_pd_key) > 1:
            print("Too many connected parts")
            return
        opd = old_pd[old_pd_key[0]]
        print("Stopping old connections: ")
        for key, val in opd.connections.up.items():
            uppart = [val.upstream_part, val.up_part_rev, val.upstream_output_port]
            dnpart = [val.downstream_part, val.down_part_rev, val.downstream_input_port]
            self.update_connection('stop', uppart, dnpart, cdate, ctime)
        for key, val in opd.connections.down.items():
            uppart = [val.upstream_part, val.up_part_rev, val.upstream_output_port]
            dnpart = [val.downstream_part, val.down_part_rev, val.downstream_input_port]
            self.update_connection('stop', uppart, dnpart, cdate, ctime)
        if replace_with_none:
            return
        print("Adding connections: ")
        for key, val in opd.connections.up.items():
            uppart = [val.upstream_part, val.up_part_rev, val.upstream_output_port]
            dnpart = [new[0], new[1], val.downstream_input_port]
            self.update_connection('add', uppart, dnpart, cdate, ctime)
        for key, val in opd.connections.down.items():
            uppart = [new[0], new[1], val.upstream_output_port]
            dnpart = [val.downstream_part, val.down_part_rev, val.downstream_input_port]
            self.update_connection('add', uppart, dnpart, cdate, ctime)

    def done(self):
        self.fp.close()
        if self.verbose:
            print("----------------------DONE-----------------------")
        if not self.chmod:
            if self.verbose:
                print("If changes OK, 'chmod u+x {}' and run that script."
                      .format(self.output_script))
        else:
            os.chmod(self.output_script, 0o755)
            if self.verbose:
                print("Run {}".format(self.output_script))
