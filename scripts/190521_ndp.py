#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import signal_chain
import sys

hera = signal_chain.Update(sys.argv[0], do_it=True)

parts_to_add = [
               [['NBP00', 'A', 'node-bulkhead', '00'], '2018/07/18', '11:00'],
               [['NBP09', 'A', 'node-bulkhead', '01'], '2019/05/15', '10:00']
]

connections_to_add = [
                     [['NBP00', 'A', 'e1'], ['PAM010', 'A', 'e'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'e2'], ['PAM011', 'A', 'e'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'e3'], ['PAM012', 'A', 'e'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'e4'], ['PAM013', 'A', 'e'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'e5'], ['PAM014', 'A', 'e'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'e6'], ['PAM015', 'A', 'e'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'e1'], ['PAM022', 'A', 'e'], '2019/02/16', '11:30'],
                     [['NBP00', 'A', 'e2'], ['PAM023', 'A', 'e'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'e3'], ['PAM024', 'A', 'e'], '2019/02/23', '12:10'],
                     [['NBP00', 'A', 'e4'], ['PAM025', 'A', 'e'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'e5'], ['PAM026', 'A', 'e'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'e6'], ['PAM027', 'A', 'e'], '2019/02/16', '11:30'],
                     [['NBP00', 'A', 'e7'], ['PAM028', 'A', 'e'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'e8'], ['PAM029', 'A', 'e'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'e9'], ['PAM030', 'A', 'e'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'e10'], ['PAM031', 'A', 'e'], '2019/02/16', '11:30'],
                     [['NBP00', 'A', 'e11'], ['PAM032', 'A', 'e'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'e12'], ['PAM033', 'A', 'e'], '2019/02/20', '11:00'],
                     [['NBP09', 'A', 'e1'], ['PAM035', 'A', 'e'], '2019/05/15', '11:00'],
                     [['NBP09', 'A', 'e2'], ['PAM036', 'A', 'e'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'e3'], ['PAM037', 'A', 'e'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'e4'], ['PAM038', 'A', 'e'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'e5'], ['PAM039', 'A', 'e'], '2019/05/17', '11:00'],
                     [['NBP09', 'A', 'e6'], ['PAM040', 'A', 'e'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'e7'], ['PAM041', 'A', 'e'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'e8'], ['PAM042', 'A', 'e'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'e9'], ['PAM043', 'A', 'e'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'e10'], ['PAM044', 'A', 'e'], '2019/05/15', '11:00'],
                     [['NBP09', 'A', 'e11'], ['PAM045', 'A', 'e'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'e12'], ['PAM046', 'A', 'e'], '2019/05/15', '11:00'],
                     [['NBP00', 'A', 'e7'], ['PAM047', 'A', 'e'], '2019/05/12', '11:00'],
                     [['NBP00', 'A', 'n1'], ['PAM010', 'A', 'n'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'n2'], ['PAM011', 'A', 'n'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'n3'], ['PAM012', 'A', 'n'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'n4'], ['PAM013', 'A', 'n'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'n5'], ['PAM014', 'A', 'n'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'n6'], ['PAM015', 'A', 'n'], '2018/10/30', '10:30'],
                     [['NBP00', 'A', 'n1'], ['PAM022', 'A', 'n'], '2019/02/16', '11:30'],
                     [['NBP00', 'A', 'n2'], ['PAM023', 'A', 'n'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'n3'], ['PAM024', 'A', 'n'], '2019/02/23', '12:10'],
                     [['NBP00', 'A', 'n4'], ['PAM025', 'A', 'n'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'n5'], ['PAM026', 'A', 'n'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'n6'], ['PAM027', 'A', 'n'], '2019/02/16', '11:30'],
                     [['NBP00', 'A', 'n7'], ['PAM028', 'A', 'n'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'n8'], ['PAM029', 'A', 'n'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'n9'], ['PAM030', 'A', 'n'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'n10'], ['PAM031', 'A', 'n'], '2019/02/16', '11:30'],
                     [['NBP00', 'A', 'n11'], ['PAM032', 'A', 'n'], '2019/02/20', '11:00'],
                     [['NBP00', 'A', 'n12'], ['PAM033', 'A', 'n'], '2019/02/20', '11:00'],
                     [['NBP09', 'A', 'n1'], ['PAM035', 'A', 'n'], '2019/05/15', '11:00'],
                     [['NBP09', 'A', 'n2'], ['PAM036', 'A', 'n'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'n3'], ['PAM037', 'A', 'n'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'n4'], ['PAM038', 'A', 'n'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'n5'], ['PAM039', 'A', 'n'], '2019/05/17', '11:00'],
                     [['NBP09', 'A', 'n6'], ['PAM040', 'A', 'n'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'n7'], ['PAM041', 'A', 'n'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'n8'], ['PAM042', 'A', 'n'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'n9'], ['PAM043', 'A', 'n'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'n10'], ['PAM044', 'A', 'n'], '2019/05/15', '11:00'],
                     [['NBP09', 'A', 'n11'], ['PAM045', 'A', 'n'], '2019/05/16', '11:00'],
                     [['NBP09', 'A', 'n12'], ['PAM046', 'A', 'n'], '2019/05/15', '11:00'],
                     [['NBP00', 'A', 'n7'], ['PAM047', 'A', 'n'], '2019/05/12', '11:00'],
                     [['FEM010', 'A', 'e'], ['NBP00', 'A', 'e1'], '2018/10/30', '10:30'],
                     [['FEM011', 'A', 'e'], ['NBP00', 'A', 'e2'], '2018/10/30', '10:30'],
                     [['FEM012', 'A', 'e'], ['NBP00', 'A', 'e3'], '2018/10/30', '10:30'],
                     [['FEM013', 'A', 'e'], ['NBP00', 'A', 'e4'], '2018/10/30', '10:30'],
                     [['FEM014', 'A', 'e'], ['NBP00', 'A', 'e5'], '2018/10/30', '10:30'],
                     [['FEM015', 'A', 'e'], ['NBP00', 'A', 'e6'], '2018/10/30', '10:30'],
                     [['FEM016', 'A', 'e'], ['NBP00', 'A', 'e1'], '2019/02/16', '11:30'],
                     [['FEM017', 'A', 'e'], ['NBP00', 'A', 'e2'], '2019/02/20', '11:00'],
                     [['FEM018', 'A', 'e'], ['NBP00', 'A', 'e3'], '2019/02/16', '11:30'],
                     [['FEM019', 'A', 'e'], ['NBP00', 'A', 'e4'], '2019/02/20', '11:00'],
                     [['FEM020', 'A', 'e'], ['NBP00', 'A', 'e5'], '2019/02/20', '11:00'],
                     [['FEM021', 'A', 'e'], ['NBP00', 'A', 'e6'], '2019/02/16', '11:30'],
                     [['FEM022', 'A', 'e'], ['NBP00', 'A', 'e7'], '2019/02/20', '11:00'],
                     [['FEM023', 'A', 'e'], ['NBP00', 'A', 'e8'], '2019/02/20', '11:00'],
                     [['FEM024', 'A', 'e'], ['NBP00', 'A', 'e9'], '2019/02/20', '11:00'],
                     [['FEM025', 'A', 'e'], ['NBP00', 'A', 'e10'], '2019/02/16', '11:30'],
                     [['FEM026', 'A', 'e'], ['NBP00', 'A', 'e11'], '2019/02/20', '11:00'],
                     [['FEM027', 'A', 'e'], ['NBP00', 'A', 'e12'], '2019/02/20', '11:00'],
                     [['FEM028', 'A', 'e'], ['NBP09', 'A', 'e11'], '2019/05/16', '11:00'],
                     [['FEM029', 'A', 'e'], ['NBP09', 'A', 'e12'], '2019/05/15', '11:00'],
                     [['FEM030', 'A', 'e'], ['NBP09', 'A', 'e10'], '2019/05/15', '11:00'],
                     [['FEM031', 'A', 'e'], ['NBP09', 'A', 'e1'], '2019/05/15', '11:00'],
                     [['FEM032', 'A', 'e'], ['NBP09', 'A', 'e8'], '2019/05/16', '11:00'],
                     [['FEM033', 'A', 'e'], ['NBP09', 'A', 'e5'], '2019/05/17', '11:00'],
                     [['FEM040', 'A', 'e'], ['NBP00', 'A', 'e2'], '2019/05/13', '11:20'],
                     [['FEM041', 'A', 'e'], ['NBP00', 'A', 'e5'], '2019/05/13', '11:40'],
                     [['FEM043', 'A', 'e'], ['NBP00', 'A', 'e9'], '2019/05/13', '12:00'],
                     [['FEM044', 'A', 'e'], ['NBP09', 'A', 'e9'], '2019/05/16', '11:00'],
                     [['FEM04', 'A', 'e'], ['NBP00', 'A', 'e3'], '2018/08/13', '12:00'],
                     [['FEM06', 'A', 'e'], ['NBP00', 'A', 'e1'], '2018/08/13', '12:00'],
                     [['FEM92', 'A', 'e'], ['NBP00', 'A', 'e3'], '2018/09/19', '10:30'],
                     [['FEM96', 'A', 'e'], ['NBP00', 'A', 'e1'], '2018/09/19', '10:30'],
                     [['FEM010', 'A', 'n'], ['NBP00', 'A', 'n1'], '2018/10/30', '10:30'],
                     [['FEM011', 'A', 'n'], ['NBP00', 'A', 'n2'], '2018/10/30', '10:30'],
                     [['FEM012', 'A', 'n'], ['NBP00', 'A', 'n3'], '2018/10/30', '10:30'],
                     [['FEM013', 'A', 'n'], ['NBP00', 'A', 'n4'], '2018/10/30', '10:30'],
                     [['FEM014', 'A', 'n'], ['NBP00', 'A', 'n5'], '2018/10/30', '10:30'],
                     [['FEM015', 'A', 'n'], ['NBP00', 'A', 'n6'], '2018/10/30', '10:30'],
                     [['FEM016', 'A', 'n'], ['NBP00', 'A', 'n1'], '2019/02/16', '11:30'],
                     [['FEM017', 'A', 'n'], ['NBP00', 'A', 'n2'], '2019/02/20', '11:00'],
                     [['FEM018', 'A', 'n'], ['NBP00', 'A', 'n3'], '2019/02/16', '11:30'],
                     [['FEM019', 'A', 'n'], ['NBP00', 'A', 'n4'], '2019/02/20', '11:00'],
                     [['FEM020', 'A', 'n'], ['NBP00', 'A', 'n5'], '2019/02/20', '11:00'],
                     [['FEM021', 'A', 'n'], ['NBP00', 'A', 'n6'], '2019/02/16', '11:30'],
                     [['FEM022', 'A', 'n'], ['NBP00', 'A', 'n7'], '2019/02/20', '11:00'],
                     [['FEM023', 'A', 'n'], ['NBP00', 'A', 'n8'], '2019/02/20', '11:00'],
                     [['FEM024', 'A', 'n'], ['NBP00', 'A', 'n9'], '2019/02/20', '11:00'],
                     [['FEM025', 'A', 'n'], ['NBP00', 'A', 'n10'], '2019/02/16', '11:30'],
                     [['FEM026', 'A', 'n'], ['NBP00', 'A', 'n11'], '2019/02/20', '11:00'],
                     [['FEM027', 'A', 'n'], ['NBP00', 'A', 'n12'], '2019/02/20', '11:00'],
                     [['FEM028', 'A', 'n'], ['NBP09', 'A', 'n11'], '2019/05/16', '11:00'],
                     [['FEM029', 'A', 'n'], ['NBP09', 'A', 'n12'], '2019/05/15', '11:00'],
                     [['FEM030', 'A', 'n'], ['NBP09', 'A', 'n10'], '2019/05/15', '11:00'],
                     [['FEM031', 'A', 'n'], ['NBP09', 'A', 'n1'], '2019/05/15', '11:00'],
                     [['FEM032', 'A', 'n'], ['NBP09', 'A', 'n8'], '2019/05/16', '11:00'],
                     [['FEM033', 'A', 'n'], ['NBP09', 'A', 'n5'], '2019/05/17', '11:00'],
                     [['FEM040', 'A', 'n'], ['NBP00', 'A', 'n2'], '2019/05/13', '11:20'],
                     [['FEM041', 'A', 'n'], ['NBP00', 'A', 'n5'], '2019/05/13', '11:40'],
                     [['FEM043', 'A', 'n'], ['NBP00', 'A', 'n9'], '2019/05/13', '12:00'],
                     [['FEM044', 'A', 'n'], ['NBP09', 'A', 'n9'], '2019/05/16', '11:00'],
                     [['FEM04', 'A', 'n'], ['NBP00', 'A', 'n3'], '2018/08/13', '12:00'],
                     [['FEM06', 'A', 'n'], ['NBP00', 'A', 'n1'], '2018/08/13', '12:00'],
                     [['FEM92', 'A', 'n'], ['NBP00', 'A', 'n3'], '2018/09/19', '10:30'],
                     [['FEM96', 'A', 'n'], ['NBP00', 'A', 'n1'], '2018/09/19', '10:30']
]

connections_to_stop = [
                      [['FEM010', 'A', 'e'], ['NBP00', 'A', 'e1'], '2018/10/30', '10:30'],
                      [['FEM011', 'A', 'e'], ['NBP00', 'A', 'e2'], '2018/10/30', '10:30'],
                      [['FEM012', 'A', 'e'], ['NBP00', 'A', 'e3'], '2018/10/30', '10:30'],
                      [['FEM013', 'A', 'e'], ['NBP00', 'A', 'e4'], '2018/10/30', '10:30'],
                      [['FEM014', 'A', 'e'], ['NBP00', 'A', 'e5'], '2018/10/30', '10:30'],
                      [['FEM015', 'A', 'e'], ['NBP00', 'A', 'e6'], '2018/10/30', '10:30'],
                      [['FEM017', 'A', 'e'], ['NBP00', 'A', 'e2'], '2019/02/20', '11:00'],
                      [['FEM020', 'A', 'e'], ['NBP00', 'A', 'e5'], '2019/02/20', '11:00'],
                      [['FEM024', 'A', 'e'], ['NBP00', 'A', 'e9'], '2019/02/20', '11:00'],
                      [['FEM04', 'A', 'e'], ['NBP00', 'A', 'e3'], '2018/08/13', '12:00'],
                      [['FEM06', 'A', 'e'], ['NBP00', 'A', 'e1'], '2018/08/13', '12:00'],
                      [['FEM92', 'A', 'e'], ['NBP00', 'A', 'e3'], '2018/09/19', '10:30'],
                      [['FEM96', 'A', 'e'], ['NBP00', 'A', 'e1'], '2018/09/19', '10:30'],
                      [['FEM010', 'A', 'n'], ['NBP00', 'A', 'n1'], '2018/10/30', '10:30'],
                      [['FEM011', 'A', 'n'], ['NBP00', 'A', 'n2'], '2018/10/30', '10:30'],
                      [['FEM012', 'A', 'n'], ['NBP00', 'A', 'n3'], '2018/10/30', '10:30'],
                      [['FEM013', 'A', 'n'], ['NBP00', 'A', 'n4'], '2018/10/30', '10:30'],
                      [['FEM014', 'A', 'n'], ['NBP00', 'A', 'n5'], '2018/10/30', '10:30'],
                      [['FEM015', 'A', 'n'], ['NBP00', 'A', 'n6'], '2018/10/30', '10:30'],
                      [['FEM017', 'A', 'n'], ['NBP00', 'A', 'n2'], '2019/02/20', '11:00'],
                      [['FEM020', 'A', 'n'], ['NBP00', 'A', 'n5'], '2019/02/20', '11:00'],
                      [['FEM024', 'A', 'n'], ['NBP00', 'A', 'n9'], '2019/02/20', '11:00'],
                      [['FEM04', 'A', 'n'], ['NBP00', 'A', 'n3'], '2018/08/13', '12:00'],
                      [['FEM06', 'A', 'n'], ['NBP00', 'A', 'n1'], '2018/08/13', '12:00'],
                      [['FEM92', 'A', 'n'], ['NBP00', 'A', 'n3'], '2018/09/19', '10:30'],
                      [['FEM96', 'A', 'n'], ['NBP00', 'A', 'n1'], '2018/09/19', '10:30'],
                      [['NBP00', 'A', 'e1'], ['PAM010', 'A', 'e'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'e2'], ['PAM011', 'A', 'e'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'e3'], ['PAM012', 'A', 'e'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'e4'], ['PAM013', 'A', 'e'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'e5'], ['PAM014', 'A', 'e'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'e6'], ['PAM015', 'A', 'e'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'e7'], ['PAM028', 'A', 'e'], '2019/02/20', '11:00'],
                      [['NBP00', 'A', 'n1'], ['PAM010', 'A', 'n'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'n2'], ['PAM011', 'A', 'n'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'n3'], ['PAM012', 'A', 'n'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'n4'], ['PAM013', 'A', 'n'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'n5'], ['PAM014', 'A', 'n'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'n6'], ['PAM015', 'A', 'n'], '2018/10/30', '10:30'],
                      [['NBP00', 'A', 'n7'], ['PAM028', 'A', 'n'], '2019/02/20', '11:00']
]

for part, cdate, ctime in parts_to_add:
    hera.update_part('add', part, cdate, ctime)

for up, down, cdate, ctime in connections_to_add:
    hera.update_connection('add', up, down, cdate, ctime)

for up, down, cdate, ctime in connections_to_stop:
    hera.update_connection('stop', up, down, cdate, ctime)

print("Next steps: psql hera_mc")
print("\tupdate connections set upstream_output_port='e' where upstream_output_port='eb' and upstream_part like 'PAM0%';")
print("\tupdate connections set upstream_output_port='n' where upstream_output_port='nb' and upstream_part like 'PAM0%';")
print("\tdelete from connections where upstream_part like 'CRF%'")
print("\tdelete from connections where downstream_part like 'CRF%'")
print("\tdelete from parts where hpn like 'CRF%'")

hera.done()
