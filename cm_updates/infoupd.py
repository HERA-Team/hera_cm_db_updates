#! /usr/bin/env python
"""
Pulls the infoupd information out of the add_part_info script files.

Writes the file 'cat_infoupd.txt'
"""
import os
import datetime
import argparse
from hera_mc import cm_utils

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--directory', help="Search directory", default='2020')
    ap.add_argument('-s', '--search-after', dest='search_after', help="Search after YYMMDD",
                    default='200101')
    args = ap.parse_args()
else:
    args = argparse.Namespace(directory='2020', search_after='200101')

yr = int(args.search_after[:2])
mn = int(args.search_after[2:4])
dy = int(args.search_after[4:6])
args.search_after = datetime.datetime(year=yr, month=mn, day=dy)

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
                antenna = cm_utils.peel_key(pre.split()[2], 'PNR')
                comment = line.split('"')[1]
                dind = line.index('--date')
                date = line[dind + 12: dind + 17]
                tind = line.index('--time')
                time = line[tind + 7: tind + 12]
                s = "{} {:3d}    {}  {}  {}".format(antenna[0], antenna[1], date, time, comment)
                print(s)
                print(s, file=fpout)
