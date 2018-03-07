#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2017 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Script to handle updating the dubitable antennas.
"""

from __future__ import absolute_import, division, print_function
from hera_mc import part_connect
from astropy.time import Time

ant_list = ['3', '4', '5', '6', '7', '8', '9',
            '10', '15', '16', '17', '18', '19',
            '20', '21', '22', '28', '29',
            '30', '31', '32', '33', '34', '35',
            '42', '43', '44', '45', '46', '47', '48', '49',
            '50', '56', '57', '58', '59',
            '60', '61', '62', '63', '64', '68',
            '72', '73', '74', '75', '76', '77', '78', '79',
            '80', '89',
            '90', '91', '92', '93', '94', '95', '96', '97',
            '104', '105', '106', '107', '108', '109',
            '110', '111', '112', '113', '114', '115',
            '125', '126', '127', '128', '129',
            '130', '131', '132', '133', '134', '135',
            '144', '145', '146', '147', '148', '149',
            '150', '151', '152', '153', '154', '155', '156', '157', '158', '159',
            '160', '161', '162', '163', '164', '165', '166', '167', '168', '169',
            '170', '171', '172', '173', '174', '175', '176', '177', '178', '179',
            '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',
            '190', '191', '192', '193', '194', '195', '196', '197', '198', '199',
            '200', '201', '202', '203', '204', '205', '206', '207', '208', '209',
            '210', '211', '212', '213', '214', '215', '216', '217', '218', '219',
            '220', '221', '222', '223', '224', '225', '226', '227', '228', '229',
            '230', '231', '232', '233', '234', '235', '236', '237', '238', '239',
            '240', '241', '242', '243', '244', '245', '246', '247', '248', '249',
            '250', '251', '252', '253', '254', '255', '256', '257', '258', '259',
            '260', '261', '262', '263', '264', '265', '266', '267', '268', '269',
            '270', '271', '272', '273', '274', '275', '276', '277', '278', '279',
            '280', '281', '282', '283', '284', '285', '286', '287', '288', '289',
            '290', '291', '292', '293', '294', '295', '296', '297', '298', '299',
            '300', '301', '302', '303', '304', '305', '306', '307', '308', '309',
            '310', '311', '312', '313', '314', '315', '316', '317', '318', '319',
            '320', '321', '322', '323', '324', '325', '326', '327', '328', '329',
            '330', '331', '332', '333', '334', '335', '336', '337', '338', '339',
            '340', '341', '342', '343', '344', '345', '346', '347', '348', '349',
            '350'
            ]

transition_gpstime = int(Time.now().gps)
part_connect.update_dubitable(None, transition_gpstime, ant_list)
