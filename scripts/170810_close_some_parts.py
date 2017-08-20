#! /usr/bin/env python

from __future__ import print_function

from astropy.time import Time
import sys

now = Time.now()
log_file = 'scripts.log'
use_date = '2017/06/01'
do_it_this_time = True

parts_to_close = [
['A0','P'],
['A1','P'],
['A14','P'],
['A15','P'],
['A2','P'],
['A23','P'],
['A24','P'],
['A26','P'],
['A27','P'],
['A28','P'],
['A3','P'],
['A36','P'],
['A37','P'],
['A38','P'],
['A39','P'],
['A4','P'],
['A40','P'],
['A42','P'],
['A51','P'],
['A52','P'],
['A54','P'],
['A56','P'],
['A67','P'],
['A68','P'],
['A69','P'],
['A70','P'],
['A71','P'],
['A84','P'],
['A85','P'],
['A86','P'],
['A87','P']
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

for data in parts_to_close:
    s = 'stop_part.py --date {} -p {} -r {} '.format(use_date,data[0],data[1])
    if do_it_this_time:
        s+= '--actually_do_it\n'
    else:
        s+='\n'
    script_fp.write(s)
