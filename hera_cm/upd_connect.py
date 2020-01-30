# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
"""
from hera_mc import cm_hookup, cm_utils, cm_sysdef, cm_partconnect
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
        self.mismatches = Namespace(hookup={}, connection={})

    def get_hpn_from_col(self, col, key, header):
        return util.gen_hpn(col, self.gsheet.data[key][header.index(col)])

    def load_hookup(self):
        """
        Gets the hookup data from the hera_mc database.
        """
        self.hookup = cm_hookup.Hookup()
        self.hookup_dict = self.hookup.get_hookup(hpn=cm_req.hpn, pol=cm_req.pol,
                                                  at_date=cm_req.at_date,
                                                  exact_match=cm_req.exact_match,
                                                  hookup_type=cm_req.hookup_type)

    def make_sheet_connections(self):
        """
        Go through all of the sheet and make cm_partconnect.Connections for comparison
        """
        self.gsheet.connection = {}
        for sant in self.gsheet.ants:
            for pol in self.pols:
                key = '{}-{}'.format(sant, pol)
                node_num = self.gsheet.data[key][0]
                tab = self.gsheet.ant_to_tab[sant]
                header = self.gsheet.header[tab] + ['get_PAM_loc']
                self.gsheet.connection[key] = []
                for i, col in enumerate(header):
                    if col not in self.gsheet.hu_col.keys():
                        continue
                    if self.gsheet.data[key][i] is not None:
                        tc_ = cm_partconnect.Connections()
                        if col == 'Ant':
                            ant = self.get_hpn_from_col('Ant', key, header)
                            feed = self.get_hpn_from_col('Feed', key, header)
                            tc_.connection(upstream_part=ant, up_part_rev='H',
                                           upstream_output_port='focus',
                                           downstream_part=feed, down_part_rev='A',
                                           downstream_input_port='input')
                        elif col == 'Feed':
                            feed = self.get_hpn_from_col('Feed', key, header)
                            fem = self.get_hpn_from_col('FEM', key, header)
                            tc_.connection(upstream_part=feed, up_part_rev='A',
                                           upstream_output_port='terminals',
                                           downstream_part=fem, down_part_rev='A',
                                           downstream_input_port='input')
                        elif col == 'FEM':
                            fem = self.get_hpn_from_col('FEM', key, header)
                            nbp = util.gen_hpn('NBP', node_num)
                            port = '{}{}'.format(pol, self.gsheet.data[key][header.index('Node/PAMloc')])  # noqa
                            if port is not None:
                                port = port.lower()
                            tc_.connection(upstream_part=fem, up_part_rev='A',
                                           upstream_output_port=pol.lower(),
                                           downstream_part=nbp, down_part_rev='A',
                                           downstream_input_port=port)
                        elif col == 'Node/PAMloc':
                            nbp = util.gen_hpn('NBP', node_num)
                            port = '{}{}'.format(pol, self.gsheet.data[key][header.index('Node/PAMloc')])  # noqa
                            if port is not None:
                                port = port.lower()
                            pam = self.get_hpn_from_col('PAM', key, header)
                            tc_.connection(upstream_part=nbp, up_part_rev='A',
                                           upstream_output_port=port,
                                           downstream_part=pam, down_part_rev='A',
                                           downstream_input_port=pol.lower())
                        elif col == 'PAM':
                            pam = self.get_hpn_from_col('PAM', key, header)
                            snap = self.get_hpn_from_col('SNAP', key, header)
                            port = self.gsheet.data[key][header.index('Port')]
                            if len(port) == 0:
                                port = None
                            if port is not None:
                                port = port.lower()
                                if port[0] != pol[0].lower():
                                    msg = "{} port ({}) and pol ({}) don't match".format(snap,
                                                                                         port, pol)
                                    print(msg)
                            tc_.connection(upstream_part=pam, up_part_rev='A',
                                           upstream_output_port=pol.lower(),
                                           downstream_part=snap, down_part_rev='A',
                                           downstream_input_port=port)
                        elif col == 'get_PAM_slot':  # extra to get @slot
                            pam = self.get_hpn_from_col('PAM', key, header)
                            try:
                                pamkey = cm_utils.make_part_key(pam, 'A')
                                pch = self.hookup.active.connections['up'][pamkey]['@SLOT'].downstream_part  # noqa
                            except KeyError:
                                print("{} is not an active connection!  No pam from {}"
                                      .format(pam, key))
                                pch = None
                            slot = '{}{}'.format('@SLOT', self.gsheet.data[key][header.index('Bulkhead-PAM_Slot')])  # noqa
                            if slot is not None:
                                slot = slot.lower()
                            tc_.connection(upstream_part=pam, up_part_rev='A',
                                           upstream_output_port='@slot',
                                           downstream_part=pch, down_part_rev='A',
                                           downstream_input_port=slot)
                        elif col == 'SNAP':
                            snap = self.get_hpn_from_col('SNAP', key, header)
                            node = util.gen_hpn("Node", node_num)
                            loc = "loc{}".format(self.gsheet.data[key][header.index('SNAP_Slot')])
                            tc_.connection(upstream_part=snap, up_part_rev='A',
                                           upstream_output_port='rack',
                                           downstream_part=node, down_part_rev='A',
                                           downstream_input_port=loc)
                        elif col == 'SNAPloc':  # extra to get @slot
                            pam = self.get_hpn_from_col('PAM', key, header)
                            try:
                                pamkey = cm_utils.make_part_key(pam, 'A')
                                pch = self.hookup.active.connections['up'][pamkey]['@SLOT'].downstream_part  # noqa
                            except KeyError:
                                print("{} is not an active connection!  No pam from {}"
                                      .format(pam, key))
                                pch = None
                            slot = '{}{}'.format('@SLOT', self.gsheet.data[key][header.index('Bulkhead-PAM_Slot')])  # noqa
                            if slot is not None:
                                slot = slot.lower()
                            tc_.connection(upstream_part=pam, up_part_rev='A',
                                           upstream_output_port='@slot',
                                           downstream_part=pch, down_part_rev='A',
                                           downstream_input_port=slot)

                        if tc_.upstream_part is None or tc_.up_part_rev is None or\
                           tc_.upstream_output_port is None or tc_.downstream_part is None or\
                           tc_.down_part_rev is None or tc_.downstream_input_port is None:
                            continue
                        self.gsheet.connection[key].append(tc_)

    def compare_connection(self):
        """
        Step through all of the sheet Connections and make sure they are all there and the same.
        """
        for sckey, scvals in self.gsheet.connection.items():
            for scval in scvals:
                ackey = cm_utils.make_part_key(scval.downstream_part, scval.down_part_rev)
                acport = scval.downstream_input_port.upper()
                try:
                    acval = self.hookup.active.connections['down'][ackey][acport]
                except KeyError:
                    acval = None
                if acval is None or acval != scval:
                    self.mismatches.connection.setdefault(sckey, {'sheet': scvals, 'diff': []})
                    self.mismatches.connection[sckey]['diff'].append([acval, scval])

    def compare_hookup(self):
        """
        ## Note that this is left in for sanity/double-checking purposes.
        Compares the hookup data with the spreadsheet.  Writes self.mismatches.hookup
        keyed on 'ant:rev-pol' then 'sheet' and 'diff
        e.g. self.mismatches.hookup['HH30:A-E']['diff']
             self.mismatches.hookup['HH30:A-N']['sheet']
        """
        for antkey in self.gsheet.ants:
            for pol in self.pols:
                sheet_key = "{}-{}".format(antkey, pol)
                tab = 'node{}'.format(self.gsheet.data[sheet_key][0])
                header = self.gsheet.header[tab]
                sheet_row = util.get_row_dict(header, self.gsheet.data[sheet_key])
                for i, col in enumerate(header):
                    val = self._get_val_from_cmdb(antkey, pol, col)
                    if val is not None:
                        sheet_val = self.gsheet.data[sheet_key][i]
                        if val.upper() != sheet_val.upper():
                            if val != self.NotFound or len(sheet_val.strip()):
                                self.mismatches.hookup.setdefault(sheet_key, {'sheet': sheet_row, 'diff': []})  # noqa
                                self.mismatches.hookup[sheet_key]['diff'].append([col, val, sheet_val])  # noqa

    def view_compare(self, ctypes=['hookup', 'connection']):
        """
        Views the comparison with cm database and spreadsheet.

        Parameters
        ----------
        ctypes : list, str
            List of strings for compare type:  connection/hookup

        Returns
        -------
        str
            output string
        """
        if isinstance(ctypes, str):
            ctypes = [ctypes]
        antkeys = []
        for ctype in ctypes:
            comp_type = getattr(self.mismatches, ctype)
            antkeys += list(comp_type.keys())
        antkeys = cm_utils.put_keys_in_order(list(set(antkeys)), sort_order='NPR')
        output_string = ''
        for antkey in antkeys:
            key, pol = antkey.split('-')
            output_string += "\n{:10s}----------    cm       <--->  sheet\n".format(antkey)
            for ctype in ctypes:
                comp_type = getattr(self.mismatches, ctype)
                if antkey in comp_type.keys():
                    for diff in comp_type[antkey]['diff']:
                        if ctype == 'hookup':
                            output_string += "{:18s}  {:10s}   <--->"
                            "   {}\n".format(diff[0], diff[1], diff[2])
                        else:
                            output_string += "{:30s}   <--->   {}  "
                            "({}  {})\n".format(str(diff[0]), diff[1], self.cdate, self.ctime)
        print(output_string)

    def gen_compare_script(self):
        """
        Generate the compare script.
        """
        antkeys = cm_utils.put_keys_in_order(list(self.mismatches.connection.keys()),
                                             sort_order='NPR')
        added_parts = []
        for antkey in antkeys:
            key, pol = antkey.split('-')
            for diff in self.mismatches.connection[antkey]['diff']:
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

    def _get_val_from_cmdb(self, antkey, pol, sheet_col):
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
