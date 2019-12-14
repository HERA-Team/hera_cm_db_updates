#! /usr/bin/env python
"""
Pulls the infoupd information out of the add_part_info script files.

Writes the file 'cat_infoupd.txt'
"""
import os
import datetime
import argparse

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--directory', help="Search directory", default='2019')
    ap.add_argument('-s', '--search-after', dest='search_after', help="Search after YYMMDD", default='191210')
    args = ap.parse_args()
else:
    args = argparse.Namespace(directory='2019', search_after='191201')

yr = int(args.search_after[:2])
mn = int(args.search_after[2:4])
dy = int(args.search_after[4:6])
args.search_after = datetime.datetime(year=yr, month=mn, day=dy)
args.keywords = args.keywords.split(',')

infoupd_files = []
files = os.listdir(args.directory)
for f in sorted(files):
    if 'infoupd' in f:
        infoupd_files.append(f)

fpout = open('cat_infoupd.txt', 'w')
infoupd_data = []
infoupd_track = []
for ifile in infoupd_files:
    path_ifile = os.path.join(args.directory, ifile)
    dstr = ifile.split('_')[0]
    yr = int(dstr[:2])
    mn = int(dstr[2:4])
    dy = int(dstr[4:6])
    dt = datetime.datetime(year=yr, month=mn, day=dy)
    if dt < args.search_after:
        continue
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
