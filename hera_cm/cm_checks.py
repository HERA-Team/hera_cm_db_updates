# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Series of database checks."""
from hera_mc import cm_utils, cm_active, cm_sysutils
import redis
from node_control import he_check


def _get_keys(this_dict, these_keys, defv):
    fndkeys = []
    for key in these_keys:
        try:
            x = this_dict[key]
        except KeyError:
            x = defv
        fndkeys.append(x)
    return fndkeys


class Checks:
    """Check class."""

    def __init__(self, start_time=2458500, stop_time='now', day_step=1.0):
        """Initialize."""
        self.active = cm_active.ActiveData()
        self.start = cm_utils.get_astropytime(start_time)
        self.stop = cm_utils.get_astropytime(stop_time)
        self.step = day_step
        self.chk_same = None

    def check_for_same(self):
        if self.chk_same is None:
            print("Run 'check_hosts_ethers' first.")
            return
        for key, data in self.chk_same.items():
            for dev in ['arduino', 'wr', 'snap0', 'snap1', 'snap2', 'snap3']:
                for id in ['serial', 'mac', 'ip']:
                    for _i in range(1, len(data['source'])):
                        for _j in range(_i):
                            if data[dev][id][_i].lower() != data[dev][id][_j].lower():
                                if data[dev][id][_i].lower() == 'x' or\
                                  data[dev][id][_j].lower() == 'x':
                                    pass
                                else:
                                    print(f"====={key}=====")
                                    print("\t{}: {} != {}: {}".format(data['source'][_i],
                                                                      data[dev][id][_i],
                                                                      data['source'][_j],
                                                                      data[dev][id][_j]))

    def check_hosts_ethers(self, table_fmt='orgtbl'):
        self.hera_mc = cm_sysutils.node_info()
        r = redis.Redis('redishost', decode_responses=True)
        # Read hosts/ethers from redis
        he = he_check.Check('redis')
        he.parse_data()
        he_node_control = he.write_csv('return_only')
        self.redis_rd = {}
        self.redis_wr = {}
        self.redis_sn = {}
        tdat = []
        headers = ['source', 'arduino', 'wr', 'snap0', 'snap1', 'snap2', 'snap3']
        divider = ['-'*7, '-'*17, '-'*17, '-'*17, '-'*17, '-'*17, '-'*17]
        self.chk_same = {}
        # Read hera_mc
        for nd in range(0, 30):
            key = f"N{nd:02d}"
            tdat.append([key] * len(headers))
            self.chk_same[key] = {'source': []}
            for hdr in headers[1:]:
                self.chk_same[key][hdr] = {}
                for _d in ['serial', 'mac', 'ip']:
                    self.chk_same[key][hdr][_d] = []
            try:
                hmc = self.hera_mc[key]
                rd = {'serial': _get_keys(hmc, ['arduino'], '-'), 'ip': ['-'], 'mac': ['-']}
                wr = {'serial': _get_keys(hmc, ['wr'], '-'), 'ip': ['-'], 'mac': ['-']}
                sn = {'serial': _get_keys(hmc, ['snaps'], ['-']*4)[0], 'ip': ['-']*4, 'mac': ['-']*4}  # noqa
                for x in [rd, wr, sn]:
                    for i in range(len(x['serial'])):
                        notes = _get_keys(self.hera_mc, [x['serial'][i]], [['-']])[0]
                        for dv in ['ip', 'mac']:
                            tts = 0
                            for note in notes:
                                if note.lower().startswith(dv):
                                    ntn = note.split('|')[0]
                                    nts = int(note.split('|')[1])
                                    if nts > tts:
                                        x[dv][i] = ntn.split('-')[1].strip()
                                        tts = nts
                col1 = hmc['ncm']
                self.chk_same[key]['source'].append(col1)
                for x in ['serial', 'mac', 'ip']:
                    tdat.append([col1] + rd[x] + wr[x] + sn[x])
                    self.chk_same[key]['arduino'][x].append(rd[x][0])
                    self.chk_same[key]['wr'][x].append(wr[x][0])
                    for i in range(4):
                        self.chk_same[key][f'snap{i}'][x].append(sn[x][i])
            except KeyError:
                pass
            # Read redis
            self.chk_same[key]['source'].append('redis')
            self.redis_rd[key] = r.hgetall(f"status:node:{nd}")
            self.redis_wr[key] = r.hgetall(f"status:wr:heraNode{nd}wr")
            for i in range(4):
                self.redis_sn[key + str(i)] = r.hgetall(f"status:snap:heraNode{nd}Snap{i}")
            # ...get serial numbers
            rser = 'x'
            wser = _get_keys(self.redis_wr[key], ['serial'], '-')[0]
            self.chk_same[key]['arduino']['serial'].append(rser)
            self.chk_same[key]['wr']['serial'].append(wser)
            sser = []
            for i in range(4):
                sser.append(_get_keys(self.redis_sn[key + str(i)], ['serial'], '-')[0])
                self.chk_same[key][f"snap{i}"]['serial'].append(sser[i])
            if len(rser + wser + sser[0] + sser[1] + sser[2] + sser[3]) > 6:
                tdat.append(['redis', rser, wser, sser[0], sser[1], sser[2], sser[3]])
            # --- get macs
            rmac = _get_keys(self.redis_rd[key], ['mac'], '-')[0]
            wmac = _get_keys(self.redis_wr[key], ['mac'], 'x')[0]
            self.chk_same[key]['arduino']['mac'].append(rmac)
            self.chk_same[key]['wr']['mac'].append(wmac)
            for i in range(4):
                self.chk_same[key][f"snap{i}"]['mac'].append('x')
            if len(rmac + wmac) > 2:
                tdat.append(['redis', rmac, wmac, 'x', 'x', 'x', 'x'])
            # --- get ips
            rip = _get_keys(self.redis_rd[key], ['ip'], '-')[0]
            wip = _get_keys(self.redis_wr[key], ['ip'], '-')[0]
            self.chk_same[key]['arduino']['ip'].append(rip)
            self.chk_same[key]['wr']['ip'].append(wip)
            for i in range(4):
                self.chk_same[key][f"snap{i}"]['ip'].append('x')
            if len(rip + wip) > 2:
                tdat.append(['redis', rip, wip, 'x', 'x', 'x', 'x'])
            # Add hosts/ethers
            self.chk_same[key]['source'].append('host')
            for _e in ['serial', 'mac', 'ip']:
                trow = ['host']
                for _d in ['arduino', 'white_rabbit', 'snap0', 'snap1', 'snap2', 'snap3']:
                    trow.append(he_node_control[key][_e][_d])
                    if _d == 'white_rabbit':
                        _x = 'wr'
                    else:
                        _x = _d
                    self.chk_same[key][_x][_e].append(he_node_control[key][_e][_d])
                tdat.append(trow)
            if table_fmt != 'csv':
                tdat.append(divider)
        print(cm_utils.general_table_handler(headers, tdat, table_fmt))

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
