#! /usr/bin/env python
"""
Pulls the connupd information out of the add_part_conn script files.

Writes the file 'cat_connupd.txt'
"""
import os
import datetime
import argparse

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--directory', help="Search directory", default='2019')
    ap.add_argument('-s', '--search-after', dest='search_after', help="Search after YYMMDD", default='191210')
    ap.add_argument('-k', '--keywords', help='Keywords to use only once.', default='echo,source')
    args = ap.parse_args()
else:
    args = argparse.Namespace(directory='2019', search_after='191201', keywords='echo,source')

yr = int(args.search_after[:2])
mn = int(args.search_after[2:4])
dy = int(args.search_after[4:6])
args.search_after = datetime.datetime(year=yr, month=mn, day=dy)
args.keywords = args.keywords.split(',')

connupd_files = []
files = os.listdir(args.directory)
for f in sorted(files):
    if 'connupd' in f:
        connupd_files.append(f)

fprm = open('rm_connupd', 'w')

connupd_data = []
connupd_track = []
for ifile in connupd_files:
    path_ifile = os.path.join(args.directory, ifile)
    fprm.write("rm -f {}\n".format(path_ifile))
    dstr = ifile.split('_')[0]
    yr = int(dstr[:2])
    mn = int(dstr[2:4])
    dy = int(dstr[4:6])
    dt = datetime.datetime(year=yr, month=mn, day=dy)
    if dt < args.search_after:
        continue
    with open(path_ifile, 'r') as fp:
        for line in fp:
            found_keyword = False
            for ky in args.keywords:
                if line.startswith(ky):
                    found_keyword = True
                    if ky not in connupd_track:
                        connupd_data.append(line.strip())
                        connupd_track.append(ky)
                    break
            if found_keyword:
                continue
            if '--date' in line:
                data = line[:line.index('--date')]
            else:
                data = line[:].strip()
            if data not in connupd_track:
                connupd_data.append(line.strip())
                connupd_track.append(data)

with open('cat_connupd.txt', 'w') as fp:
    for x in connupd_data:
        print(x, file=fp)
