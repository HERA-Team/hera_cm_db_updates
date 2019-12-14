#! /usr/bin/env python

import os.path

infoupd_files = []

with open('infoupd.txt', 'r') as fp:
    for line in fp:
        infoupd_files.append(line.strip())

fpout = open('cat_infoupd.txt', 'w')

for ifile in infoupd_files:
    path_ifile = os.path.join('2019', ifile)
    with open(path_ifile, 'r') as fp:
        for line in fp:
            if line.startswith('add'):
                pre = line.split('"')[0]
                antenna = pre.split()[2]
                comment = line.split('"')[1]
                post = line.split('"')[2]
                date = post.split()[1]
                time = post.split()[3]
                fpout.write("{:6s} {} {}     {}\n".format(antenna, date, time, comment))
