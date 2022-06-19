# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
This class sets up to update the connections database.
"""
import datetime
from hera_mc import mc, cm_active, cm_utils, cm_sysdef
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
        self.active = None
        self.skipping = []
        self.disable_err = disable_err

    def pipe(self, node_csv='n'):
        self.load_gsheet(node_csv)
        self.load_active()
        self.make_sheet_connections()
        self.compare_connections()
        self.add_missing_parts()
        self.add_missing_connections()
        self.add_partial_connections()
        self.add_different_connections()
        self.add_rosetta()
        self.finish()
        self.show_summary_of_compare()

    def load_active(self):
        """
        Gets the hookup data from the hera_mc database.
        """
        db = mc.connect_to_mc_db(None)
        with db.sessionmaker() as session:
            self.active = cm_active.ActiveData(session=session)
            self.active.load_connections()

    def get_from_col(self, rtype, col, antpol, node, pre='', check=False):
        self.gsheet.data[antpol][self.gsheet.header[node].index(col)].lower()
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

        self.gsheet.connections is set up identically to self.active.connections
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
                    conn = self.active.connections[key]['up']['RACK']
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
        self.missing = {}
        self.partial = {}
        self.different = {}
        self.different_stop = {}
        self.same = {}
        if direction.startswith('g'):
            A = self.gsheet.connections[part_side]
            B = self.active.connections[part_side]
        else:
            A = self.active.connections[part_side]
            B = self.gsheet.connections[part_side]
        for this_part, pside_connections in A.items():
            if this_part not in B.keys():
                self.missing[this_part] = pside_connections
                continue
            for port, conn in pside_connections.items():
                if port not in B[this_part].keys():
                    self.partial.setdefault(this_part, {})
                    self.partial[this_part][port] = conn
                elif B[this_part][port] == conn:
                    self.same.setdefault(this_part, {})
                    self.same[this_part][port] = conn
                else:
                    self.different.setdefault(this_part, {})
                    self.different[this_part][port] = conn
                    self.different_stop.setdefault(this_part, {})
                    self.different_stop[this_part][port] = B[this_part][port]

    def add_missing_parts(self):
        self.active.load_parts()
        missing_parts = set()
        for pc in self.missing.values():
            for conn in pc.values():
                key = cm_utils.make_part_key(conn.upstream_part, conn.up_part_rev)
                if key not in self.active.parts.keys():
                    missing_parts.add(key)
                key = cm_utils.make_part_key(conn.downstream_part, conn.down_part_rev)
                if key not in self.active.parts.keys():
                    missing_parts.add(key)
        self.missing_parts = list(missing_parts)
        if len(self.missing_parts):
            self.hera.no_op_comment('Adding missing parts')
            add_part_time_offset = self.now - datetime.timedelta(seconds=300)
            cdate = add_part_time_offset.strftime('%Y/%m/%d')
            ctime = add_part_time_offset.strftime('%H:%M')
        for part in self.missing_parts:
            self.update_counter += 1
            p = list(cm_utils.split_part_key(part))
            try:
                this_part = p + [upd_base.signal_chain.part_types[part[:3]], p[0]]
            except KeyError:
                this_part = p + [upd_base.signal_chain.part_types[part[:2]], p[0]]
            self.hera.update_part('add', this_part, cdate=cdate, ctime=ctime)

    def add_missing_connections(self):
        if len(self.missing):
            self.hera.no_op_comment('Adding missing connections')
            self._modify_connections(self.missing, 'add', self.cdate, self.ctime)

    def stop_missing_connections(self, skip=[]):
        stopping = {}
        for missing_part, missing_connections in self.missing.items():
            use_it = True
            for sk in skip:
                if missing_part.startswith(sk):
                    use_it = False
                    break
            if use_it:
                stopping[missing_part] = missing_connections
        if len(stopping):
            self.hera.no_op_comment('Stopping missing connections')
            self._modify_connections(stopping, 'stop', self.cdate, self.ctime)

    def add_partial_connections(self):
        if len(self.partial):
            self.hera.no_op_comment('Adding partial connections')
            self._modify_connections(self.partial, 'add', self.cdate, self.ctime)

    def add_different_connections(self):
        if len(self.different):
            self.hera.no_op_comment('Adding different connections')
            stop_conn_time_offset = self.now - datetime.timedelta(seconds=90)
            cdate = stop_conn_time_offset.strftime('%Y/%m/%d')
            ctime = stop_conn_time_offset.strftime('%H:%M')
            self._modify_connections(self.different_stop, 'stop', cdate, ctime)
            self._modify_connections(self.different, 'add', self.cdate, self.ctime)

    def _modify_connections(self, this_one, add_or_stop, cdate, ctime):
        for mod_conn in this_one.values():
            for conn in mod_conn.values():
                self.update_counter += 1
                up = [conn.upstream_part, conn.up_part_rev, conn.upstream_output_port]
                dn = [conn.downstream_part, conn.down_part_rev, conn.downstream_input_port]
                self.hera.update_connection(add_or_stop, up, dn, cdate=cdate, ctime=ctime)

    def show_summary_of_compare(self):
        print("\n---Summary---")
        print("Missing:  {}".format(len(self.missing)))
        print("Same:  {}".format(len(self.same)))
        print("Skipping:  {}".format(len(self.skipping)))
        print("Partial:  {}".format(len(self.partial)), end='   ')
        if len(self.partial) and len(self.partial) < 5:
            print("*****CHECK*****")
            for p in self.partial:
                print("\t{}".format(p))
        else:
            print()
        print("Different:  {}".format(len(self.different)), end='   ')
        if len(self.different) and len(self.different) < 5:
            print("*****CHECK*****")
            for d in self.different:
                print("\t{}".format(d))
        else:
            print()
        print("Different_stop:  {}".format(len(self.different_stop)), end='   ')
        if len(self.different_stop) and len(self.different_stop) < 5:
            print("*****CHECK*****")
            for d in self.different_stop:
                print("\t{}".format(d))
        else:
            print()
