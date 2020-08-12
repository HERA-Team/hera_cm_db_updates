# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
This class sets up to update the connections database.
"""
from hera_mc import cm_active, cm_utils, cm_sysdef
from hera_mc import cm_partconnect as CMPC
from . import util, cm_gsheet, upd_base
from argparse import Namespace

cm_req = Namespace(hpn=cm_sysdef.hera_zone_prefixes, pol='all',
                   at_date='now', exact_match=False, hookup_type=None)


class UpdateConnect(upd_base.Update):
    pols = ['E', 'N']
    NotFound = "Not Found"

    def __init__(self, script_nom='connupd', script_path='./', verbose=True):
        super(UpdateConnect, self).__init__(script_nom=script_nom, script_path=script_path,
                                            verbose=verbose)
        self.active = None

    def get_hpn_from_col(self, col, key, header):
        return util.gen_hpn(col, self.gsheet.data[key][header.index(col)])

    def load_active(self):
        """
        Gets the hookup data from the hera_mc database.
        """
        self.active = cm_active.ActiveData()
        self.active.load_connections()

    def make_sheet_connections(self):
        """
        Go through all of the sheet and make cm_partconnect.Connections for comparison.

        self.gsheet.connections is set up identically to self.active.connections
        """
        self.gsheet.connections = {'up': {}, 'down': {}}  # To mirror cm_active
        for sant in self.gsheet.ants:
            previous = {}
            for pol in self.pols:
                gkey = '{}-{}'.format(sant, pol)
                node_num = self.gsheet.data[gkey][0]
                tab = self.gsheet.ant_to_node[sant]
                header = self.gsheet.header[tab]
                for i, col in enumerate(header):
                    if col not in cm_gsheet.hu_col.keys():
                        continue
                    if self.gsheet.data[gkey][i] is None:
                        continue
                    if col in ['Ant', 'Feed', 'SNAP'] and pol == self.pols[1]:
                        this = self.get_hpn_from_col(col, gkey, header)
                        if this != previous[col]:
                            raise ValueError("{} != {}".format(this, previous[col]))
                        continue
                    if col == 'Ant':  # Make station-antenna, antenna-feed
                        ant = self.get_hpn_from_col('Ant', gkey, header)
                        previous['Ant'] = ant
                        sta = self._sta_from_ant(ant)
                        feed = self.get_hpn_from_col('Feed', gkey, header)
                        previous['Feed'] = feed
                        # ... station-antenna
                        keyup = cm_utils.make_part_key(sta, 'A')
                        pku = 'GROUND'
                        if self._status_OK(keyup, pol, [ant]):
                            self._ugconn(keyup, pku, [sta, 'A', 'ground'], [ant, 'H', 'ground'])
                        # ... antenna-feed
                        keyup = cm_utils.make_part_key(ant, 'H')
                        pku = 'FOCUS'
                        if self._status_OK(keyup, pol, [ant, feed]):
                            self._ugconn(keyup, pku, [ant, 'H', 'focus'], [feed, 'A', 'input'])
                    elif col == 'Feed':  # Make feed-fem
                        feed = self.get_hpn_from_col('Feed', gkey, header)
                        fem = self.get_hpn_from_col('FEM', gkey, header)
                        keyup = cm_utils.make_part_key(feed, 'A')
                        pku = 'TERMINALS'
                        if self._status_OK(keyup, pol, [feed, fem]):
                            self._ugconn(keyup, pku, [feed, 'A', 'terminals'], [fem, 'A', 'input'])
                    elif col == 'FEM':  # Make fem-nbp
                        fem = self.get_hpn_from_col('FEM', gkey, header)
                        nbp = util.gen_hpn('NBP', node_num)
                        port = '{}{}'.format(pol,
                                             self.gsheet.data[gkey][header.index('NBP/PAMloc')])
                        if port is not None:
                            port = port.lower()
                        keyup = cm_utils.make_part_key(fem, 'A')
                        if self._status_OK(keyup, pol, [fem, port]):
                            self._ugconn(keyup, pol, [fem, 'A', pol.lower()], [nbp, 'A', port])
                    elif col == 'NBP/PAMloc':  # nbp-pam
                        nbp = util.gen_hpn('NBP', node_num)
                        port = '{}{}'.format(pol,
                                             self.gsheet.data[gkey][header.index('NBP/PAMloc')])
                        if port is not None:
                            port = port.lower()
                            pku = port.upper()
                        pam = self.get_hpn_from_col('PAM', gkey, header)
                        if self._status_OK('-', pol, [port, pam]):
                            keyup = cm_utils.make_part_key(nbp, 'A')
                            self._ugconn(keyup, pku, [nbp, 'A', port], [pam, 'A', pol.lower()])
                    elif col == 'PAM':  # pam-snap
                        pam = self.get_hpn_from_col('PAM', gkey, header)
                        snap = self.get_hpn_from_col('SNAP', gkey, header)
                        previous['SNAP'] = snap
                        port = self.gsheet.data[gkey][header.index('Port')]
                        if len(port) == 0:
                            port = None
                        if port is not None:
                            port = port.lower()
                            if port[0] != pol[0].lower():
                                msg = "{} port ({}) and pol ({}) don't match".format(snap,
                                                                                     port, pol)
                                raise ValueError(msg)
                        keyup = cm_utils.make_part_key(pam, 'A')
                        if self._status_OK(keyup, pol, [pam, snap, port]):
                            self._ugconn(keyup, pol, [pam, 'A', pol.lower()], [snap, 'A', port])
                    elif col == 'SNAP':  # snap-node, pam-pch, pch-node
                        # ... snap-node
                        snap = self.get_hpn_from_col('SNAP', gkey, header)
                        node = util.gen_hpn("Node", node_num)
                        loc = "loc{}".format(self.gsheet.data[gkey][header.index('SNAPloc')])
                        if self._status_OK('-', pol, [snap, node, loc]):
                            keyup = cm_utils.make_part_key(snap, 'A')
                            pku = 'RACK'
                            self._ugconn(keyup, pku, [snap, 'A', 'rack'], [node, 'A', loc])
                        if self.active is None:
                            continue
                        # pam-pch
                        pam = self.get_hpn_from_col('PAM', gkey, header)
                        pku = 'SLOT'
                        try:
                            keyup = cm_utils.make_part_key(pam, 'A')
                            pch = self.active.connections['up'][keyup][pku].downstream_part
                        except KeyError:
                            continue
                        slot = '{}{}'.format('slot',
                                             self.gsheet.data[gkey][header.index('NBP/PAMloc')])
                        if self._status_OK('-', pol, [pam, pch, slot]):
                            self._ugconn(keyup, pku, [pam, 'A', 'slot'], [pch, 'A', slot])
                        # pch-node
                        node = util.gen_hpn("Node", node_num)
                        if self._status_OK('-', pol, [pch, slot, node]):
                            keyup = cm_utils.make_part_key(pch, 'A')
                            pku = 'RACK'
                            self._ugconn(keyup, pku, [pch, 'A', 'rack'], [node, 'A', 'bottom'])

    def _ugconn(self, k, p, up, dn):
        self.gsheet.connections['up'].setdefault(k, {})
        self.gsheet.connections['up'][k][p] = CMPC.Connections()
        self.gsheet.connections['up'][k][p].connection(
            upstream_part=up[0], up_part_rev=up[1], upstream_output_port=up[2],
            downstream_part=dn[0], down_part_rev=dn[1], downstream_input_port=dn[2])

    def _status_OK(self, keyup, pol, list_to_check):
        if None in list_to_check:
            print('skipping ', list_to_check)
            return False
        if keyup != '-':
            if pol == self.pols[1]:  # Make sure key already there
                if keyup not in self.gsheet.connections['up']:
                    raise ValueError("{} not present ({}).".format(keyup, pol))
            else:  # Make sure it is not there, then process
                if keyup in self.gsheet.connections['up']:
                    raise ValueError("{} already present ({}).".format(keyup, pol))
        return True

    def _sta_from_ant(self, ant):
        antnum = int(ant[1:])
        if antnum < 320:
            return 'HH{}'.format(antnum)
        else:
            raise ValueError("NEED TO ADD OUTRIGGERS")

    def compare_connections(self, direction='gsheet-active'):
        """
        Step through all of the sheet Connections and make sure they are all there and the same.
        """
        pside = 'up'
        d = Namespace(direction=direction, missing={}, partial={}, different={}, same={})
        if direction.startswith('g'):
            A = self.gsheet.connections[pside]
            B = self.active.connections[pside]
        else:
            A = self.active.connections[pside]
            B = self.gsheet.connections[pside]
        for gkey, gpts in A.items():
            if gkey not in B.keys():
                d.missing[gkey] = gpts
                continue
            for p, c in gpts.items():
                if p not in B[gkey].keys():
                    d.partial.setdefault(gkey, {})
                    d.partial[gkey][p] = c
                elif B[gkey][p] == c:
                    d.same.setdefault(gkey, {})
                    d.same[gkey][p] = c
                else:
                    d.different.setdefault(gkey, {})
                    d.different[gkey][p] = c
        return d

    def gen_compare_script(self):
        """
        Generate the compare script.
        """
        antkeys = cm_utils.put_keys_in_order(list(self.mismatches.connection.keys()),
                                             sort_order='NPR')
        added_parts = []
        for antkey in antkeys:
            key, pol = antkey.split('-')
            for diff in self.mismatches.connection[antkey]:
                self.update_counter += 1
                if diff[0] is None:
                    up, urev, uprt = diff[1].upstream_part, diff[1].up_part_rev,\
                                     diff[1].upstream_output_port
                    add_part = self.hera.get_general_part(up, urev)
                    if add_part is not None and up not in added_parts:
                        added_parts.append(up)
                        self.hera.update_part('add', add_part, cdate=self.cdate, ctime=self.ctime)
                    dn, drev, dprt = diff[1].downstream_part, diff[1].down_part_rev,\
                                     diff[1].downstream_input_port  # noqa
                    add_part = self.hera.get_general_part(dn, drev)
                    if add_part is not None and dn not in added_parts:
                        added_parts.append(dn)
                        self.hera.update_part('add', add_part, cdate=self.cdate, ctime=self.ctime)
                    self.hera.update_connection('add', [up, urev, uprt], [dn, drev, dprt],
                                                cdate=self.cdate, ctime=self.ctime)
                else:
                    s = "{:30s}   <--->   {}  ({}  {})".format(str(diff[0]), diff[1],
                                                               self.cdate, self.ctime)
                    self.hera.no_op_comment(s)

    def OUT_OF_DATE__get_val_from_cmdb(self, antkey, pol, sheet_col):
        """
        Bunch of ad hoc stuff to map the hookup_dict to the googlesheet column for comparison.
        """
        if sheet_col not in cm_gsheet.hu_col.keys():
            return None
        hu = self.hookup_dict[antkey]
        pol = pol.upper()
        for ppkey in hu.hookup.keys():
            if ppkey.upper().startswith(pol.upper()):
                break
        try:
            pam_slot = util.get_num(hu.hookup[ppkey][cm_gsheet.hu_col['Bulkhead-PAM_Slot']].downstream_input_port)  # noqa
        except IndexError:
            return self.NotFound
        try:
            snap_slot = str(int(util.get_num(hu.hookup[ppkey][cm_gsheet.hu_col['Node']].downstream_input_port)))  # noqa
        except IndexError:
            return self.NotFound
        i2c = (int(pam_slot) + 2) % 3 + 1

        if sheet_col.lower() == 'i2c_bus':
            return str(i2c)
        if sheet_col.lower() == 'node-pam_slot':
            return pam_slot
        if sheet_col.lower() == 'snap_slot':
            return snap_slot
        if sheet_col.lower() == 'port' or sheet_col.lower() == 'pol':
            try:
                return hu.hookup[ppkey][cm_gsheet.hu_col[sheet_col]].downstream_input_port.upper()
            except IndexError:
                return self.NotFound
        try:
            part = hu.hookup[ppkey][cm_gsheet.hu_col[sheet_col]].downstream_part
        except IndexError:
            return self.NotFound
        num = str(int(util.get_num(part)))

        if sheet_col.lower() == 'snap':
            return "{}{}".format(part[3], num)

        return num
