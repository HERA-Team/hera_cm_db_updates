# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.
"""
This class sets up to update the part information database.
"""
from hera_mc import mc, cm_utils, cm_active
from . import util, upd_base, cm_gsheet
import os.path
import json


def _dict2msg(data):
    msg = f"-------------{data['ant']}: {data['cdate']}  {data['ctime']}\n"
    msg += f"\t{data['old_status']} --> {data['new_status']}\n"
    for info in data['info']:
        msg += f"\t{info}\n"
    msg += '\n'
    return msg


class UpdateInfo(upd_base.Update):
    """Generates the script to update comments and "apriori" info from the configuration gsheet."""

    def __init__(self, script_type='infoupd', script_path='default', verbose=True):
        """Init of base."""
        super(UpdateInfo, self).__init__(script_type=script_type,
                                         script_path=script_path,
                                         verbose=verbose)
        self.new_apriori = {}
        self.apriori_notify_file = os.path.join(self.script_path, 'apriori_notify.txt')

    def load_active(self):
        """Load active data."""
        db = mc.connect_to_mc_db(None)
        with db.sessionmaker() as session:
            self.active = cm_active.ActiveData(session=session)
            self.active.load_info()
            self.active.load_apriori()

    def load_gnodes(self):
        """Load node notes tab of googlesheet."""
        if self.gsheet is None:
            self.gsheet = cm_gsheet.SheetData()
        lnn = {}
        self.gsheet.load_node_notes()
        for line in self.gsheet.node_notes:
            try:
                node_n = f"N{int(line[0]):02d}"
            except ValueError:
                continue
            lnn.setdefault(node_n, [])
            for entry in line[1:]:
                if len(entry):
                    lnn[node_n].append(entry)
        self.node_notes = {}
        for key, val in lnn.items():
            if len(val):
                self.node_notes[key] = val

    def process_apriori_notification(self, notify_type='new'):
        """
        Processes the log apriori updates and send email digest.

        Parameters
        ----------
        notify_type : str
            one of 'either', 'old', 'new':  notify if status in old, new, either
        """
        from hera_mc import watch_dog

        anotify = self.handle_apriori_notification_file('read')
        if not len(anotify):
            return
        self.handle_apriori_notification_file('delete')
        self.load_gworkflow()
        from_addr = 'hera@lists.berkeley.edu'
        msg_header = 'Apriori system changes.\n------------------------------\n'
        for email, n in self.gsheet.apriori_email.items():
            msg = "{}".format(msg_header)
            used_antdt = []
            for antdt, data in anotify.items():
                if notify_type == 'old':
                    using = [data['old_status']]
                elif notify_type == 'new':
                    using = [data['new_status']]
                else:
                    using = [data['old_status'], data['new_status']]
                for this_status in n.notify:
                    if this_status in using and antdt not in used_antdt:
                        msg += _dict2msg(data)
                        used_antdt.append(antdt)
            if msg != msg_header:
                to_addr = [email]
                watch_dog.send_email(msg_header.splitlines()[0], msg, to_addr,
                                     from_addr, skip_send=False)

    def handle_apriori_notification_file(self, action='delete'):
        """
        Parameter
        ---------
        action : str, dict
            If str, can be read or delete.  If dict, it writes file.
        """
        from os import remove

        if isinstance(action, dict):
            with open(self.apriori_notify_file, 'w') as fp:
                json.dump(action, fp, indent=4)
        elif isinstance(action, str):
            if action == 'read':
                if os.path.isfile(self.apriori_notify_file):
                    with open(self.apriori_notify_file, 'r') as fp:
                        return json.load(fp)
                else:
                    return {}
            elif action == 'delete':
                if os.path.isfile(self.apriori_notify_file):
                    remove(self.apriori_notify_file)

    def log_apriori_notifications(self):
        """
        Log the found apriori updates to a file with update_info script.

        Gets processed and distributed per "process_apriori_notification".
        """
        if not len(self.new_apriori):
            return
        full_notify = self.handle_apriori_notification_file('read')
        for k, v in self.new_apriori.items():
            new_key = f"{v['ant']}|{v['cdate']}|{v['ctime']}"
            full_notify[new_key] = v
        self.handle_apriori_notification_file(full_notify)

    def add_apriori(self):
        """Write out for apriori differences."""
        status_enum = cm_active.partconn.get_apriori_antenna_status_enum()
        self.new_apriori = {}
        rev = 'A'
        stmt_hdr = "apriori_antenna status change:"
        refout = 'apa-infoupd'
        for key in self.gsheet.ants:
            ap_col = self.gsheet.header[self.gsheet.ant_to_node[key]].index('APriori')
            E = self.gsheet.data[key + '-E'][ap_col]
            N = self.gsheet.data[key + '-N'][ap_col]
            if not len(E) and not len(N):
                continue
            ant, rev = cm_utils.split_part_key(key)
            warn_msg = ''
            if E != N:
                if len(E) and len(N):
                    usestat = status_enum[min(status_enum.index(E), status_enum.index(N))]
                else:
                    usestat = N if not len(E) else E
                warn_msg = (f"Warning.  {key}:  {E} and {N} should be the same.  Using {usestat}")
                print(warn_msg)
            else:
                usestat = E
            try:
                arcstat = self.active.apriori[key].status
            except KeyError:
                print(f"{key} No existing apriori status.")
                arcstat = 'None'
            if usestat != arcstat:
                self.new_apriori[key] = {'ant': ant}
                self.new_apriori[key]['old_status'] = arcstat
                self.new_apriori[key]['new_status'] = usestat
                self.new_apriori[key]['cdate'], self.new_apriori[key]['ctime'] = util.YMD_HM(self.cdatetime, 100)  # noqa
                if len(warn_msg):
                    self.new_apriori[key]['warning'] = warn_msg
                s = f"{arcstat} > {usestat}"
                if self.verbose:
                    print(f"Updating {ant}:  {s}")
                self.hera.update_apriori(ant, usestat, self.new_apriori[key]['cdate'],
                                         self.new_apriori[key]['ctime'])
                self.hera.add_part_info(ant, rev, f"{stmt_hdr} {s}",
                                        self.new_apriori[key]['cdate'],
                                        self.new_apriori[key]['ctime'], ref=refout)
                self.update_counter += 1

    def add_gnodes(self, rev='A', duplication_window=90.0, view_duplicate=0.0):
        primary_keys = []
        for node, notes in self.node_notes.items():
            ndkey = cm_utils.make_part_key(node, rev)
            pdate = self.cdate + ''
            ptime = self.ctime + ''
            for this_note in notes:
                if not self.is_duplicate(ndkey, this_note, duplication_window, view_duplicate):
                    pkey, pdate, ptime = util.get_unique_pkey(node, rev, pdate, ptime, primary_keys)
                    refout = 'infoupd'
                    self.new_notes.setdefault(ndkey, [])
                    self.new_notes[ndkey].append(this_note)
                    if self.verbose:
                        print("Adding comment: {}:{} - {}".format(node, rev, this_note))
                    self.hera.add_part_info(node, rev, this_note, pdate, ptime, ref=refout)
                    self.update_counter += 1
                    primary_keys.append(pkey)

    def add_sheet_notes(self, duplication_window=90.0, view_duplicate=0.0):
        """
        Search the relevant fields in the googlesheets and generate add note commands.

        Parameters
        ----------
        duplication_window : float
            time-frame in days over which to check for duplicate comments.
        """
        primary_keys = []
        self.new_notes = {}
        for sheet_key in self.gsheet.data.keys():
            antrev_key, pol = sheet_key.split('-')
            ant, rev = cm_utils.split_part_key(antrev_key)
            tab = self.gsheet.ant_to_node[antrev_key]
            # Process sheet data
            pdate = self.cdate + ''
            ptime = self.ctime + ''
            for i, col in enumerate(self.gsheet.header[tab]):
                if col in cm_gsheet.hu_col.keys() or not len(col) or col == 'APriori':
                    continue
                try:
                    col_data = self.gsheet.data[sheet_key][i]
                except IndexError:
                    continue
                if len(col_data) == 0:
                    continue
                pkey, pdate, ptime = util.get_unique_pkey(ant, rev, pdate, ptime, primary_keys)
                # ##Get prefix for entry
                if col in cm_gsheet.no_prefix:
                    prefix = ''
                else:
                    prefix = '{}: '.format(col)
                statement = '{}{}'.format(prefix, col_data)
                if "'" in statement:
                    statement = statement.replace("'", "")
                statement = statement.strip()
                if len(statement) == 0:
                    continue
                if not self.is_duplicate(antrev_key, statement, duplication_window, view_duplicate):
                    refout = 'infoupd'
                    if antrev_key in self.new_apriori.keys():
                        refout = 'apa-infoupd'
                        if statement not in self.new_apriori[antrev_key]['info']:
                            self.new_apriori[antrev_key]['info'].append(statement)
                    self.new_notes.setdefault(antrev_key, [])
                    self.new_notes[antrev_key].append(statement)
                    if self.verbose:
                        print("Adding comment: {}:{} - {}".format(ant, rev, statement))
                    self.hera.add_part_info(ant, rev, statement, pdate, ptime, ref=refout)
                    self.update_counter += 1
                    primary_keys.append(pkey)

    def is_duplicate(self, key, statement, duplication_window, view_duplicate=0.0):
        """Check if duplicate."""
        if key in self.active.info.keys():
            for note in self.active.info[key]:
                note_time = cm_utils.get_astropytime(note.posting_gpstime, float_format='gps').datetime  # noqa
                dt = self.now - note_time
                ddays = dt.days + dt.seconds / (3600.0 * 24)
                if ddays < duplication_window and statement == note.comment:
                    if key.startswith('N'):
                        node = key
                    else:
                        node = self.gsheet.ant_to_node[key]
                    if self.verbose and ddays > view_duplicate:
                        print("Duplicate for {:8s}  ({}) - {}  ({:.1f} days)"
                              .format(key, node, statement, ddays))
                    return True
        return False

    def view_info(self):
        """View it."""
        if len(self.new_apriori.keys()):
            print("New Apriori")
            for x, info in sorted(self.new_apriori.items()):
                print("{}:  {}".format(x, info))
        else:
            print("No new apriori")
        if len(self.new_notes.keys()):
            print("New Notes")
            for x, info in sorted(self.new_notes.items()):
                print("{}:  {}".format(x, info))
        else:
            print("No new notes")
