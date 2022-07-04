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


class UpdateConnect(upd_base.Update):
    pols = ['E', 'N']
    NotFound = "Not Found"

    def __init__(self, script_type='connupd', script_path='default',
                 verbose=True, disable_err=False):
        super(UpdateConnect, self).__init__(script_type=script_type,
                                            script_path=script_path,
                                            verbose=verbose)
        self.disable_err = disable_err
        self.missing = {'all': {}, 'ports': {}}
        self.different = {'A': {}, 'B': {}}
        self.same = {}
        self.included = {'connections': [], 'parts': []}

    def pipe(self, node_csv='n', skip=['H', 'W'], show=True,
             cron_script='', archive_to='', alert=None):
        self.load_gsheet(node_csv)
        self.load_active()
        self.make_sheet_connections()
        for direction in ['active-gsheet', 'gsheet-active']:
            for part_side in ['up', 'down']:
                self.compare_connections(direction, part_side)
                if show:
                    self.show_summary_of_compare(direction, part_side)
        self.add_missing_parts('gsheet-active')
        self.missing_connections('add', 'gsheet-active', skip)
        self.missing_connections('stop', 'active-gsheet', skip)
        self.different_connections('gsheet-active', skip)
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
            for part in ['Node', 'node-station', 'NBP']:
                setattr(H, part.lower(), util.gen_hpn(part, node_num))
            for part in ['fps', 'pch', 'ncm']:
                setattr(H, part.lower(), getattr(self.gsheet.node_to_equip[H.node], part))
            H.wr = self.gsheet.ncm[H.ncm].wr
            H.rd = self.gsheet.ncm[H.ncm].rdhpn
            for Up, Dn in zip([('fps', 'rack'), ('ncm', 'rack'), ('pch', 'rack'),
                               ('node', 'ground'), ('wr', 'mnt'), ('rd', 'mnt')],
                              [('node', 'top'), ('node', 'middle'), ('node', 'bottom'),
                               ('node-station', 'ground'), ('ncm', 'mnt1'), ('ncm', 'mnt2')]):
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
                for Up, Dn in zip([('station', 'ground'), ('feed', 'terminals'), ('snap', 'rack'),
                                   ('ant', 'focus'), ('fem', 'pwr'), ('pam', 'slot')],
                                  [('ant', 'ground'), ('fem', 'input'), ('node', nd),
                                   ('feed', 'input'), ('fps', pw), ('pch', pc)]):
                    self.create_sheet_conn(H, Up[0], Up[1], Dn[0], Dn[1])
                for pol in self.pols:
                    # Antpol-based
                    antpol = '{}-{}'.format(sant, pol)
                    pl = pol.lower()
                    bp = self.get_from_col('port', 'NBP/PAMloc', antpol, node, pol)
                    sn = self.get_from_col('port', 'Port', antpol, node, '', check=pol)
                    for Up, Dn in zip([('fem', pl), ('nbp', bp), ('pam', pl)],
                                      [('nbp', bp), ('pam', pl), ('snap', sn)]):
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
        port = {'up': Up[2].upper(), 'down': Dn[2].upper()}
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

    def compare_connections(self, direction='gsheet-active', part_side='up'):
        """
        Step through all of the sheet Connections and make sure they are all there and the same.
        """
        self.compare_direction = direction
        self.compare_part_side = part_side
        self.missing['all'].setdefault(direction, {})
        self.missing['all'][direction].setdefault(part_side, {})
        self.missing['ports'].setdefault(direction, {})
        self.missing['ports'][direction].setdefault(part_side, {})
        self.different['A'].setdefault(direction, {})
        self.different['A'][direction].setdefault(part_side, {})
        self.different['B'].setdefault(direction, {})
        self.different['B'][direction].setdefault(part_side, {})
        self.same.setdefault(direction, {})
        self.same[direction].setdefault(part_side, {})
        if direction.startswith('g'):
            A = self.gsheet.connections[part_side]
            B = self.hera.active.connections[part_side]
        else:
            A = self.hera.active.connections[part_side]
            B = self.gsheet.connections[part_side]
        for this_part, pside_connections in A.items():
            if this_part not in B.keys():
                self.missing['all'][direction][part_side][this_part] = pside_connections
                continue
            for port, conn in pside_connections.items():
                if port not in B[this_part].keys():
                    self.missing['ports'][direction][part_side].setdefault(this_part, {})
                    self.missing['ports'][direction][part_side][this_part][port] = conn
                elif B[this_part][port] == conn:
                    self.same[direction][part_side].setdefault(this_part, {})
                    self.same[direction][part_side][this_part][port] = conn
                else:
                    self.different['A'][direction][part_side].setdefault(this_part, {})
                    self.different['A'][direction][part_side][this_part][port] = conn
                    self.different['B'][direction][part_side].setdefault(this_part, {})
                    self.different['B'][direction][part_side][this_part][port] = B[this_part][port]

    def add_missing_parts(self, direction):
        if self.hera.active.parts is None:
            self.hera.active.load_parts()
        missing_parts = set()
        for part_side in ['up', 'down']:
            for pc in self.missing['all'][direction][part_side].values():
                for conn in pc.values():
                    key = cm_utils.make_part_key(conn.upstream_part, conn.up_part_rev)
                    if key not in self.hera.active.parts.keys():
                        missing_parts.add(key)
                    key = cm_utils.make_part_key(conn.downstream_part, conn.down_part_rev)
                    if key not in self.hera.active.parts.keys():
                        missing_parts.add(key)
        self.missing_parts = list(missing_parts)
        if len(self.missing_parts):
            self.hera.no_op_comment('Adding missing parts')
            cdate, ctime = util.YMD_HM(self.cdatetime, -1.0 / 24.0)
        for part in self.missing_parts:
            part_str = str(part)
            if part_str in self.included['parts']:
                print(f"{part} already added - skipping")
                continue
            else:
                self.included['parts'].append(part_str)
            self.update_counter += 1
            p = list(cm_utils.split_part_key(part))
            try:
                this_part = p + [upd_base.signal_chain.part_types[part[:3]], p[0]]
            except KeyError:
                this_part = p + [upd_base.signal_chain.part_types[part[:2]], p[0]]
            self.hera.update_part('add', this_part, cdate=cdate, ctime=ctime)

    def missing_connections(self, rtype, direction, skip=[]):
        modifying = {}
        for mtype in ['all', 'ports']:
            for part_side in ['up', 'down']:
                for missing_part, missing_connections in self.missing[mtype][direction][part_side].items():  # noqa
                    if self.include_it(missing_part, missing_connections, skip):
                        modifying[missing_part] = missing_connections
        for modify in modifying:
            self.hera.no_op_comment(f'{rtype} missing_{mtype} connections')
            self._modify_connections(modifying, rtype, self.cdate, self.ctime)

    def different_connections(self, direction, skip=[]):
        add_diff = {}
        stop_diff = {}
        for part_side in ['up', 'down']:
            for diff_part, diff_connections in self.different['A'][direction][part_side].items():
                if self.include_it(diff_part, diff_connections, skip):
                    add_diff[diff_part] = diff_connections
            for diff_part, diff_connections in self.different['B'][direction][part_side].items():
                if self.include_it(diff_part, diff_connections, skip):
                    stop_diff[diff_part] = diff_connections
        if len(add_diff):
            self.hera.no_op_comment('Adding connections that differ')
            self._modify_connections(stop_diff, 'add', self.cdate, self.ctime)
        if len(stop_diff):
            self.hera.no_op_comment('Stopping connections that differ')
            cdate, ctime = util.YMD_HM(self.cdatetime, -1.0 / 24.0)
            self._modify_connections(stop_diff, 'stop', cdate, ctime)

    def include_it(self, part, conns, skip):
        for sk in skip:
            if part.startswith(sk):
                return False
        for port, conn in conns.items():
            for sk in skip:
                if conn.upstream_part.startswith(sk) or conn.downstream_part.startswith(sk):
                    return False
            conn_str = str(conn)
            if conn_str in self.included['connections']:
                print(f"INFO: {conn_str} already included - skipping")
                return False
            self.included['connections'].append(conn_str)
        return True

    def _modify_connections(self, this_one, add_or_stop, cdate, ctime):
        for mod_conn in this_one.values():
            for conn in mod_conn.values():
                self.update_counter += 1
                up = [conn.upstream_part, conn.up_part_rev, conn.upstream_output_port]
                dn = [conn.downstream_part, conn.down_part_rev, conn.downstream_input_port]
                self.hera.update_connection(add_or_stop, up, dn, cdate=cdate, ctime=ctime)

    def show_summary_of_compare(self, direction, part_side):
        from tabulate import tabulate
        table = []
        print(f"Summary:  {direction} {part_side}")
        for rtype in ['all', 'ports']:
            table.append(["Missing", rtype, len(self.missing[rtype][direction][part_side])])
        for rtype in ['A', 'B']:
            table.append(["Different", rtype, len(self.different[rtype][direction][part_side])])
        table.append(["Same", "", len(self.same[direction][part_side])])
        for rtype in ['parts', 'connections']:
            table.append(["Included", rtype, len(self.included[rtype])])
        print(tabulate(table), '\n')

    def check_active(self):
        from hera_mc import cm_partconnect as partconn
        from hera_mc import mc
        from copy import copy

        gps_time = cm_utils.get_astropytime(self.cdatetime).gps
        self.connections = {"up": {}, "down": {}}
        check_keys = {"up": [], "down": []}

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
                    print("CHECK ERROR: Duplicate active port {}".format(chk))
                check_keys["up"].append(chk)
                chk = cm_utils.make_part_key(
                    cnn.downstream_part, cnn.down_part_rev, cnn.downstream_input_port
                )
                if chk in check_keys["down"]:
                    print("CHECK ERROR: Duplicate active port {}".format(chk))
                check_keys["down"].append(chk)
                key = cm_utils.make_part_key(cnn.upstream_part, cnn.up_part_rev)
                self.connections["up"].setdefault(key, {})
                self.connections["up"][key][cnn.upstream_output_port.upper()] = copy(cnn)
                key = cm_utils.make_part_key(cnn.downstream_part, cnn.down_part_rev)
                self.connections["down"].setdefault(key, {})
                self.connections["down"][key][cnn.downstream_input_port.upper()] = copy(cnn)
