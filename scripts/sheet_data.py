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

hu_col = {'Ant': 0, 'Pol': 4, 'Feed': 1, 'FEM': 2, 'PAM': 4, 'PAM Slot': 3, 'I2C_bus': -1, 'SNAP': 5, 'Port': 5, 'SNAP Slot': 6, 'Node': 6, 'APriori': -1}

gsheet = {}
gsheet['node0'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=0&single=true&output=csv"
gsheet['node7'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=780596546&single=true&output=csv"
gsheet['node8'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=1174361876&single=true&output=csv"
gsheet['node9'] = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrwdnbP2yBXDUvUZ0AXQ--Rqpt7jCkiv89cVyDgtWGHPeMXfNWymohaEtXi_-t7di7POGlg8qwhBlt/pub?gid=59309582&single=true&output=csv"

pol_comments = ['RF PWR', 'Goodness']
