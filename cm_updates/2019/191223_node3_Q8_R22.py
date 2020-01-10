#! /usr/bin/env python
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)
"""
update_part
    add_or_stop:  'add' or 'stop'
    part:  [hpn, rev, <type>, <mfg num>] (last two only for 'add')
    cdate:  date of update YYYY/MM/DD
    ctime:  time of update HH:MM
update_connection
    add_or_stop:  'add' or 'stop'
    up:  upstream connection [part, rev, port]
    down:  downstream connection [part, rev, port]
    cdate:  date of update YYYY/MM/DD
    ctime:  time of update HH:MM
"""

conn_to_stop = [  # node3 Q8
               [['FEM130', 'A', 'e'], ['NBP03', 'A', 'e4'], '2019/12/12', '10:00'],
               [['FEM130', 'A', 'n'], ['NBP03', 'A', 'n4'], '2019/12/12', '10:00'],
               [['FDV77', 'A', 'terminals'], ['FEM130', 'A', 'input'], '2019/12/12', '10:00'],
               [['PAM124', 'A', 'e'], ['SNPC000018', 'A', 'e10'], '2019/12/12', '10:00'],
               [['PAM124', 'A', 'n'], ['SNPC000018', 'A', 'n8'], '2019/12/12', '10:00'],
               [['NBP05', 'A', 'e12'], ['PAM124', 'A', 'e'], '2019/12/12', '10:00'],
               [['NBP05', 'A', 'n12'], ['PAM124', 'A', 'n'], '2019/12/12', '10:00'],
               [['PAM128', 'A', 'e'], ['SNPC000002', 'A', 'e2'], '2019/12/12', '10:00'],
               [['PAM128', 'A', 'n'], ['SNPC000002', 'A', 'n0'], '2019/12/12', '10:00'],
               [['NBP03', 'A', 'e4'], ['PAM128', 'A', 'e'], '2019/12/12', '10:00'],
               [['NBP03', 'A', 'n4'], ['PAM128', 'A', 'n'], '2019/12/12', '10:00'],
               #  node3 R22
               [['FEM129', 'A', 'e'], ['NBP03', 'A', 'e10'], '2019/12/12', '10:00'],
               [['FEM129', 'A', 'n'], ['NBP03', 'A', 'n10'], '2019/12/12', '10:00'],
               [['FDV85', 'A', 'terminals'], ['FEM129', 'A', 'input'], '2019/12/12', '10:00']
               # # node3 Q18
               # # node3 Q22
               #
               # [['PAM128', 'A', 'e'], ['SNPC000002', 'A', 'e2'], '2019/12/12', '10:00'],
               # [['PAM128', 'A', 'n'], ['SNPC000002', 'A', 'n0'], '2019/12/12', '10:00'],
               # [['NBP03', 'A', 'e4'], ['PAM128', 'A', 'e'], '2019/12/12', '10:00'],
               # [['NBP03', 'A', 'n4'], ['PAM128', 'A', 'n'], '2019/12/12', '10:00'],
               # [['FEM134', 'A', 'e'], ['NBP03', 'A', 'e8'], '2019/12/12', '10:00'],
               # [['FEM134', 'A', 'n'], ['NBP03', 'A', 'n8'], '2019/12/12', '10:00'],
                ]
for conn in conn_to_stop:
    hera.update_connection('stop', conn[0], conn[1], conn[2], conn[3])

parts_to_add = [
               [['FEM107', 'A', 'front-end', 'FEM107'], '2019/12/12', '10:01'],
               [['FEM128', 'A', 'front-end', 'FEM107'], '2019/12/12', '10:01']
                ]
for part in parts_to_add:
    hera.update_part('add', part[0], part[1], part[2])

conn_to_strt = [  # node3 Q8
               [['FEM128', 'A', 'e'], ['NBP03', 'A', 'e4'], '2019/12/12', '10:02'],
               [['FEM128', 'A', 'n'], ['NBP03', 'A', 'n4'], '2019/12/12', '10:02'],
               [['FDV77', 'A', 'terminals'], ['FEM128', 'A', 'input'], '2019/12/12', '10:02'],
               [['PAM128', 'A', 'e'], ['SNPC000018', 'A', 'e10'], '2019/12/12', '10:02'],
               [['PAM128', 'A', 'n'], ['SNPC000018', 'A', 'n8'], '2019/12/12', '10:02'],
               [['NBP05', 'A', 'e12'], ['PAM128', 'A', 'e'], '2019/12/12', '10:02'],
               [['NBP05', 'A', 'n12'], ['PAM128', 'A', 'n'], '2019/12/12', '10:02'],
               [['PAM124', 'A', 'e'], ['SNPC000002', 'A', 'e2'], '2019/12/12', '10:02'],
               [['PAM124', 'A', 'n'], ['SNPC000002', 'A', 'n0'], '2019/12/12', '10:02'],
               [['NBP03', 'A', 'e4'], ['PAM124', 'A', 'e'], '2019/12/12', '10:02'],
               [['NBP03', 'A', 'n4'], ['PAM124', 'A', 'n'], '2019/12/12', '10:02'],
               #  node3 R22
               [['FDV85', 'A', 'terminals'], ['FEM107', 'A', 'input'], '2019/12/12', '10:02'],
               [['FEM107', 'A', 'e'], ['NBP03', 'A', 'e12'], '2019/12/12', '10:02'],
               [['FEM107', 'A', 'n'], ['NBP03', 'A', 'n12'], '2019/12/12', '10:02']
               ]
for conn in conn_to_strt:
    hera.update_connection('add', conn[0], conn[1], conn[2], conn[3])

hera.done()
