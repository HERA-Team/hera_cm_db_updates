#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import def_pc as pc
import sys
import six

log_file = 'scripts.log'
do_it_this_time = True

connections_to_stop = []
parts_to_stop = []

parts_to_add = [[['CRF002', 'A', 'cable-rfof', 'markings?'], '2019/02/19', '10:00'],
                [['CRF011', 'A', 'cable-rfof', 'markings?'], '2019/02/19', '10:00'],
                [['CRF014', 'A', 'cable-rfof', 'markings?'], '2019/02/19', '10:00'],
                [['CRF023', 'A', 'cable-rfof', 'markings?'], '2019/02/19', '10:00'],
                [['CRF024', 'A', 'cable-rfof', 'markings?'], '2019/02/19', '10:00'],
                [['CRF039', 'A', 'cable-rfof', 'markings?'], '2019/02/19', '10:00']
                ]

connections_to_add = [[['FDV8', 'A', 'terminals'], ['FEM017', 'A', 'input'], '2019/02/19', '11:00'],
                      [['FDV9', 'A', 'terminals'], ['FEM019', 'A', 'input'], '2019/02/19', '11:00'],
                      [['FDV3', 'A', 'terminals'], ['FEM020', 'A', 'input'], '2019/02/19', '11:00'],
                      [['FDV5', 'A', 'terminals'], ['FEM022', 'A', 'input'], '2019/02/19', '11:00'],
                      [['FDV11', 'A', 'terminals'], ['FEM023', 'A', 'input'], '2019/02/19', '11:00'],
                      [['FDV12', 'A', 'terminals'], ['FEM024', 'A', 'input'], '2019/02/19', '11:00'],
                      [['FDV7', 'A', 'terminals'], ['FEM026', 'A', 'input'], '2019/02/19', '11:00'],
                      [['FDV14', 'A', 'terminals'], ['FEM027', 'A', 'input'], '2019/02/19', '11:00'],
                      [['FEM017', 'A', 'e'], ['CRF002', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['FEM017', 'A', 'n'], ['CRF002', 'A', 'na'], '2019/02/19', '11:00'],
                      [['FEM019', 'A', 'e'], ['CRF011', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['FEM019', 'A', 'n'], ['CRF011', 'A', 'na'], '2019/02/19', '11:00'],
                      [['FEM020', 'A', 'e'], ['CRF012', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['FEM020', 'A', 'n'], ['CRF012', 'A', 'na'], '2019/02/19', '11:00'],
                      [['FEM022', 'A', 'e'], ['CRF014', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['FEM022', 'A', 'n'], ['CRF014', 'A', 'na'], '2019/02/19', '11:00'],
                      [['FEM023', 'A', 'e'], ['CRF023', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['FEM023', 'A', 'n'], ['CRF023', 'A', 'na'], '2019/02/19', '11:00'],
                      [['FEM024', 'A', 'e'], ['CRF024', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['FEM024', 'A', 'n'], ['CRF024', 'A', 'na'], '2019/02/19', '11:00'],
                      [['FEM026', 'A', 'e'], ['CRF026', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['FEM026', 'A', 'n'], ['CRF026', 'A', 'na'], '2019/02/19', '11:00'],
                      [['FEM027', 'A', 'e'], ['CRF039', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['FEM027', 'A', 'n'], ['CRF039', 'A', 'na'], '2019/02/19', '11:00'],
                      [['CRF002', 'A', 'eb'], ['PAM023', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['CRF002', 'A', 'nb'], ['PAM023', 'A', 'na'], '2019/02/19', '11:00'],
                      [['CRF011', 'A', 'eb'], ['PAM025', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['CRF011', 'A', 'nb'], ['PAM025', 'A', 'na'], '2019/02/19', '11:00'],
                      [['CRF012', 'A', 'eb'], ['PAM026', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['CRF012', 'A', 'nb'], ['PAM026', 'A', 'na'], '2019/02/19', '11:00'],
                      [['CRF014', 'A', 'eb'], ['PAM028', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['CRF014', 'A', 'nb'], ['PAM028', 'A', 'na'], '2019/02/19', '11:00'],
                      [['CRF023', 'A', 'eb'], ['PAM029', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['CRF023', 'A', 'nb'], ['PAM029', 'A', 'na'], '2019/02/19', '11:00'],
                      [['CRF024', 'A', 'eb'], ['PAM030', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['CRF024', 'A', 'nb'], ['PAM030', 'A', 'na'], '2019/02/19', '11:00'],
                      [['CRF026', 'A', 'eb'], ['PAM032', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['CRF026', 'A', 'nb'], ['PAM032', 'A', 'na'], '2019/02/19', '11:00'],
                      [['CRF039', 'A', 'eb'], ['PAM033', 'A', 'ea'], '2019/02/19', '11:00'],
                      [['CRF039', 'A', 'nb'], ['PAM033', 'A', 'na'], '2019/02/19', '11:00'],
                      [['PAM023', 'A', 'eb'], ['SNPC000057', 'A', 'e6'], '2019/02/19', '11:00'],
                      [['PAM023', 'A', 'nb'], ['SNPC000057', 'A', 'n4'], '2019/02/19', '11:00'],
                      [['PAM025', 'A', 'eb'], ['SNPA000008', 'A', 'e2'], '2019/02/19', '11:00'],
                      [['PAM025', 'A', 'nb'], ['SNPA000008', 'A', 'n0'], '2019/02/19', '11:00'],
                      [['PAM026', 'A', 'eb'], ['SNPA000008', 'A', 'e6'], '2019/02/19', '11:00'],
                      [['PAM026', 'A', 'nb'], ['SNPA000008', 'A', 'n4'], '2019/02/19', '11:00'],
                      [['PAM028', 'A', 'eb'], ['SNPA000024', 'A', 'e2'], '2019/02/19', '11:00'],
                      [['PAM028', 'A', 'nb'], ['SNPA000024', 'A', 'n0'], '2019/02/19', '11:00'],
                      [['PAM029', 'A', 'eb'], ['SNPA000024', 'A', 'e6'], '2019/02/19', '11:00'],
                      [['PAM029', 'A', 'nb'], ['SNPA000024', 'A', 'n4'], '2019/02/19', '11:00'],
                      [['PAM030', 'A', 'eb'], ['SNPA000024', 'A', 'e10'], '2019/02/19', '11:00'],
                      [['PAM030', 'A', 'nb'], ['SNPA000024', 'A', 'n8'], '2019/02/19', '11:00'],
                      [['PAM032', 'A', 'eb'], ['SNPA000020', 'A', 'e6'], '2019/02/19', '11:00'],
                      [['PAM032', 'A', 'nb'], ['SNPA000020', 'A', 'n4'], '2019/02/19', '11:00'],
                      [['PAM033', 'A', 'eb'], ['SNPA000020', 'A', 'e10'], '2019/02/19', '11:00'],
                      [['PAM033', 'A', 'nb'], ['SNPA000020', 'A', 'n8'], '2019/02/19', '11:00']
                      ]

fp = pc.init_script(sys.argv, log_file)

for c in connections_to_stop:
    fp.write(pc.connect('stop', c[0], c[1], c[2], c[3], do_it_this_time))

for p in parts_to_stop:
    fp.write(pc.part('stop', p[0], p[1], p[2], do_it_this_time))

for p in parts_to_add:
    fp.write(pc.part('add', p[0], p[1], p[2], do_it_this_time))

for c in connections_to_add:
    fp.write(pc.connect('add', c[0], c[1], c[2], c[3], do_it_this_time))


fp.close()
