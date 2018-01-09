#! /usr/bin/env python
from __future__ import absolute_import, division, print_function


def init_script(argv, log_file):
    output_script = argv[0].strip('.').strip('/').split('.')[0]
    print("starting {}".format(output_script))
    fp = open(output_script, 'w')
    s = '#! /usr/bin/env bash\n'
    s += 'echo {} >> {}\n'.format(output_script, log_file)
    fp.write(s)
    return fp


def part(add_or_stop, p, cdate, ctime, do_it):
    s = '{}_part.py -p {} -r {} '.format(
        add_or_stop, p[0], p[1])
    if add_or_stop == 'add':
        s += '-t {} -m {} '.format(p[2], p[3])
    s += '--date {} --time {}'.format(cdate, ctime)
    if do_it:
        s += ' --actually_do_it'
    s += '\n'
    return s


def connect(add_or_stop, up, dn, cdate, ctime, do_it):
    s = '{}_connection.py -u {} --uprev {} --upport {} -d {} --dnrev {} --dnport {} --date {} --time {}'.format(
        add_or_stop, up[0], up[1], up[2], dn[0], dn[1], dn[2], cdate, ctime)
    if do_it:
        s += ' --actually_do_it'
    s += '\n'
    return s
