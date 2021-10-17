"""List all redis keys"""
import redis


class RedisKeys():

    def __init__(self):
        connection_pool = redis.ConnectionPool(host='redishost', decode_responses=True)
        self.r = redis.StrictRedis(connection_pool=connection_pool, charset='utf-8')
        self.all_keys = sorted(self.r.keys())
        self.hashvals = {}
        self.keyvals = {}

    def _cull_entry(self, key, splitchar=':'):
        if self.cull is None:
            return key
        culled_key = splitchar.join(key.split(splitchar)[:self.cull])
        self.culled.setdefault(culled_key, [])
        self.culled[culled_key].append(key)
        return culled_key

    def split(self, cull=None):
        self.cull = cull
        self.culled = {}
        for this_key in self.all_keys:
            culled_key = self._cull_entry(this_key)
            try:
                these_hkeys = sorted(self.r.hkeys(this_key))
                self.hashvals.setdefault(culled_key, {})
                for thishk in these_hkeys:
                    try:
                        val = self.r.hget(this_key, thishk)
                    except UnicodeDecodeError:
                        val = '<<byte-data>>'
                    self.hashvals[culled_key].setdefault(thishk, {})
                    self.hashvals[culled_key][thishk] = val
            except redis.ResponseError:
                if culled_key in self.keyvals:
                    continue
                try:
                    val = self.r.get(this_key)
                except (redis.ResponseError, UnicodeDecodeError):
                    val = '<<byte-data>>'
                self.keyvals[culled_key] = val

    def write_cull_info(self, fn='key_overview.txt', trunc=50):
        print(f"Writing {fn}")
        single = []
        with open(fn, 'w') as fp:
            for ck, cv in self.culled.items():
                if len(cv) > 1:
                    data = ', '.join(cv[:12])
                    if len(data) > 50:
                        data = data[:50] + ' ...'
                    print(f"{ck:20s}: {len(cv):03d} - {data}", file=fp)
                else:
                    single.append(ck)
            print("\n----------Single----------", file=fp)
            print(f"{', '.join(single)}", file=fp)

    def write_kv(self, fn='key_vals.txt', trunc=50):
        print(f"Writing {fn}")
        with open(fn, 'w') as fp:
            for k, v in self.keyvals.items():
                if self.cull is None:
                    cnt = ""
                else:
                    cnt = f"{len(self.culled[k]):03d}"
                data = str(v)
                if len(data) > trunc:
                    data = data[:trunc] + ' ...'
                print("{:20s}  {}  -  {}".format(k, cnt, data), file=fp)

    def write_hv(self, fn='hash_vals.txt', trunc=50):
        print(f"Writing {fn}")
        with open(fn, 'w') as fp:
            for k, v in self.hashvals.items():
                if self.cull is None:
                    cnt = ""
                else:
                    cnt = f"({len(self.culled[k])})"
                print("{}  {}".format(k, cnt), file=fp)
                for k2, v2 in v.items():
                    data = str(v2)
                    if len(data) > trunc:
                        data = data[:trunc] + ' ...'
                    print("\t{}: {}".format(k2, data), file=fp)
