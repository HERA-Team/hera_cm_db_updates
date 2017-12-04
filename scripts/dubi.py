#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2017 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Script to handle updated the dubitable antennas.
"""

from __future__ import absolute_import, division, print_function
from hera_mc import part_connect
from astropy.time import Time

ant_list = ['HH4', 'HH5', 'HH6', 'HH7', 'HH8', 'HH9', 'HH10',
            'HH15', 'HH16', 'HH17', 'HH18', 'HH19', 'HH20', 'HH21', 'HH22',
            'HH29', 'HH30', 'HH31', 'HH32', 'HH33', 'HH34', 'HH35',
            'HH43', 'HH44', 'HH45', 'HH46', 'HH47', 'HH48', 'HH49',
            'HH57', 'HH58', 'HH59', 'HH60', 'HH61', 'HH62', 'HH63', 'HH64',
            'HH72', 'HH73', 'HH74', 'HH75', 'HH76', 'HH77', 'HH78', 'HH79', 'HH80', 'HH81',
            'HH89', 'HH90', 'HH91', 'HH92', 'HH93', 'HH94', 'HH95', 'HH96', 'HH97',
            'HH99', 'HH100', 'HH101', 'HH102', 'HH103', 'HH104', 'HH105', 'HH106', 'HH107', 'HH108', 'HH109',
            'HH110', 'HH111', 'HH112', 'HH113', 'HH114', 'HH115', 'HH116', 'HH117', 'HH118', 'HH119',
            'HH125', 'HH126', 'HH127', 'HH128', 'HH129', 'HH130', 'HH131', 'HH132', 'HH133', 'HH134', 'HH135',
            'HH144', 'HH145', 'HH146', 'HH147', 'HH148', 'HH149', 'HH150',
            'HH151', 'HH152', 'HH153', 'HH154', 'HH155', 'HH156', 'HH157', 'HH158', 'HH159',
            'HH160', 'HH161', 'HH162', 'HH163', 'HH164', 'HH165', 'HH166', 'HH167', 'HH168', 'HH169',
            'HH170', 'HH171', 'HH172', 'HH173', 'HH174', 'HH175', 'HH176', 'HH177', 'HH178', 'HH179',
            'HH180', 'HH181', 'HH182', 'HH183', 'HH184', 'HH185', 'HH186', 'HH187', 'HH188', 'HH189',
            'HH190', 'HH191', 'HH192', 'HH193', 'HH194', 'HH195', 'HH196', 'HH197', 'HH198', 'HH199',
            'HH200', 'HH201', 'HH202', 'HH203', 'HH204', 'HH205', 'HH206', 'HH207', 'HH208', 'HH209',
            'HH210', 'HH211', 'HH212', 'HH213', 'HH214', 'HH215', 'HH216', 'HH217', 'HH218', 'HH219',
            'HH220', 'HH221', 'HH222', 'HH223', 'HH224', 'HH225', 'HH226', 'HH227', 'HH228', 'HH229',
            'HH230', 'HH231', 'HH232', 'HH233', 'HH234', 'HH235', 'HH236', 'HH237', 'HH238', 'HH239',
            'HH240', 'HH241', 'HH242', 'HH243', 'HH244', 'HH245', 'HH246', 'HH247', 'HH248', 'HH249',
            'HH250', 'HH251', 'HH252', 'HH253', 'HH254', 'HH255', 'HH256', 'HH257', 'HH258', 'HH259',
            'HH260', 'HH261', 'HH262', 'HH263', 'HH264', 'HH265', 'HH266', 'HH267', 'HH268', 'HH269',
            'HH270', 'HH271', 'HH272', 'HH273', 'HH274', 'HH275', 'HH276', 'HH277', 'HH278', 'HH279',
            'HH280', 'HH281', 'HH282', 'HH283', 'HH284', 'HH285', 'HH286', 'HH287', 'HH288', 'HH289',
            'HH290', 'HH291', 'HH292', 'HH293', 'HH294', 'HH295', 'HH296', 'HH297', 'HH298', 'HH299',
            'HH300', 'HH301', 'HH302', 'HH303', 'HH304', 'HH305', 'HH306', 'HH307', 'HH308', 'HH309',
            'HH310', 'HH311', 'HH312', 'HH313', 'HH314', 'HH315', 'HH316', 'HH317', 'HH318', 'HH319',
            'HH320', 'HH321', 'HH322', 'HH323', 'HH324', 'HH325', 'HH326', 'HH327', 'HH328', 'HH329',
            'HH330', 'HH331', 'HH332', 'HH333', 'HH334', 'HH335', 'HH336', 'HH337', 'HH338', 'HH339',
            'HH340', 'HH341', 'HH342', 'HH343', 'HH344', 'HH345', 'HH346', 'HH347', 'HH348', 'HH349',
            'HH350'
            ]

part_connect.update_dubitable(None, Time.now().gps, ant_list)
