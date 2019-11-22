#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
"""
from hera_mc import cm_active, cm_utils
from astropy.time import Time


class Checks:
    def __init__(self, start_time=2458500, stop_time='now', day_step=1.0):
        self.cmad = cm_active.ActiveData()
        self.start = cm_utils.get_astropytime(start_time)
        self.stop = cm_utils.get_astropytime(stop_time)
        self.step = day_step

    def check_for_duplicate_comments(self):
        cmdpre = 'delete from part_info where hpn='
        filename = 'dupcomm.sql'
        self.cmad.load_info()
        duplicates_found = 0
        with open(filename, 'w') as fp:
            for part, comments in self.cmad.info.items():
                ncomm = len(comments)
                for i in range(ncomm - 1):
                    for j in range(i + 1, ncomm):
                        if comments[i].comment == comments[j].comment:
                            duplicates_found += 1
                            hpn, rev = cm_utils.split_part_key(part)
                            if comments[i].posting_gpstime > comments[j].posting_gpstime:
                                posting_gpstime = comments[i].posting_gpstime
                            else:
                                posting_gpstime = comments[j].posting_gpstime
                            print("{}'{}' and hpn_rev='{}' and posting_gpstime='{}';".format(cmdpre, hpn, rev, posting_gpstime), file=fp)
        if duplicates_found:
            print("{} duplicates found".format(duplicates_found))
            print("run 'psql hera_mc -f {}'".format(filename))
        else:
            print("No duplicates found.")

    def apriori(self):
        """
        Check for multiple apriori active states between start and stop times.
        """
        next = self.start
        while next < self.stop:
            print(next.isot)
            print("This doesn't do anything yet")
            self.cmad.load_apriori(next)
            next += self.step

    def part_conn_assoc(self):
        """
        Checks to make sure that all connections have an associated active part
        between start and stop times.

        The database will allow non-active parts to have a connection, which is not
        desired.  This will check and list connections without an associated active
        part.  It does not Error or Warn, but just lists.

        Returns
        -------
        list
            List of missing parts.
        """
        missing_parts = {}
        next = self.start
        while next < self.stop:
            self.cmad.parts = None
            self.cmad.connections = None
            self.cmad.load_parts(next)
            self.cmad.load_connections(next)
            #print(self.cmad.at_date.isot)
            full_part_set = list(self.cmad.parts.keys())
            full_conn_set = set(list(self.cmad.connections['up'].keys()) + list(self.cmad.connections['down'].keys()))
            for key in full_conn_set:
                if key == 'xxPCH1:A':
                    print(self.cmad.at_date.isot)
                    try:
                        print(self.cmad.connections['up']['PCH1:A'])
                    except KeyError:
                        print("No up")
                    try:
                        print(self.cmad.connections['down']['PCH1:A'])
                    except KeyError:
                        print("No down")
                if key not in full_part_set:
                    missing_parts.setdefault(key, [])
                    missing_parts[key].append(next)
                    print(self.cmad.at_date.isot)
                    print("\t{} is not listed as an active part even though listed in an active connection.".format(key))
            next += self.step
        if len(missing_parts.keys()):
            print('Found the following parts:')
            print(missing_parts.keys())
        return missing_parts


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--comments', help="Check for duplicate comments", action='store_true')
    ap.add_argument('--connections', help="Check connections for ...", action='store_true')
    ap.add_argument('--apriori', help="Check for overlapping apriori states", action='store_true')
    args = ap.parse_args()

    cc = Checks()

    if args.comments:
        cc.check_for_duplicate_comments()
    if args.connections:
        cc.part_conn_assoc()
    if args.apriori:
        cc.apriori()
