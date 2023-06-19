import redis
from datetime import datetime
import json


def wrview(nodes=24, alert=[]):
    WRV = WRView(nodes=nodes)
    WRV.get_wr_status()
    if len(alert):
        WRV.track_alert(email=alert)
    else:
        WRV.wr_status_table(show=True)


class WRView():
    def __init__(self, nodes):
        if isinstance(nodes, (int, float)):
            self.nodes = list(range(int(nodes)))
        elif isinstance(nodes, str):
            self.nodes = nodes.split(',')
        elif isinstance(nodes, list):
            self.nodes = nodes
        self.r = redis.Redis('redishost', decode_responses=True)

    def get_wr_status(self):
        self.wrstat = {}
        self.stat_now = datetime.now()
        for node in self.nodes:
            wrhost = f'status:wr:heraNode{node}wr'
            self.wrstat[node] = self.r.hgetall(wrhost)
            if not self.wrstat[node]:
                continue
            self.wrstat[node]['datetime'] = datetime.fromisoformat(self.wrstat[node]['timestamp'])  # noqa
            self.wrstat[node]['age'] = (self.stat_now - self.wrstat[node]['datetime']).seconds

    def track_alert(self, agelimit=1800, email=[], add_to_redis='track_phase_nodes'):
        self.bad_nodes = []
        self.good_nodes = []
        for node in self.nodes:
            if not self.wrstat[node]:
                continue
            try:
                good_one = 'TRACK_PHASE' in self.wrstat[node]['wr0_ss'] and self.wrstat[node]['age'] < agelimit
            except KeyError:
                good_one = False
            if good_one:
                self.good_nodes.append(node)
            else:
                self.bad_nodes.append(node)
        if add_to_redis is not None:
            self.r.set(add_to_redis, json.dumps(self.good_nodes))
        if len(self.bad_nodes):
            if len(email):
                from hera_mc import watch_dog
                subj = f"Bad WR: {', '.join([str(x) for x in self.bad_nodes])}"
                from_addr = 'hera@lists.berkeley.edu'
                msg = self.wr_status_table(show=False)
                try:
                    watch_dog.send_email(subj, msg, to_addr=email, from_addr=from_addr)
                except ConnectionRefusedError:
                    print("No email sent - ConnectionRefusedError")
            else:
                for bn in self.bad_nodes:
                    print(f"{bn}:  {self.wrstat[bn]['wr0_ss']}")

    def wr_status_table(self, fields=['wr0_ss', 'age', 'wr0_lock', 'wr1_lock', 'ip'], show=False):
        import tabulate
        table_data = []
        headers = ['Node'] + fields
        for node in self.nodes:
            if not self.wrstat[node]:
                continue
            table_row = [node]
            for fld in fields:
                table_row.append(self.wrstat[node][fld])
            table_data.append(table_row)
        if show:
            print(tabulate.tabulate(table_data, headers=headers))
        else:
            return tabulate.tabulate(table_data, headers=headers)
