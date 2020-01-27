"""
x.hookup_dict['HH104:A'].hookup['e']

0 <HH104:A<ground|ground>A104:H>
1 <A104:H<focus|input>FDV10:A>
2 <FDV10:A<terminals|input>FEM061:A>
3 <FEM061:A<e|e5>NBP08:A>
4 <NBP08:A<e5|e>PAM014:A>
5 <PAM014:A<e|e6>SNPC000044:A>
6 <SNPC000044:A<rack|loc1>N08:A>
"""
import csv
import requests
from . import util
from hera_mc import cm_utils

hu_col = {'Ant': 0, 'Pol': 4, 'Feed': 1, 'FEM': 2, 'PAM': 4, 'NBP/PAM-loc': 3,
          'SNAP': 5, 'Port': 5, 'SNAP-loc': 6, 'Node': 6}
sheet_headers = ['Ant', 'Pol', 'Feed', 'FEM', 'NBP/PAM-loc', 'PAM', 'SNAP', 'Port', 'SNAP-loc',
                 'APriori', 'History', 'Comments']

gsheet = {}
gsheet['node0'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=0&single=true&output=csv"  # noqa
gsheet['node3'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1451443110&single=true&output=csv"  # noqa
gsheet['node4'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1237822868&single=true&output=csv"  # noqa
gsheet['node5'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1836116919&single=true&output=csv"  # noqa
gsheet['node7'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=780596546&single=true&output=csv"  # noqa
gsheet['node8'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1174361876&single=true&output=csv"  # noqa
gsheet['node9'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=59309582&single=true&output=csv"  # noqa
gsheet['node10'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=298497018&single=true&output=csv"  # noqa
gsheet['node12'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1465370847&single=true&output=csv"  # noqa
gsheet['node13'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=954070149&single=true&output=csv"  # noqa
gsheet['node14'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1888985402&single=true&output=csv"  # noqa
gsheet['node15'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1947163734&single=true&output=csv"  # noqa
no_prefix = ['Comments']


class SheetData:
    def __init__(self):
        self.data = {}
        self.ant_to_tab = {}
        self.header = {}
        self.date = {}
        self.notes = {}
        self.ants = set()
        self.tabs = list(gsheet.keys())

    def load_sheet(self, node_csv='none', check_headers=False):
        """
        Gets the googlesheet information from the internet (or locally for testing etc)

        Parameters
        ----------
        node_csv : str
            node csv file status:  one of 'read', 'write', 'none' (only need first letter)
            'read' uses a local version as opposed to internet version
            'write' writes a local version
            'none' does neither of the above
        """
        node_csv = node_csv[0].lower()
        for tab in self.tabs:
            if node_csv == 'r':
                csv_data = []
                with open(tab + '.csv', 'r') as fp:
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
                with open(tab + '.csv', 'w') as fp:
                    fp.write('\n'.join(csv_data))
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
                self.ants.add(hkey)
                self.ant_to_tab[hkey] = tab
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
        self.ants = cm_utils.put_keys_in_order(list(self.ants), sort_order='NPR')
