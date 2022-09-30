import redis
import json

r = redis.Redis('redishost', decode_responses=True)

snap_ants_str = r.hgetall('corr:snap_ants')

snap_ants = {}
for snaphost, indlist in snap_ants_str.items():
    snap_ants[snaphost] = json.loads(indlist)
print(snap_ants['heraNode16Snap0'])

map_snap_ant = json.loads(r.hget('corr:map', 'snap_to_ant'))
print(map_snap_ant['heraNode16Snap0'])

map_ant_snap = json.loads(r.hget('corr:map', 'ant_to_snap'))
print(map_ant_snap['151']['e']['host'])
