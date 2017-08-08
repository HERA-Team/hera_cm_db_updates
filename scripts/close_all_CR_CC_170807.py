#! /usr/bin/env python

from __future__ import print_function

script_file = open('close_all_CR_CC_170807','w')
csv_file = open('../initialization_data_connections.csv','r')

use_date = '2017/06/01'
do_it_this_time = False

for line in csv_file:
    if line[:2] == 'CR':
        data = line.split(',')
        s = 'stop_connection.py --date {} -u {} -d {} '.format(use_date,data[0],data[2])
        s+= '--uprev {} --upport {} '.format(data[1],data[4])
        s+= '--dnrev {} --dnport {} '.format(data[3],data[5])
        if do_it_this_time:
            s+= '--actually_do_it\n'
        else:
            s+='\n'
        script_file.write(s)