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
import datetime
from . import util
from hera_mc import cm_utils

hu_col = {'Ant': 0, 'Pol': 4, 'Feed': 1, 'FEM': 2, 'PAM': 4, 'Bulkhead-PAM_Slot': 3, 'I2C_bus': -1, 'SNAP': 5, 'Port': 5, 'SNAP_Slot': 6, 'Node': 6}
sheet_headers = ['Ant', 'Pol', 'Feed', 'FEM', 'PAM', 'Bulkhead-PAM_Slot', 'I2C_bus', 'SNAP_Slot', 'SNAP',
                 'Port', 'APriori', 'History', 'Actions', 'FEM_I2C', 'PAM_I2C', 'Goodness', 'Comments']

gsheet = {}
gsheet['node0'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=0&single=true&output=csv"
gsheet['node3'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1451443110&single=true&output=csv"
gsheet['node4'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1237822868&single=true&output=csv"
gsheet['node5'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1836116919&single=true&output=csv"
gsheet['node7'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=780596546&single=true&output=csv"
gsheet['node8'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1174361876&single=true&output=csv"
gsheet['node9'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=59309582&single=true&output=csv"
gsheet['node10'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=298497018&single=true&output=csv"

pol_comments = ['Goodness']
no_prefix = ['Comments']
com_ignore = ['Node', 'Ant', 'Pol', 'Feed', 'FEM', 'PAM', 'Bulkhead-PAM_Slot', 'Actions',
              'FEM_I2C', 'PAM_I2C', 'I2C_bus', 'SNAP_Slot', 'SNAP', 'Port', 'APriori', 'History']


class SheetData:
    def __init__(self):
        self.data = {}
        self.parts = {}
        self.header = {}
        self.date = {}
        self.notes = {}
        self.ants = set()
        self.tabs = sorted(list(gsheet.keys()))

    def load_sheet(self):
        """
        Gets the googlesheet information from the internet
        """

        for tab in self.tabs:
            xxx = requests.get(gsheet[tab])
            csv_tab = b''
            for line in xxx:
                csv_tab += line
            csv_tab = csv.reader(csv_tab.decode('utf-8').splitlines())
            for data in csv_tab:
                if data[0].startswith('Ant'):
                    self.header[tab] = ['Node'] + data
                    continue
                elif data[0].startswith('Date:'):
                    self.date[tab] = data[1]
                    break
                try:
                    antnum = int(data[0])
                except ValueError:
                    continue
                hpn = util.gen_hpn('HH', antnum)
                hkey = cm_utils.make_part_key(hpn, 'A')
                self.ants.add(hkey)
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
