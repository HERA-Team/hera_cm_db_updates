#! /usr/bin/env python
"""
Pulls the connupd information out of the add_part_conn script files.

Writes the file 'cat_connupd.txt'
"""
import os
import datetime
import argparse


class CollapseConn:
    def __init__(self):
        self.connupd_files = {}
        files = os.listdir()
        for f in sorted(files):
            if 'connupd' in f:
                parts = f.split('_')
                dt = datetime.strftime(f"{parts[0]}T{parts[2]}", '%y%m%dT%H%m')
                self.connupd_files[dt] = f

# fprm = open('rm_connupd', 'w')

# connupd_data = []
# connupd_track = []
# for ifile in connupd_files:
#     path_ifile = os.path.join(args.directory, ifile)
#     fprm.write("rm -f {}\n".format(path_ifile))
#     dstr = ifile.split('_')[0]
#     try:
#         yr = int(dstr[:2])
#     except ValueError:
#         continue
#     mn = int(dstr[2:4])
#     dy = int(dstr[4:6])
#     dt = datetime.datetime(year=yr, month=mn, day=dy)
#     if dt < args.search_after:
#         continue
#     with open(path_ifile, 'r') as fp:
#         for line in fp:
#             found_keyword = False
#             for ky in args.keywords:
#                 if line.startswith(ky):
#                     found_keyword = True
#                     if ky not in connupd_track:
#                         connupd_data.append(line.strip())
#                         connupd_track.append(ky)
#                     break
#             if found_keyword:
#                 continue
#             if '--date' in line:
#                 data = line[:line.index('--date')]
#             else:
#                 data = line[:].strip()
#             if data not in connupd_track:
#                 connupd_data.append(line.strip())
#                 connupd_track.append(data)

# with open('cat_connupd.txt', 'w') as fp:
#     for x in connupd_data:
#         print(x, file=fp)
