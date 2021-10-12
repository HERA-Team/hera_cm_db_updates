"""Class for config gsheet."""
import csv
import requests
from . import util
from hera_mc import cm_utils
from argparse import Namespace

apriori_enum_header = 'Current apriori enum'
hu_col = {'Ant': 0, 'Pol': 4, 'Feed': 1, 'FEM': 2, 'PAM': 4, 'NBP/PAMloc': 3,
          'SNAP': 5, 'Port': 5, 'SNAPloc': 6, 'Node': 6}
sheet_headers = ['Ant', 'Pol', 'Feed', 'FEM', 'NBP/PAMloc', 'PAM', 'SNAP', 'Port',
                 'SNAPloc', 'APriori', 'History', 'Comments']

gsheet = {}
gsheet['node0'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=0&single=true&output=csv"  # noqa
gsheet['node1'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=6391145&single=true&output=csv"  # noqa
gsheet['node2'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1387042544&single=true&output=csv"  # noqa
gsheet['node3'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1451443110&single=true&output=csv"  # noqa
gsheet['node4'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1237822868&single=true&output=csv"  # noqa
gsheet['node5'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1836116919&single=true&output=csv"  # noqa
gsheet['node6'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1913506139&single=true&output=csv" # noqa
gsheet['node7'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=780596546&single=true&output=csv"  # noqa
gsheet['node8'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1174361876&single=true&output=csv"  # noqa
gsheet['node9'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=59309582&single=true&output=csv"  # noqa
gsheet['node10'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=298497018&single=true&output=csv"  # noqa
gsheet['node11'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=660944848&single=true&output=csv"  # noqa
gsheet['node12'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1465370847&single=true&output=csv"  # noqa
gsheet['node13'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=954070149&single=true&output=csv"  # noqa
gsheet['node14'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1888985402&single=true&output=csv"  # noqa
gsheet['node15'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1947163734&single=true&output=csv"  # noqa
gsheet['node16'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1543199929&single=true&output=csv"  # noqa
# gsheet['node17'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=523815291&single=true&output=csv",  # noqa
gsheet['node18'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=2120802515&single=true&output=csv"  # noqa
gsheet['node19'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=488699377&single=true&output=csv"  # noqa
gsheet['node20'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=319083641&single=true&output=csv"  # noqa
no_prefix = ['Comments']

README = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1630961076&single=true&output=csv"  # noqa
WORKFLOW = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=2096134790&single=true&output=csv"  # noqa


class SheetData:
    """Class for googlesheet."""

    def __init__(self):
        """Initialize dictionaries/lists."""
        self.tabs = list(gsheet.keys())
        # It reads into the variables below
        self.data = {}
        self.ant_to_node = {}
        self.node_to_ant = {}
        self.header = {}
        self.date = {}
        self.notes = {}
        self.ants = []

    def load_workflow(self):
        """
        Load relevant data out of WORKFLOW tab.

        Currently, this is the apriori enums and emails.
        """
        xxx = requests.get(WORKFLOW)
        csv_tab = b''
        for line in xxx:
            csv_tab += line
        csv_data = csv_tab.decode('utf-8').splitlines()
        self.workflow = {}
        self.apriori_enum = []
        self.apriori_email = {}
        capture_enums = False
        for data in csv.reader(csv_data):
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

    def load_sheet(self, node_csv='none', tabs=None, check_headers=False,
                   path='', time_tag=True):
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
        time_tag : bool
            If True, time_tag the output files (if node_csv=w).
        """
        ant_set = set()
        node_csv = node_csv[0].lower()
        if tabs is None or str(tabs) == 'all':
            tabs = sorted(list(gsheet.keys()))
        elif isinstance(tabs, str):
            tabs = tabs.split(',')
        if node_csv == 'w' and time_tag:
            import time
            ttag = f"_{int(time.time())}"
            print(ttag)
        else:
            ttag = ""
        for tab in tabs:
            if node_csv == 'r':
                csv_data = []
                ofnc = f"{path}/{tab}.csv"
                with open(ofnc, 'r') as fp:
                    for line in fp:
                        csv_data.append(line)
            else:
                xxx = requests.get(gsheet[tab])
                csv_tab = b''
                for line in xxx:
                    csv_tab += line
                csv_data = csv_tab.decode('utf-8').splitlines()
            csv_tab = csv.reader(csv_data)
            if node_csv == 'w':
                ofnc = f"{path}/{tab}{ttag}.csv"
                with open(ofnc, 'w') as fp:
                    fp.write('\n'.join(csv_data))
            self.node_to_ant[tab] = []
            for data in csv_tab:
                if data[0].startswith('Ant'):  # This is the header line
                    self.header[tab] = ['Node'] + data
                    if check_headers:
                        util.compare_lists(sheet_headers, data, info=tab)
                    continue
                elif data[0].startswith('Date:'):  # This is the overall date line
                    self.date[tab] = data[1]
                    break
                try:
                    antnum = int(data[0])
                except ValueError:
                    continue
                hpn = util.gen_hpn('HH', antnum)
                hkey = cm_utils.make_part_key(hpn, 'A')
                ant_set.add(hkey)
                self.ant_to_node[hkey] = tab
                self.node_to_ant[tab].append(hpn)
                dkey = '{}-{}'.format(hkey, data[1].upper())
                self.data[dkey] = [util.get_num(tab)] + data
            # Get the notes below the hookup table.
            node_pn = 'N{:02d}'.format(int(util.get_num(tab)))
            for data in csv_tab:
                if data[0].startswith("Note"):
                    note_part = data[0].split()
                    if len(note_part) > 1:
                        npkey = note_part[1]
                    else:
                        npkey = node_pn
                    self.notes.setdefault(npkey, [])
                    self.notes[npkey].append('-'.join([y for y in data[1:] if len(y) > 0]))
        self.ants = cm_utils.put_keys_in_order(list(ant_set), sort_order='NPR')
