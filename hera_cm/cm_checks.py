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

    def apriori(self):
        """
        Check for multiple apriori active states between start and stop times.
        """
        next = self.start
        while next < self.stop:
            print(next.isot)
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
            print(next.isot)
            self.cmad.load_parts(next)
            self.cmad.load_connections(next)
            full_part_set = list(self.cmad.parts.keys())
            full_conn_set = set(list(self.cmad.connections['up']) + list(self.cmad.connections['down']))
            for key in full_conn_set:
                if key not in full_part_set:
                    missing_parts.setdefault(key, [])
                    missing_parts[key].append(next)
                    print("{} is not listed as an active part even though listed in an active connection.".format(key))
            next += self.step
        return missing_parts
