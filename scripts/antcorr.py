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

    def ant_2_host_corr(self, antnos):
        headers = ['Ant', 'Host', 'Corr Index']
        table_data = []
        for antno in antnos:
            hostname = self.map_ant_snap[antno]['e']['host']
            ants = self.map_snap_ant[hostname]
            corr = self.snap_corr[hostname]
            ind = ants.index(antno)
            table_data.append([antno, hostname, corr[ind]])
        print(tabulate.tabulate(table_data, headers=headers))
#print(snap_ants['heraNode16Snap0'])
#print(map_snap_ant['heraNode16Snap0'])
#print(map_ant_snap['151']['e']['host'])

    def corr_2_ant_host(self, corrs):
        headers = ['Corr Index', 'Ant', 'Host']
        table_data = []
        for corrno in corrs:
            hostname = self.snap_corr(int(corrno))
            corr = self.snap_corr[hostname]
            ants = self.map_snap_ant[hostname]
            ind = corr.index(int(corrno))
            table_data.append([corr, ants[ind], hostname])
        print(tabulate.tabulate(table_data, headers=headers))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    apah = ap.add_mutually_exclusive_group()
    apah.add_argument('-a', '--antno', help='antenna numbers', default=None)
    apah.add_argument('-s', '--snap_hostname', help='hostnames of SNAP', default=None)
    apah.add_argument('-c', '--corr_input', help="Correlator inputs")
    args = ap.parse_args()

    ac = AntCorr()
    if args.antno is not None:
        args.antno = args.antno.split(',')
        ac.ant_2_host_corr(args.antno)
