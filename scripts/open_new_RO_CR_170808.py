#! /usr/bin/env python

from __future__ import print_function

script_file = open('open_new_RO_CR_170808','w')

data_arr = [
['CR8A1E','A','b','CC5R5C1','A','a'], ### RECEIVERATOR 8
]

use_date = '2017/08/01'
do_it_this_time = False

for data in data_arr:
    s = 'add_connection.py --date {} -u {} -d {} '.format(use_date,data[0],data[3])
    s+= '--uprev {} --upport {} '.format(data[1],data[2])
    s+= '--dnrev {} --dnport {} '.format(data[4],data[5])
    if do_it_this_time:
        s+= '--actually_do_it\n'
    else:
        s+='\n'
    script_file.write(s)