"""Class for config gsheet."""
import csv
import requests
from . import util
from argparse import Namespace
import os.path as ospath
from tabulate import tabulate
from copy import copy


apriori_enum_header = 'Current apriori enum'
hu_col = {'Ant': 0, 'Pol': 4, 'Feed': 1, 'FEM': 2, 'PAM': 4, 'NBP/PAMloc': 3,
          'SNAP': 5, 'Port': 5, 'SNAPloc': 6, 'Node': 6}
sheet_headers = ['Ant', 'Pol', 'Feed', 'FEM', 'NBP/PAMloc', 'PAM', 'SNAP', 'Port',
                 'SNAPloc', 'APriori', 'History', 'Comments']

gsheet_prefix = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?"  # noqa

gsheet = {}
gsheet['node0'] = "gid=0&single=true&output=csv"
gsheet['node1'] = "gid=6391145&single=true&output=csv"
gsheet['node2'] = "gid=1387042544&single=true&output=csv"
gsheet['node3'] = "gid=1451443110&single=true&output=csv"
gsheet['node4'] = "gid=1237822868&single=true&output=csv"
gsheet['node5'] = "gid=1836116919&single=true&output=csv"
gsheet['node6'] = "gid=1913506139&single=true&output=csv"
gsheet['node7'] = "gid=780596546&single=true&output=csv"
gsheet['node8'] = "gid=1174361876&single=true&output=csv"
gsheet['node9'] = "gid=59309582&single=true&output=csv"
gsheet['node10'] = "gid=298497018&single=true&output=csv"
gsheet['node11'] = "gid=660944848&single=true&output=csv"
gsheet['node12'] = "gid=1465370847&single=true&output=csv"
gsheet['node13'] = "gid=954070149&single=true&output=csv"
gsheet['node14'] = "gid=1888985402&single=true&output=csv"
gsheet['node15'] = "gid=1947163734&single=true&output=csv"
gsheet['node16'] = "gid=1543199929&single=true&output=csv"
gsheet['node17'] = "gid=523815291&single=true&output=csv"
gsheet['node18'] = "gid=2120802515&single=true&output=csv"
gsheet['node19'] = "gid=488699377&single=true&output=csv"
gsheet['node20'] = "gid=319083641&single=true&output=csv"
gsheet['node21'] = "gid=535819481&single=true&output=csv"
gsheet['node22'] = "gid=196866991&single=true&output=csv"
gsheet['node23'] = "gid=78305433&single=true&output=csv"
gsheet['node24'] = "gid=1348236988&single=true&output=csv"
gsheet['node25'] = "gid=2134158656&single=true&output=csv"
gsheet['node26'] = "gid=1376433001&single=true&output=csv"
gsheet['node27'] = "gid=1902916331&single=true&output=csv"
gsheet['node28'] = "gid=1379228027&single=true&output=csv"
gsheet['node29'] = "gid=1386400309&single=true&output=csv"
no_prefix = ['Comments']

gsheet['NodeNotes'] = "gid=906207981&single=true&output=csv"
gsheet['README'] = "gid=1630961076&single=true&output=csv"
gsheet['AprioriWorkflow'] = "gid=2096134790&single=true&output=csv"
gsheet['NCMs'] = "gid=1671631905&single=true&output=csv"


class SheetData:
    """Class for googlesheet."""

    def __init__(self):
        """Initialize dictionaries/lists."""
        self.tabs = []
        for key in gsheet.keys():
            gsheet[key] = gsheet_prefix + gsheet[key]
            if key.startswith('node'):
                self.tabs.append(key)
        self.tabs = sorted(self.tabs)
        # It reads into the variables below
        self.data = {}
        self.ant_to_node = {}
        self.node_to_ant = {}
        self.node_to_equip = {}
        self.header = {}
        self.date = {}
        self.notes = {}
        self.ants = []

    def load_workflow(self):
        """
        Load relevant data out of AprioriWorkflow tab.

        Currently, this is the apriori enums and emails.
        """
        self.workflow = {}
        self.apriori_enum = []
        self.apriori_email = {}
        csv_data = self.load_sheet_from_web('AprioriWorkflow')
        capture_enums = False
        for data in csv_data:
            self.workflow[data[0]] = data[1:]
            if data[0] == apriori_enum_header:
                capture_enums = True
                for _i, email_addr in enumerate(data[1:]):
                    if len(email_addr):
                        self.apriori_email[email_addr] = Namespace(eno=_i+1, notify=[])
            elif capture_enums and not len(data[0]):
                capture_enums = False
            if capture_enums:
                if data[0] != apriori_enum_header:
                    self.apriori_enum.append(data[0])
                    for notifyee, nent in self.apriori_email.items():
                        if data[nent.eno].lower() == 'y':
                            nent.notify.append(data[0])

    def load_node_notes(self):
        self.node_notes = self.load_sheet_from_web('NodeNotes')

    def csv_file(self, action, fn, data=None):
        if action == 'write' and data is not None:
            with open(fn, 'w') as fp:
                csvfw = csv.writer(fp, delimiter=',')
                csvfw.writerows(data)
            return
        elif action == 'read' and data is None:
            data = []
            with open(fn, 'r') as fp:
                csvfr = csv.reader(fp, delimiter=',')
                for row in csvfr:
                    data.append(row)
            return data
        else:
            print("Wrong csv arguments.")

    def load_sheet_from_web(self, key):
        sheet_info = []
        try:
            xxx = requests.get(gsheet[key])
        except Exception as e:
            print(f"Error reading {key}:  {gsheet[key]}:  {e}")
            return
        csv_tab = b''
        for line in xxx:
            csv_tab += line
        _info = csv_tab.decode('utf-8').splitlines()
        for nn in csv.reader(_info):
            sheet_info.append(nn)
        return sheet_info

    def load_ncm(self, ending_at='31'):
        self.ncm = {}
        ncmsheet = self.load_sheet_from_web('NCMs')
        indata = False
        for row in ncmsheet:
            if not indata and row[0] == 'NCM':
                indata = True
            elif indata:
                if row[1] == ending_at:
                    break
                if row[0].startswith('Pre'):
                    ncm = f"NCMP{int(row[1]):d}"
                else:
                    ncm = f"NCM{int(row[1]):02d}"
                if row[5].startswith('A'):
                    wrsn = f"WR{row[5]}"
                else:
                    wrsn = row[5]
                try:
                    r11 = int(row[11])
                    rdsn = f"arduino{r11}"
                    rdhpn = f"RD{r11:02d}"
                except ValueError:
                    rdsn = ''
                    rdhpn = ''
                self.ncm[ncm] = Namespace(
                                          wr=wrsn,
                                          wrmac=row[7],
                                          rd=rdsn,
                                          rdmac=row[13],
                                          rdhpn=rdhpn,
                                          notes=row[-1]
                )

    def check_found_antennas(self):
        chkfa = set(self.found_antennas)
        cntfa = {}
        for ant in chkfa:
            cntfa[ant] = 0
            for cha in self.found_antennas:
                if cha == ant:
                    cntfa[ant] += 1
        for ant, cnt in cntfa.items():
            if cnt != 2:
                print(f"Ant {ant} has {cnt} entries.")

    def load_sheet(self, node_csv='none', tabs=None, check_headers=False, path='.'):
        """
        Get the googlesheet information from the internet (or locally for testing etc).

        Parameters
        ----------
        node_csv : str
            node csv file status:  one of 'read', 'write', 'none' (only need first letter)
            'read' uses a local version as opposed to internet version
            'write' writes a local version
            'none' does neither of the above
        tabs : none, str, list
            List of tabs to use.  None == all of them.
        check_headers : bool
            If True, it will make sure all of the headers agree with sheet_headers
        path : str
            Path to use if reading/writing csv files.
        """
        from hera_mc import cm_utils
        ant_set = set()
        node_csv = node_csv[0].lower()
        if tabs is None or str(tabs) == 'all':
            tabs = self.tabs
        elif isinstance(tabs, str):
            tabs = tabs.split(',')
        missing_ant = 9999
        self.found_antennas = []
        for tab in tabs:
            if node_csv == 'r':
                csv_data = self.csv_file('read', ospath.join(path, f"{tab}.csv"))
            else:
                csv_data = self.load_sheet_from_web(tab)
            if node_csv == 'w':
                self.csv_file('write', ospath.join(path, f"{tab}.csv"), csv_data)
            self.node_to_ant[tab] = []
            header_found = False
            for data in csv_data:
                if data[0].startswith('Ant'):  # This is the header line
                    header_found = True
                    self.header[tab] = ['Node'] + data
                    if check_headers:
                        util.compare_lists(sheet_headers, data, info=tab)
                    continue
                elif data[0].startswith('#END'):
                    break
                try:
                    antnum = int(data[0])
                except ValueError:
                    if data[1].upper() == 'E':
                        missing_ant += 1
                    antnum = missing_ant
                self.found_antennas.append(antnum)
                hpn = util.gen_hpn('station', antnum)
                if antnum > 350:
                    print(f"antenna>350:  {tab} {antnum}")
                hkey = cm_utils.make_part_key(hpn, 'A')
                ant_set.add(hkey)
                self.ant_to_node[hkey] = tab
                self.node_to_ant[tab].append(hpn)
                dkey = '{}-{}'.format(hkey, data[1].upper())
                self.data[dkey] = [util.get_num(tab)] + data
            if not header_found:
                print(f"WARNING: Header was not located for {tab}")
            # Get the notes below the hookup table.
            node_pn = 'N{:02d}'.format(int(util.get_num(tab)))
            self.node_to_equip[node_pn] = Namespace()
            for data in csv_data:
                key = data[0].strip().lower()
                if key.startswith("note"):
                    note_part = data[0].split()
                    if len(note_part) > 1:
                        npkey = note_part[1]
                    else:
                        npkey = node_pn
                    self.notes.setdefault(npkey, [])
                    self.notes[npkey].append('-'.join([y for y in data[1:] if len(y) > 0]))
                elif key in ['ncm', 'fps', 'pch', 'wrs']:
                    if not len(data[1]):
                        val = ''
                    else:
                        try:
                            val = f"{key.upper()}{int(data[1]):02d}"
                        except ValueError:
                            val = f"{key.upper()}{data[1].upper()}"
                    setattr(self.node_to_equip[node_pn], key, val)
        ants_full = cm_utils.put_keys_in_order(list(ant_set), sort_order='NPR')
        self.ants = []
        self.other = []
        for aa in ants_full:
            if len(aa) == 9:
                self.other.append(aa)
            else:
                self.ants.append(aa)

class ArchiveGsheet:
    allowed_to_find = {'ant': 'Ant', 'feed': 'Feed', 'fem': 'FEM', 'nbp/pamloc': 'NBP/PAMloc', 'nbp': 'NBP/PAMloc', 'pamloc': 'NBP/PAMloc',
                       'pam': 'PAM', 'snap': 'SNAP', 'ncm': 'Ant:NCM', 'fps': 'Ant:FPS', 'PCH': 'Ant:PCH'}
    def __init__(self, base_path=None):
        import pandas
        from hera_mc.mc import get_cm_csv_path
        self.cm_path = get_cm_csv_path()
        if base_path is None:
            self.base_path = ospath.join(self.cm_path, 'cm_updates/gsheet')
        else:
            self.base_path = base_path
        self.node = {}
        for node in range(24):
            self.node[node] = pandas.read_csv(ospath.join(self.base_path, f"node{node}.csv"))

    def find(self, **kwargs):
        per_ant_hdr = ['Node', 'Ant', 'Pol', 'Feed', 'FEM', 'NBP/PAMloc', 'PAM', 'SNAP', 'Port', 'SNAPloc', 'APriori', 'row']
        per_ant_rows = []
        per_node_hdr = ['Node', 'Part Name', 'Part Number', 'row']
        per_node_rows = []
        for pname, tmp_pval in kwargs.items():
            if pname.lower() not in self.allowed_to_find:
                print(f"Skipping {pname.lower()}")
                continue
            loc = self.allowed_to_find[pname.lower()]
            col = loc.split(':')[0]
            rowloc = loc.split(':')[1] if ':' in loc else None
            try:
                pval = int(tmp_pval)
            except ValueError:
                pval = tmp_pval
            for this_node, these_conn in self.node.items():
                if rowloc is None:  # this is a per_ant part
                    for i, data in enumerate(these_conn[col]):
                        try:
                            cdat = int(data)
                        except ValueError:
                            cdat = data
                        if cdat == pval:
                            this_row = [this_node]
                            for cval in per_ant_hdr[1:-1]:
                                _xx = these_conn[cval][i]
                                try:
                                    use_xx = int(_xx)
                                except ValueError:
                                    use_xx = _xx
                                this_row.append(use_xx)
                            this_row.append(i)
                            per_ant_rows.append(this_row)
                else:  # this is a per_node part
                    for i, data in enumerate(these_conn[col]):
                        if data == rowloc:
                            try:
                                check_val = int(these_conn['Pol'][i])
                            except ValueError:
                                check_val = -99
                            if pval == check_val:
                                per_node_rows.append([this_node, rowloc, these_conn['Pol'][i], i])
        # Warning for now
        print("Not working as expected for multiple name/value pairs...")
        print(kwargs)
        print()
        show_blame = []
        if len(per_ant_rows):
            print(tabulate(per_ant_rows, headers=per_ant_hdr))
            show_blame = per_ant_rows
        elif len(per_node_rows):
            print(tabulate(per_node_rows, headers=per_node_hdr))
            show_blame = per_node_rows
        # These are used for blame.
        self.column_indices = {}
        for pname, pval in kwargs.items():
            self.column_indices[self.node[0].columns.get_loc(self.allowed_to_find[pname])] = pval
        self.track_blame = {}
        for row in show_blame:
            self.track_blame.setdefault(row[0], [])
            self.track_blame[row[0]].append(row[-1])

    def blame(self):
        print("Running blame_gitpython with default search_past")
        self.blame_gitpython()

    def blame_gitpython(self, search_past=100):
        from git import Repo
        # Get all data into blame_data dict and capture antennas with matching component info
        repo = Repo(self.cm_path)
        self.blame_data = {}
        for node in self.track_blame:
            fn = ospath.join(self.base_path, f"node{node}.csv")
            with open(fn, 'r') as fpr:
                reader = csv.reader(fpr)
                self.blame_data[fn] = {'header': next(reader), 'ants': set(), 'commits': set()}
            for val in repo.iter_commits('main', max_count=search_past):
                for commit, lines in repo.blame(val, fn):
                    hexsha = commit.hexsha[:8]
                    self.blame_data[fn]['commits'].add(hexsha)
                    self.blame_data[fn].setdefault(hexsha, {'commit': copy(commit), 'data': set()})
                    for data in lines:
                        self.blame_data[fn][hexsha]['data'].add(copy(data))
                        for row in csv.reader([data]):
                            for col2chk, val2match in self.column_indices.items():
                                if row[col2chk] == val2match:
                                    self.blame_data[fn]['ants'].add(row[0])
        # Go through blame_data for matching antennas and key on datetime|row
        datetime_blame = {}
        for this_fn in self. blame_data:
            datetime_blame[this_fn] = {}
            for this_commit in self.blame_data[this_fn]['commits']:
                for this_ant in self.blame_data[this_fn]['ants']:
                    for data in self.blame_data[this_fn][this_commit]['data']:
                        for row in csv.reader([data]):
                            try:
                                trial_ant = row[0]
                            except IndexError:
                                continue
                            if trial_ant == this_ant:
                                dt = self.blame_data[this_fn][this_commit]['commit'].committed_datetime.strftime('%Y-%m-%d %H:%M')
                                key = f"{dt}|{data}"
                                datetime_blame[this_fn][key] = this_commit
        # Print out sorted results
        for this_fn in datetime_blame:
            print(f"\n---{this_fn}")
            previous_dt = '-'
            for key in sorted(datetime_blame[this_fn]):
                dt, data = key.split('|')
                if dt != previous_dt:
                    print()
                    previous_dt = copy(dt)
                print(f"  {dt}  {data}")


    def blame_commandline(self):
        import subprocess
        for node, lines in self.track_blame.items():
            fn = ospath.join(self.base_path, f"node{node}.csv")
            print(f"\n---{fn}")
            rows = ','.join([str(x+2) for x in lines])
            process = subprocess.run(['git', 'blame', '-L', rows, fn])
            if process.stdout is not None:
                print(process.stdout)
            else:
                print()
                