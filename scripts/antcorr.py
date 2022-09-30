import redis
import json
import argparse


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    apah = ap.add_mutually_exclusive_group()
    apah.add_argument('-a', '--antno', 'antenna number', default=None)
    apah.add_argument('-h', '--hostname', 'hostname', default=None)
    args = ap.parse_args()

    if args.antno is None and args.hostname is None:
        print("Must chose one of antno or hostname.")


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

    def ant_2_host_corr(self, antno):
        hostname = self.map_ant_snap[antno]['e']['host']
        ants = self.map_snap_ant[hostname]
        corr = self.snap_corr[hostname]
        print(hostname, ants, corr)
#print(snap_ants['heraNode16Snap0'])
#print(map_snap_ant['heraNode16Snap0'])
#print(map_ant_snap['151']['e']['host'])
