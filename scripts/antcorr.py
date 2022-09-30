#! /usr/bin/env python
import redis
import json
import argparse
import tabulate


class AntCorr:
    def __init__(self):
        self.r = redis.Redis('redishost', decode_responses=True)
        snap_ants_str = self.r.hgetall('corr:snap_ants')
        self.snap_corr = {}
        for snaphost, indlist in snap_ants_str.items():
            self.snap_corr[snaphost] = json.loads(indlist)
        map_snap_ant_str = json.loads(self.r.hget('corr:map', 'snap_to_ant'))
        self.map_snap_ant = {}
        for snaphost, antpols in map_snap_ant_str.items():
            self.map_snap_ant[snaphost] = []
            for a in [antpols[i] for i in [0, 2, 4]]:
                if a is not None:
                    a = a[2: -1]
                self.map_snap_ant[snaphost].append(a)
        self.map_ant_snap = json.loads(self.r.hget('corr:map', 'ant_to_snap'))

    def ant_2_snap_corr(self, antenna_numbers):
        headers = ['Ant', 'Snap', 'Corr Index']
        table_data = []
        for antno in antenna_numbers:
            snap = self.map_ant_snap[antno]['e']['host']
            ants = self.map_snap_ant[snap]
            corrs = self.snap_corr[snap]
            table_data.append([antno, snap, corrs[ants.index(antno)]])
        print(tabulate.tabulate(table_data, headers=headers))
        print('\n')

    def corr_2_ant_snap(self, corr_indices):
        headers = ['Corr Index', 'Ant', 'Snap']
        table_data = []
        for corrno in corr_indices:
            fnd_snap = None
            for snap, corrinds in self.snap_corr.items():
                if corrno in corrinds:
                    if fnd_snap is not None:
                        raise ValueError(f"Found {corrno} in multiple snaps: {fnd_snap}, {snap}")
                    fnd_snap = snap + ''
                    fnd_corr = corrno + 0
                    ind = corrinds.index(corrno)
                    fnd_ant = self.map_snap_ant[fnd_snap][ind]
            table_data.append([fnd_corr, fnd_ant, fnd_snap])
        print(tabulate.tabulate(table_data, headers=headers))
        print('\n')

    def snap_2_ant_corr(self, snap_hostnames):
        headers = ['Snap', 'Antennas', 'Corr Indices']
        table_data = []
        for snap in snap_hostnames:
            ants = ', '.join([str(x) for x in self.map_snap_ant[snap]])
            corrs = ', '.join([str(x) for x in self.snap_corr[snap]])
            table_data.append([snap, ants, corrs])
        print(tabulate.tabulate(table_data, headers=headers))
        print('\n')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-a', '--ants', help='csv antenna numbers', default=None)
    ap.add_argument('-s', '--snaps', help='csv hostnames of SNAP', default=None)
    ap.add_argument('-c', '--corrs', help='csv correlator inputs')
    args = ap.parse_args()

    ac = AntCorr()
    if args.ants is not None:
        args.ants = args.ants.split(',')
        ac.ant_2_snap_corr(args.ants)
    if args.snaps is not None:
        args.snaps = args.snaps.split(',')
        ac.snap_2_ant_corr(args.snaps)
    if args.corrs is not None:
        args.corrs = [int(x) for x in args.corrs.split(',')]
        ac.corr_2_ant_snap(args.corrs)
