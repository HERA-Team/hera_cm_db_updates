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
        for ak in self.all_keys:
            cak = self._cull_entry(ak)
            try:
                sahk = sorted(self.r.hkeys(ak))
                if cak in self.hashvals:
                    continue
                for ahk in sahk:
                    try:
                        val = self.r.hget(ak, ahk)
                    except UnicodeDecodeError:
                        val = '<<byte-data>>'
                    self.hashvals[cak] = {ahk: val}
            except redis.ResponseError:
                if cak in self.keyvals:
                    continue
                try:
                    val = self.r.get(ak)
                except (redis.ResponseError, UnicodeDecodeError):
                    val = '<<byte-data>>'
                self.keyvals[cak] = val

    def write_cull_info(self, fn='key_overview.txt'):
        print(f"Writing {fn}")
        single = []
        with open(fn, 'w') as fp:
            for ck, cv in self.culled.items():
                if len(cv) > 1:
                    print(f"{ck:20s}: {len(cv):03d} - {cv[:4]}", file=fp)
                else:
                    single.append(ck)
            print("\n----------Single----------", file=fp)
            print(f"{', '.join(single)}", file=fp)

    def write_kv(self, fn='key_vals.txt', trunc=35):
        print(f"Writing {fn}")
        with open(fn, 'w') as fp:
            for k, v in self.keyvals.items():
                if self.cull is None:
                    cnt = ""
                else:
                    cnt = f"{len(self.culled[k]):03d}"
                print("{:20s}  {}  -  {}".format(k, cnt, v[:trunc]), file=fp)

    def _dictitems(self, val):
        s = ''
        if isinstance(val, dict):
            s += self._dict_items(val)
        else:
            return f"\t{val}"

    def write_hv(self, fn='hash_vals.txt', trunc=35):
        print(f"Writing {fn}")
        with open(fn, 'w') as fp:
            for k, v in self.hashvals.items():
                if self.cull is None:
                    cnt = ""
                else:
                    cnt = f"({len(self.culled[k])})"
                print("{}  {}".format(k, cnt), file=fp)
                for k2, v2 in v.items():
                    print("\t{}: {}".format(k2, v2), file=fp)
