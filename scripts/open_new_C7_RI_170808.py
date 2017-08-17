#! /usr/bin/env python

from __future__ import print_function

from astropy.time import Time
import sys

now = Time.now()
log_file = 'scripts.log'
use_date = '2017/08/01'
do_it_this_time = True

data_arr = [
           ['C7F84', 'A', 'eb', 'RI8A1E', 'A', 'a'],
           ['C7F84', 'A', 'nb', 'RI8A1N', 'A', 'a'],
           ['C7F85', 'A', 'eb', 'RI8A2E', 'A', 'a'],
           ['C7F85', 'A', 'nb', 'RI8A2N', 'A', 'a'],
           ['C7F86', 'A', 'eb', 'RI8A3E', 'A', 'a'],
           ['C7F86', 'A', 'nb', 'RI8A3N', 'A', 'a'],
           ['C7F87', 'A', 'eb', 'RI8A4E', 'A', 'a'],
           ['C7F87', 'A', 'nb', 'RI8A4N', 'A', 'a'],
           ['C7F52', 'A', 'eb', 'RI8A5E', 'A', 'a'],
           ['C7F52', 'A', 'nb', 'RI8A5N', 'A', 'a'],
           ['C7F53', 'A', 'eb', 'RI8A6E', 'A', 'a'],
           ['C7F53', 'A', 'nb', 'RI8A6N', 'A', 'a'],
           ['C7F54', 'A', 'eb', 'RI8A7E', 'A', 'a'],
           ['C7F54', 'A', 'nb', 'RI8A7N', 'A', 'a'],
           ['C7F55', 'A', 'eb', 'RI8A8E', 'A', 'a'],
           ['C7F55', 'A', 'nb', 'RI8A8N', 'A', 'a'],
           ['C7F24', 'A', 'eb', 'RI8B1E', 'A', 'a'],
           ['C7F24', 'A', 'nb', 'RI8B1N', 'A', 'a'],
           ['C7F25', 'A', 'eb', 'RI8B2E', 'A', 'a'],
           ['C7F25', 'A', 'nb', 'RI8B2N', 'A', 'a'],
           ['C7F26', 'A', 'eb', 'RI8B3E', 'A', 'a'],
           ['C7F26', 'A', 'nb', 'RI8B3N', 'A', 'a'],
           ['C7F27', 'A', 'eb', 'RI8B4E', 'A', 'a'],
           ['C7F27', 'A', 'nb', 'RI8B4N', 'A', 'a'],
# ['C7F36','A','eb','RI6A1E','A','a'],
# ['C7F36','A','nb','RI6A1N','A','a'],
# ['C7F51','A','eb','RI6A2E','A','a'],
# ['C7F51','A','nb','RI6A2N','A','a'],
# ['C7F69','A','eb','RI6A3E','A','a'],
# ['C7F69','A','nb','RI6A3N','A','a'],
# ['C7F70','A','eb','RI6A4E','A','a'],
# ['C7F70','A','nb','RI6A4N','A','a']
]

if len(sys.argv)>1:
    script_file = sys.argv[1]
else:
    script_file = sys.argv[0]
    if '/' in script_file:
        script_file = script_file.split('/')[1]
    script_file = script_file.split('.')[0]
print("Writing ",script_file)

script_fp = open(script_file,'w')
script_fp.write('# Generated {}\n'.format(str(now)))

if do_it_this_time:
    log_comment = "echo '{} -->> {}' >> {}\n".format(script_file, now, log_file)
    script_fp.write(log_comment)

for data in data_arr:
    s = 'add_connection.py --date {} -u {} -d {} '.format(use_date,data[0],data[3])
    s+= '--uprev {} --upport {} '.format(data[1],data[2])
    s+= '--dnrev {} --dnport {} '.format(data[4],data[5])
    if do_it_this_time:
        s+= '--actually_do_it\n'
    else:
        s+='\n'
    script_fp.write(s)
