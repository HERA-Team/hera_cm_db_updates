#! /usr/bin/env python

from __future__ import print_function

from astropy.time import Time
import sys

now = Time.now()
log_file = 'scripts.log'
use_date = '2017/08/17'
do_it_this_time = True

data_arr = [
           ['C7F0', 'A', 'eb', 'RI8B5E', 'A', 'a'],
           ['C7F0', 'A', 'nb', 'RI8B5N', 'A', 'a'],
           ['C7F1', 'A', 'eb', 'RI8B6E', 'A', 'a'],
           ['C7F1', 'A', 'nb', 'RI8B6N', 'A', 'a'],
           ['C7F2', 'A', 'eb', 'RI5B1E', 'A', 'a'],
           ['C7F2', 'A', 'nb', 'RI5B1N', 'A', 'a'],
           ['C7F11', 'A', 'eb', 'RI5A4E', 'A', 'a'],
           ['C7F11', 'A', 'nb', 'RI5A4N', 'A', 'a'],
           ['C7F12', 'A', 'eb', 'RI8B8E', 'A', 'a'],
           ['C7F12', 'A', 'nb', 'RI8B8N', 'A', 'a'],
           ['C7F13', 'A', 'eb', 'RI5A2E', 'A', 'a'],
           ['C7F13', 'A', 'nb', 'RI5A2N', 'A', 'a'],
           ['C7F23', 'A', 'eb', 'RI5A3E', 'A', 'a'],
           ['C7F23', 'A', 'nb', 'RI5A3N', 'A', 'a'],
           ['C7F36', 'A', 'eb', 'RI5A8E', 'A', 'a'],
           ['C7F36', 'A', 'nb', 'RI5A8N', 'A', 'a'],
           ['C7F37', 'A', 'eb', 'RI8B7E', 'A', 'a'],
           ['C7F37', 'A', 'nb', 'RI8B7N', 'A', 'a'],
           ['C7F38', 'A', 'eb', 'RI8A2E', 'A', 'a'],
           ['C7F38', 'A', 'nb', 'RI8A2N', 'A', 'a'],
           ['C7F39', 'A', 'eb', 'RI5A1E', 'A', 'a'],
           ['C7F39', 'A', 'nb', 'RI5A1N', 'A', 'a'],
           ['C7F67', 'A', 'eb', 'RI5A5E', 'A', 'a'],
           ['C7F67', 'A', 'nb', 'RI5A5N', 'A', 'a'],
           ['C7F68', 'A', 'eb', 'RI5A6E', 'A', 'a'],
           ['C7F68', 'A', 'nb', 'RI5A6N', 'A', 'a']
]

if len(sys.argv) > 1:
    script_file = sys.argv[1]
else:
    script_file = sys.argv[0]
    if '/' in script_file:
        script_file = script_file.split('/')[1]
    script_file = script_file.split('.')[0]
print("Writing ", script_file)

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
