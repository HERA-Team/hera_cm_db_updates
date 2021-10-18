# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Series of database checks."""
from hera_mc import cm_utils
from hera_mc import cm_active
import redis


class Checks:
    """Check class."""

    def __init__(self, start_time=2458500, stop_time='now', day_step=1.0):
        """Initialize."""
        self.active = cm_active.ActiveData()
        self.start = cm_utils.get_astropytime(start_time)
        self.stop = cm_utils.get_astropytime(stop_time)
        self.step = day_step

    def check_hosts_ethers(self, load_to_redis=False):
        self.active.load_connections()
        self.active.load_info()

        macip = {
           'rd': {'mac': {}, 'ip': {}},
           'wr': {'mac': {}, 'ip': {}}
        }
        found = {'mac': [], 'ip': []}
        self.dups = {}
        for ikey, info in self.active.info.items():
            rdwr = ikey[:2].lower()
            if rdwr in macip.keys():
                for note in info:
                    idtype = note.comment.lower().split('-')[0].strip()
                    if idtype in found:
                        val = note.comment.split('-')[1].strip()
                        if val in found[idtype]:
                            self.dups.setdefault(val, [])
                            self.dups[val].append(ikey)
                            self.dups[val].append(macip[rdwr][idtype][val])
                            print(f"{val} already found:  {self.dups[val]}!!!")
                        found[idtype].append(val)
                        macip[rdwr][idtype][val] = ikey
        print('=+=+=+=+=+=+=+=+=+=+=+=+=+=')
        # "invert" macip -- I should be able to skip macip
        self.picam = {}
        for rdwr in macip:
            for idtype in macip[rdwr]:
                for val in macip[rdwr][idtype]:
                    hpnkey = macip[rdwr][idtype][val]
                    self.picam.setdefault(hpnkey, {})
                    self.picam[hpnkey][idtype] = val
                    ncm = self.active.connections['up'][hpnkey]['MNT'].downstream_part
                    self.picam[hpnkey]['ncm'] = ncm
                    ncmkey = f"{ncm}:A"
                    try:
                        node = int(self.active.connections['up'][ncmkey]['RACK'].downstream_part[1:])  # noqa
                    except KeyError:
                        node = -1
                    self.picam[hpnkey]['node'] = node

        r = redis.Redis('redishost', decode_responses=True)
        for key, info in self.picam.items():
            redis_key = f"status:node:{info['node']}"
            data = r.hgetall(redis_key)
            dnod, dm, di = self._get_keys(data, ['node_ID', 'mac', 'ip'], 'rr')
            inod, im, ii = self._get_keys(info, ['node', 'mac', 'ip'], 'pp')
            if dnod == inod and dm == im and di == ii:
                print(f"<<<Node {dnod} agrees>>>")
            else:
                print(f"-------------{key}------------------")
                print(f"- redis {dnod:2s}  {dm:18s}  {di}")
                print(f"- psql  {inod:2s}  {im:18s}  {ii}")
            if load_to_redis:
                raise ValueError("NOTE READY YET")
                hostn = f"heraNode{info['node']}"
                vals = [hostn, info['ip'], info['mac']]
                check_redis_key = f"check:node:{info['node']}"
                r.hset(check_redis_key, vals, ex=3600)

    def _get_keys(self, this_dict, these_keys, defv):
        fndkeys = []
        for key in these_keys:
            try:
                x = str(this_dict[key])
            except KeyError:
                x = defv
            fndkeys.append(x)
        return fndkeys

    def check_for_duplicate_comments(self, verbose=False):
        """Check the database for duplicate comments."""
        cmdpre = 'delete from part_info where hpn='
        filename = 'dupcomm.sql'
        self.active.load_info()
        duplicates_found = 0
        with open(filename, 'w') as fp:
            for part, comments in self.active.info.items():
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
                            print("{}'{}' and hpn_rev='{}' and posting_gpstime='{}';"
                                  .format(cmdpre, hpn, rev, posting_gpstime), file=fp)
                            if verbose:
                                print(f"{hpn} ({posting_gpstime}): {comments[i]}")
        if duplicates_found:
            print("{} duplicates found".format(duplicates_found))
            print("run 'psql hera_mc -f {}'".format(filename))
        else:
            print("No duplicates found.")

    def apriori(self):
        """Check for multiple apriori active states between start and stop times."""
        next = self.start
        while next < self.stop:
            print(next.isot)
            print("This doesn't do anything yet")
            self.active.load_apriori(next)
            next += self.step

    def part_conn_assoc(self):
        """
        Check to make sure that all connections have an associated active part.

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
        print("Starting check at {}".format(next.isot))
        while next < self.stop:
            self.active.load_parts(next)
            self.active.load_connections(next)
            full_part_set = list(self.active.parts.keys())
            full_conn_set = set(list(self.active.connections['up'].keys()) +
                                list(self.active.connections['down'].keys()))
            for key in full_conn_set:
                if key not in full_part_set:
                    if key not in missing_parts:
                        print(self.active.at_date.isot)
                        print("\t{} is not listed as an active part "
                              "even though listed in an active connection.".format(key))
                        try:
                            print('\t', self.active.connections['up'][key])
                        except KeyError:
                            pass
                        try:
                            print('\t', self.active.connections['down'][key])
                        except KeyError:
                            pass
                    missing_parts.setdefault(key, [])
                    missing_parts[key].append(next.gps)
            next += self.step
        print("Stopping check at {}".format(next.isot))
        if len(missing_parts.keys()):
            print('Found the following parts:')
            for key in missing_parts.keys():
                print(f"\t{key}:  {missing_parts[key][0]}")
