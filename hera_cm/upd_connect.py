# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
This class sets up to update the connections database.
"""
import datetime
from hera_mc import mc, cm_active, cm_utils, cm_sysdef
from hera_mc import cm_partconnect as CMPC
from . import util, cm_gsheet, upd_base
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

    def get_hpn_from_col(self, col, key, header):
        return util.gen_hpn(col, self.gsheet.data[key][header.index(col)])

    def load_active(self):
        """
        Gets the hookup data from the hera_mc database.
        """
        db = mc.connect_to_mc_db(None)
        with db.sessionmaker() as session:
            self.active = cm_active.ActiveData(session=session)
            self.active.load_connections()

    def _get_port(self, key, pol, hdr_item, tab):
        if hdr_item:
            pdes = self.gsheet.data[key][self.gsheet.header[tab].index(hdr_item)].lower()
        else:
            pdes = ''
        port = '{}{}'.format(pol, pdes)
        return port

    def make_sheet_connections(self):
        """
        Go through all of the sheet and make cm_partconnect.Connections for comparison.

        self.gsheet.connections is set up identically to self.active.connections
        """
        self.gsheet.connections = {'up': {}, 'down': {}}  # To mirror cm_active
        # Make node-based connections
        for node in self.gsheet.tabs:
            node_num = int(node[4:])
            node = util.gen_hpn('Node', node_num)
            # Make fps-node
            fps = self.gsheet.node_to_equip[node].fps
            self._create_sheet_conn([[fps, 'A', 'rack'], [node, 'A', 'top']])
            # ... pch-node
            pch = self.gsheet.node_to_equip[node].pch
            self._create_sheet_conn([[pch, 'A', 'rack'], [node, 'A', 'bottom']])
            # Make ncm-node
            ncm = self.gsheet.node_to_equip[node].ncm
            self._create_sheet_conn([[ncm, 'A', 'rack'], [node, 'A', 'middle']])
            # Make node and node station
            nsta = util.gen_hpn('node-station', node_num)
            self._create_sheet_conn([[node, 'A', 'ground'], [nsta, 'A', 'ground']])
            # Make white-rabbit and arduino
            wr = self.gsheet.ncm[ncm].wr
            rd = self.gsheet.ncm[ncm].rdhpn
            if len(wr):
                self._create_sheet_conn([[wr, 'A', 'mnt'], [ncm, 'A', 'mnt1']])
            if len(rd):
                self._create_sheet_conn([[rd, 'A', 'mnt'], [ncm, 'A', 'mnt2']])
        # Make ~antenna-based connections
        for sant in self.gsheet.ants + self.gsheet.other:
            previous = {}
            for pol in self.pols:
                gkey = '{}-{}'.format(sant, pol)
                node_num = self.gsheet.data[gkey][0]
                node = util.gen_hpn("Node", node_num)
                tab = self.gsheet.ant_to_node[sant]
                header = self.gsheet.header[tab]
                for i, col in enumerate(header):
                    if col not in cm_gsheet.hu_col.keys():
                        continue
                    if col in ['Ant', 'Feed', 'SNAP'] and pol == self.pols[1]:
                        # Check that the lines needing same value, do have same value.
                        this = self.get_hpn_from_col(col, gkey, header)
                        if this != previous[col]:
                            msg = f'Error: {this} != {previous[col]}'
                            if self.disable_err:
                                print(msg)
                            else:
                                raise ValueError(msg)
                        continue
                    if col == 'Ant':  # Make station-antenna, antenna-feed
                        ant = self.get_hpn_from_col('Ant', gkey, header)
                        if ant is not None:
                            sta = util.gen_hpn('station', int(ant[1:]))
                        else:
                            sta = None
                        feed = self.get_hpn_from_col('Feed', gkey, header)
                        previous['Ant'] = ant
                        previous['Feed'] = feed
                        # ... station-antenna
                        self._create_sheet_conn([[sta, 'A', 'ground'], [ant, 'H', 'ground']])
                        # ... antenna-feed
                        self._create_sheet_conn([[ant, 'H', 'focus'], [feed, 'A', 'input']])
                    elif col == 'Feed':  # Make feed-fem
                        feed = self.get_hpn_from_col('Feed', gkey, header)
                        fem = self.get_hpn_from_col('FEM', gkey, header)
                        self._create_sheet_conn([[feed, 'A', 'terminals'], [fem, 'A', 'input']])
                    elif col == 'FEM':  # Make fem-nbp
                        fem = self.get_hpn_from_col('FEM', gkey, header)
                        nbp = util.gen_hpn('NBP', node_num)
                        port = self._get_port(key=gkey, pol=pol, hdr_item='NBP/PAMloc', tab=tab)
                        self._create_sheet_conn([[fem, 'A', pol.lower()], [nbp, 'A', port]])
                    elif col == 'NBP/PAMloc':  # nbp-pam
                        nbp = util.gen_hpn('NBP', node_num)
                        port = self._get_port(key=gkey, pol=pol, hdr_item='NBP/PAMloc', tab=tab)
                        pam = self.get_hpn_from_col('PAM', gkey, header)
                        self._create_sheet_conn([[nbp, 'A', port], [pam, 'A', pol.lower()]])
                    elif col == 'PAM':  # pam-snap
                        pam = self.get_hpn_from_col('PAM', gkey, header)
                        snap = self.get_hpn_from_col('SNAP', gkey, header)
                        previous['SNAP'] = snap
                        port = self._get_port(key=gkey, pol='', hdr_item='Port', tab=tab)
                        if port[0] != pol[0].lower():
                            msg = "{} in {}: port ({}) and pol ({}) don't match".format(snap, node, port, pol)  # noqa
                            if self.disable_err:
                                print(msg)
                            else:
                                raise ValueError(msg)
                        self._create_sheet_conn([[pam, 'A', pol.lower()], [snap, 'A', port]])
                    elif col == 'SNAP':  # snap-node, pam-pch, pch-node
                        # ... snap-node
                        snap = self.get_hpn_from_col('SNAP', gkey, header)
                        loc = "loc{}".format(self.gsheet.data[gkey][header.index('SNAPloc')])
                        self._create_sheet_conn([[snap, 'A', 'rack'], [node, 'A', loc]])
                        # ... pam-pch
                        pam = self.get_hpn_from_col('PAM', gkey, header)
                        pch = self.gsheet.node_to_equip[node].pch
                        slot = '{}{}'.format('slot',
                                             self.gsheet.data[gkey][header.index('NBP/PAMloc')])
                        self._create_sheet_conn([[pam, 'A', 'slot'], [pch, 'A', slot]])

    def _create_sheet_conn(self, conn):
        if None in conn[0] or None in conn[1]:
            return
        keys = {'up': cm_utils.make_part_key(conn[0][0], conn[0][1]),
                'down': cm_utils.make_part_key(conn[1][0], conn[1][1])}
        port = {'up': conn[0][2].upper(), 'down': conn[1][2].upper()}
        for dir, key in keys.items():
            self.gsheet.connections[dir].setdefault(key, {})
            if port[dir] in self.gsheet.connections[dir][key]:
                continue
            self.gsheet.connections[dir][key][port[dir]] = CMPC.Connections()
            self.gsheet.connections[dir][key][port[dir]].connection(
                upstream_part=conn[0][0], up_part_rev=conn[0][1],
                upstream_output_port=conn[0][2],
                downstream_part=conn[1][0], down_part_rev=conn[1][1],
                downstream_input_port=conn[1][2])

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

    def compare_connections(self, direction='gsheet-active'):
        """
        Step through all of the sheet Connections and make sure they are all there and the same.
        """
        pside = 'up'
        self.compare_direction = direction
        self.missing = {}
        self.partial = {}
        self.different = {}
        self.different_stop = {}
        self.same = {}
        if direction.startswith('g'):
            A = self.gsheet.connections[pside]
            B = self.active.connections[pside]
        else:
            A = self.active.connections[pside]
            B = self.gsheet.connections[pside]
        for gkey, gpts in A.items():
            if gkey not in B.keys():
                self.missing[gkey] = gpts
                continue
            for p, c in gpts.items():
                if p not in B[gkey].keys():
                    self.partial.setdefault(gkey, {})
                    self.partial[gkey][p] = c
                elif B[gkey][p] == c:
                    self.same.setdefault(gkey, {})
                    self.same[gkey][p] = c
                else:
                    self.different.setdefault(gkey, {})
                    self.different[gkey][p] = c
                    self.different_stop.setdefault(gkey, {})
                    self.different_stop[gkey][p] = B[gkey][p]

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
        stopping = []
        for mss in self.missing:
            use_it = True
            for sk in skip:
                if mss.startswith(sk):
                    use_it = False
                    break
            if use_it:
                stopping.append(mss)
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
