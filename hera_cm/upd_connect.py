# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
This class sets up to update the connections database.
"""
from hera_mc import cm_utils, cm_sysdef
from hera_mc import cm_partconnect as CMPC
from . import util, upd_base
from argparse import Namespace

cm_req = Namespace(hpn=cm_sysdef.hera_zone_prefixes, pol='all',
                   at_date='now', exact_match=False, hookup_type=None)


def node_based():
    return {('node', 'ground'): ('nodestation', 'ground'),
            ('fps', 'rack'): ('node', 'top'),
            ('ncm', 'rack'): ('node', 'middle'),
            ('pch', 'rack'): ('node', 'bottom'),
            ('wr', 'mnt'): ('ncm', 'mnt1'),
            ('rd', 'mnt'): ('ncm', 'mnt2')}


def ant_based(nd, pw, pc):
    return {('station', 'ground'): ('ant', 'ground'),
            ('ant', 'focus'): ('feed', 'input'),
            ('feed', 'terminals'): ('fem', 'input'),
            ('fem', 'pwr'): ('fps', pw),
            ('pam', 'slot'): ('pch', pc),
            ('snap', 'rack'): ('node', nd)}


def antpol_based(pl, bp, sn):
    return {('fem', pl): ('nbp', bp),
            ('nbp', bp): ('pam', pl),
            ('pam', pl): ('snap', sn)}


class UpdateConnect(upd_base.Update):
    pols = ['E', 'N']
    NotFound = "Not Found"
    part_side_dir = ['up', 'down']

    def __init__(self, script_type='connupd', script_path='default',
                 verbose=True, disable_err=False):
        super(UpdateConnect, self).__init__(script_type=script_type,
                                            script_path=script_path,
                                            verbose=verbose)
        self.disable_err = disable_err
        self.sysinfo = {'gsheet': {'conn': {}, 'parts': set()},
                        'active': {'conn': {}, 'parts': set()}}

    def pipe(self, node_csv='n', skip_stop=['H', 'W'], show=True,
             cron_script='conn', archive_to='', alert=None):
        self.load_gsheet(node_csv)
        self.load_active()
        self.make_sheet_connections()
        self.gsheet.check_found_antennas()
        self.make_connection_dictionaries_and_compare()
        self.modify_parts('add', 'gsheet_not_active')
        self.modify_connections('add', 'gsheet_not_active', skip=[])
        self.modify_connections('stop', 'active_not_gsheet', skip=skip_stop)
        self.finish(cron_script=cron_script, archive_to=archive_to, alert=alert)

    def get_from_col(self, rtype, col, antpol, node, pre='', check=False):
        if col:
            v = self.gsheet.data[antpol][self.gsheet.header[node].index(col)]
        else:
            v = ''
        if rtype == 'hpn':
            return util.gen_hpn(col, v)
        if rtype == 'port':
            port = f'{pre}{v.lower()}'
            if check:
                if port[0] != check[0].lower():
                    par = [col, antpol, node]
                    msg = f"{par}: port {port} and pol ({check}) don't match"
                    if self.disable_err:
                        print(msg)
                    else:
                        raise ValueError(msg)
            return port
        raise ValueError(f"rtype {rtype} not valid.")

    def make_sheet_connections(self):
        """
        Go through all of the sheet and make cm_partconnect.Connections for comparison.

        self.gsheet.connections is set up identically to self.hera.active.connections
        """
        self.gsheet.connections = {'up': {}, 'down': {}}  # To mirror cm_active
        # Make connections
        H = Namespace()
        for node in self.gsheet.tabs:
            # Node-based
            node_num = int(util.get_num(node))
            for part in ['node', 'nodestation', 'NBP']:
                setattr(H, part.lower(), util.gen_hpn(part, node_num))
            for part in ['fps', 'pch', 'ncm']:
                setattr(H, part.lower(), getattr(self.gsheet.node_to_equip[H.node], part))
            try:
                H.wr = self.gsheet.ncm[H.ncm].wr
                H.rd = self.gsheet.ncm[H.ncm].rdhpn
            except KeyError:
                H.wr = None
                H.rd = None
            for Up, Dn in node_based().items():
                self.create_sheet_conn(H, Up[0], Up[1], Dn[0], Dn[1])
            for station in self.gsheet.node_to_ant[node]:
                # Ant-based
                sant = f"{station}:A"
                H.station = station
                for col in ['Ant', 'Feed', 'FEM', 'PAM', 'SNAP', 'NBP/PAMloc', 'SNAPloc']:
                    A = self.get_from_col('hpn', col, f"{sant}-{self.pols[0]}", node)
                    B = self.get_from_col('hpn', col, f"{sant}-{self.pols[1]}", node)
                    if A != B:
                        if self.disable_err:
                            print(f'Error, but proceeding: {A} != {B}')
                        else:
                            raise ValueError(f'{A} != {B}')
                antpol = f"{sant}-E"  # pick E
                for part in ['Ant', 'FEM', 'Feed', 'PAM', 'SNAP']:
                    setattr(H, part.lower(), self.get_from_col('hpn', part, antpol, node))
                pw = self.get_from_col('port', 'NBP/PAMloc', antpol, node, 'pwr')
                pc = self.get_from_col('port', 'NBP/PAMloc', antpol, node, 'slot')
                nd = self.get_from_col('port', 'SNAPloc', antpol, node, 'loc')
                for Up, Dn in ant_based(nd, pw, pc).items():
                    self.create_sheet_conn(H, Up[0], Up[1], Dn[0], Dn[1])
                for pol in self.pols:
                    # Antpol-based
                    antpol = '{}-{}'.format(sant, pol)
                    bp = self.get_from_col('port', 'NBP/PAMloc', antpol, node, pol)
                    sn = self.get_from_col('port', 'Port', antpol, node, '', check=pol)
                    for Up, Dn in antpol_based(pol.lower(), bp, sn).items():
                        self.create_sheet_conn(H, Up[0], Up[1], Dn[0], Dn[1])

    def create_sheet_conn(self, H, Up_part, Up_port, Dn_part, Dn_port):
        uprev = 'H' if Up_part.lower() == 'ant' else 'A'
        dnrev = 'H' if Dn_part.lower() == 'ant' else 'A'
        Up = [getattr(H, Up_part.lower()), uprev, Up_port]
        Dn = [getattr(H, Dn_part.lower()), dnrev, Dn_port]

        if None in Up or None in Dn:
            return
        if not len(Up[0]) or not len(Dn[0]):
            return
        keys = {'up': cm_utils.make_part_key(Up[0], Up[1]),
                'down': cm_utils.make_part_key(Dn[0], Dn[1])}
        port = {'up': Up[2].lower(), 'down': Dn[2].lower()}
        for dir, key in keys.items():
            self.gsheet.connections[dir].setdefault(key, {})
            if port[dir] in self.gsheet.connections[dir][key]:
                continue
            self.gsheet.connections[dir][key][port[dir]] = CMPC.Connections()
            self.gsheet.connections[dir][key][port[dir]].connection(
                upstream_part=Up[0], up_part_rev=Up[1],
                upstream_output_port=Up[2],
                downstream_part=Dn[0], down_part_rev=Dn[1],
                downstream_input_port=Dn[2])

    def add_rosetta(self):
        for t2u in ['missing', 'different']:
            t2u_attr = getattr(self, t2u)
            if not len(t2u_attr):
                continue
            self.hera.no_op_comment('Adding {} parts'.format(t2u))
            for key in t2u_attr:
                if not key.startswith('SNP'):
                    continue
                try:
                    conn = self.hera.active.connections[key]['up']['RACK']
                    hname = "heraNode{}Snap{}".format(int(conn.downstream_part[1:]),
                                                      int(conn.downstream_input_port[-1]))
                    self.hera.add_part_rosetta(conn.upstream_part, hname, self.cdate, self.ctime)
                except KeyError:
                    with open('upd_connect.log', 'a') as fp:
                        print(f"Need to put {key} in active connections.", file=fp)

    def make_connection_dictionaries_and_compare(self):
        for sysinfo_type in ['gsheet', 'active']:
            if sysinfo_type == 'gsheet':
                use_sys = self.gsheet.connections
            elif sysinfo_type == 'active':
                use_sys = self.hera.active.connections
            for part_side in self.part_side_dir:
                for this_part, pside_conn in use_sys[part_side].items():
                    for port, conn in pside_conn.items():
                        self.sysinfo[sysinfo_type]['conn'][str(conn).upper()] = conn
                        key = cm_utils.make_part_key(conn.upstream_part, conn.up_part_rev)
                        self.sysinfo[sysinfo_type]['parts'].add(key)
                        key = cm_utils.make_part_key(conn.downstream_part, conn.down_part_rev)
                        self.sysinfo[sysinfo_type]['parts'].add(key)
        self.diffs = {'gsheet_not_active': {}, 'active_not_gsheet': {}}
        self.diffs['gsheet_not_active'] = {'conn': [], 'parts': []}
        for key in self.sysinfo['gsheet']['conn']:
            if key not in self.sysinfo['active']['conn'].keys():
                self.diffs['gsheet_not_active']['conn'].append(key)
        for part in self.sysinfo['gsheet']['parts']:
            if part not in self.sysinfo['active']['parts']:
                self.diffs['gsheet_not_active']['parts'].append(part)

        self.diffs['active_not_gsheet'] = {'conn': [], 'parts': []}
        for key in self.sysinfo['active']['conn']:
            if key not in self.sysinfo['gsheet']['conn'].keys():
                self.diffs['active_not_gsheet']['conn'].append(key)
        for part in self.sysinfo['active']['parts']:
            if part not in self.sysinfo['gsheet']['parts']:
                self.diffs['active_not_gsheet']['parts'].append(part)

    def modify_parts(self, add_or_stop='add', sysinfo='gsheet_not_active'):
        if not len(self.diffs[sysinfo]['parts']):
            if self.verbose:
                print(f"No parts to {add_or_stop} for {sysinfo}")
            return
        self.hera.no_op_comment(f'{add_or_stop} parts for {sysinfo}')
        cdate, ctime = util.YMD_HM(self.cdatetime, -1.0 / 24.0)
        for prev in self.diffs[sysinfo]['parts']:
            self.update_counter += 1
            part, rev = cm_utils.split_part_key(prev)
            pref = part.strip(util.get_num(part))
            t_part = upd_base.signal_chain.get_part_type(pref)
            this_part = [part, rev, t_part, part]
            self.hera.update_part(add_or_stop, this_part, cdate=cdate, ctime=ctime)

    def include_it(self, conn, skip):
        for sk in skip:
            if conn.upstream_part.startswith(sk) or conn.downstream_part.startswith(sk):
                return False
        return True

    def modify_connections(self, add_or_stop, sysinfo, skip=[]):
        if not len(self.diffs[sysinfo]['conn']):
            if self.verbose:
                print(f"No connections to {add_or_stop} for {sysinfo}")
            return
        self.hera.no_op_comment(f'{add_or_stop} connections for {sysinfo}')
        cdate, ctime = util.YMD_HM(self.cdatetime, 0.0)
        this_one = sysinfo.split('_')[0]
        for connkey in self.diffs[sysinfo]['conn']:
            conn = self.sysinfo[this_one]['conn'][connkey]
            if self.include_it(conn, skip):
                self.update_counter += 1
                up = [conn.upstream_part, conn.up_part_rev, conn.upstream_output_port]
                dn = [conn.downstream_part, conn.down_part_rev, conn.downstream_input_port]
                self.hera.update_connection(add_or_stop, up, dn, cdate=cdate, ctime=ctime)

    def show_summary_of_compare(self, direction, part_side):
        from tabulate import tabulate
        table = []
        print(f"Summary:  {direction} {part_side}")
        print(tabulate(table), '\n')

    def check_active(self):
        from hera_mc import cm_partconnect as partconn
        from hera_mc import mc

        gps_time = cm_utils.get_astropytime(self.cdatetime).gps
        dupconn = {"up": {}, "down": {}}
        check_keys = {"up": [], "down": []}

        duplicates = False
        with mc.MCSessionWrapper() as session:
            for cnn in session.query(partconn.Connections).filter(
                (partconn.Connections.start_gpstime <= gps_time)
                & (
                    (partconn.Connections.stop_gpstime > gps_time)
                    | (partconn.Connections.stop_gpstime == None)  # noqa
                )
            ):
                chk = cm_utils.make_part_key(
                    cnn.upstream_part, cnn.up_part_rev, cnn.upstream_output_port
                )
                if chk in check_keys["up"]:
                    duplicates = True
                dupconn['up'].setdefault(chk, [])
                dupconn['up'][chk].append(str(cnn))
                check_keys["up"].append(chk)
                chk = cm_utils.make_part_key(
                    cnn.downstream_part, cnn.down_part_rev, cnn.downstream_input_port
                )
                if chk in check_keys["down"]:
                    duplicates = True
                dupconn['down'].setdefault(chk, [])
                dupconn['down'][chk].append(str(cnn))
                check_keys["down"].append(chk)

        if duplicates:
            print("Showing duplicates:")
            print("----------------------------UP-----------------------")
            for key, val in dupconn['up'].items():
                if len(val) > 1:
                    pval = [f"{x.strip('<').strip('>'):<40}" for x in val]
                    print(f"{key:<20}  {' '.join(pval)}")
            print("--------------------------DOWN-----------------------")
            for key, val in dupconn['down'].items():
                if len(val) > 1:
                    pval = [f"{x.strip('<').strip('>'):<40}" for x in val]
                    print(f"{key:<20}  {' '.join(pval)}")
