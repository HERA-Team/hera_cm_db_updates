# -*- mode: python; coding: utf-8 -*-
# Copyright 2022 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Series of configuration utilities."""
from hera_mc import mc, cm_hookup, geo_handling
import yaml
import matplotlib.pyplot as plt
from datetime import datetime
import copy


configs = {'208a_221020':
           {
            'compile_limit': 208,
            'use_nodes': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,18,19,20],
            'min_connected': 2,
            'ignore_outriggers': True,
            'include_hosts': ['heraNode12Snap1'],
            'skip_hosts': ['heraNode12Snap0']
           },
           '231a_221021':
           {
            'compile_limit': 231,
            'use_nodes': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,20],
            'min_connected': 1,
            'ignore_outriggers': False,
            'include_hosts': [],
            'skip_hosts': []
           },
          }


def ret_str(this_set):
    return f"[{','.join([str(i) for i in this_set])}]"


def get_snap_connections(verbose=False):
    hostinfo = {}
    hookup = cm_hookup.get_hookup('H')
    for ant in hookup:
        for port in hookup[ant].hookup:
            if len(hookup[ant].hookup[port]) == 7:
                snap_sn = hookup[ant].hookup[port][-1].upstream_part
                node_num = int(hookup[ant].hookup[port][-1].downstream_part[1:])
                loc_num = int(hookup[ant].hookup[port][-1].downstream_input_port[3:])
                hostname = f"heraNode{node_num}Snap{loc_num}"
                hostinfo.setdefault(hostname, {'sn': snap_sn, 'all': [], 'cnt': 0})
                if ant not in hostinfo[hostname]['all']:
                    hostinfo[hostname]['all'].append(ant)
                    hostinfo[hostname]['cnt'] += 1
                hostinfo[hostname].setdefault(ant[:2], [])
                if ant not in hostinfo[hostname][ant[:2]]:
                    hostinfo[hostname][ant[:2]].append(ant)
    return hostinfo


class Configuration:
    def __init__(self, old_config_file):
        self.hostinfo = get_snap_connections()
        self.setup_config_gen(old_config_file)

    def setup_config_gen(self, old_config_file):
        self.old_config_file = old_config_file
        print(f"Reading old config file {old_config_file}")
        with open(old_config_file, 'r') as fp:
            self.sc = yaml.load(fp, Loader=yaml.Loader)

    def get_hostnames_to_use(self,
                             compile_limit,
                             use_nodes=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,20],
                             min_connected=1, ignore_outriggers=False,
                             include_hosts=[], skip_hosts=[]):
        key2use = 'HH' if ignore_outriggers else 'all'
        self.compile_limit = compile_limit
        self.use_nodes = use_nodes
        self.min_connected = min_connected
        self.ignore_outriggers = ignore_outriggers
        self.include_hosts = include_hosts
        self.skip_hosts = skip_hosts

        print("Getting hosts.")
        hosts_to_use  = copy.copy(include_hosts)
        stop_loop = False
        for node in use_nodes:
            for sloc in range(4):
                if len(hosts_to_use) * 3 > compile_limit:
                    stop_loop = True
                    break
                else:
                    this_hostname = f"heraNode{node}Snap{sloc}"
                    if this_hostname in hosts_to_use:
                        continue
                    if this_hostname in skip_hosts:
                        print(f"    Skipping {this_hostname} since marked to skip.")
                        continue
                    if this_hostname not in self.hostinfo:
                        print(f"    Skipping {this_hostname} since no connections.")
                        continue
                    antconn = len(self.hostinfo[this_hostname][key2use])
                    if antconn < min_connected:
                        print(f"    Skipping {this_hostname} since {antconn} < {min_connected}")
                        continue
                    if this_hostname not in self.sc['fengines']:
                        print(f"    FYI: {this_hostname} wasn't enabled in {self.old_config_file}")
                    hosts_to_use.append(this_hostname)
            if stop_loop:
                break
        self.hosts_to_use = []
        self.hosts_not_used = []
        for node in range(max(use_nodes) + 1):
            for sloc in range(4):
                this_hostname = f"heraNode{node}Snap{sloc}"
                if this_hostname in hosts_to_use:
                    self.hosts_to_use.append(this_hostname)
                else:
                    self.hosts_not_used.append(this_hostname)

    def generate_new_fengines(self):
        self.total_ants = 0
        self.ant_list = []

        antno = 0
        phase_switch_index = 1
        print("Generating new fengines.")
        self.fengines = {}
        for this_host in self.hosts_to_use:
            ant_per_host = len(self.hostinfo[this_host]['all'])
            if ant_per_host > 3:
                raise ValueError(f"!!!!!!Warning:  more than 3 antennas:  {self.hostinfo[this_host]['all']}")
            for ant in self.hostinfo[this_host]['all']:
                self.ant_list.append(ant.split(':')[0])
            self.total_ants += ant_per_host

            ant_set = []
            for ctr in range(3):
                ant_set.append(antno)
                antno += 1
            phase_set = []
            for ctr in range(6):
                phase_set.append(phase_switch_index)
                phase_switch_index += 1
                if phase_switch_index > 24:
                    phase_switch_index = 1
            self.max_antno = antno
            self.fengines[this_host] = {'ants': ret_str(ant_set), 'phase_switch_index': ret_str(phase_set)}
   
    def write_yaml(self, start_block='fengines:', end_block='# Data is sent assuming a total'):
        wtime = datetime.strftime(datetime.now(), '%y%m%d%H%M')
        self.new_config_file = f"{self.old_config_file.split('.')[0]}_{self.compile_limit}_{wtime}.yaml"
        print(f"Writing new config file {self.new_config_file}")
        with open(self.old_config_file, 'r') as fpin:
            with open(self.new_config_file, 'w') as fpout:
                in_fengine_block = False
                for line in fpin:
                    if line.startswith(start_block):
                        in_fengine_block = True
                        print("# ---snap_config parameters---", file=fpout)
                        print(f"# compile_limit={self.compile_limit}", file=fpout)
                        print(f"# use_nodes=[{','.join([str(x) for x in self.use_nodes])}]", file=fpout)
                        print(f"# min_connected={self.min_connected}", file=fpout)
                        print(f"# ignore_outriggers={str(self.ignore_outriggers)}", file=fpout)
                        print(f"# include_hosts=[{','.join(self.include_hosts)}]", file=fpout)
                        print(f"# skip_hosts=[{','.join(self.skip_hosts)}]", file=fpout)
                        print('fengines:', file=fpout)
                        for hostname in self.hosts_to_use:
                            print(f"    {hostname}:", file=fpout)
                            for fld in ['ants', 'phase_switch_index']:
                                val = self.fengines[hostname][fld].strip("'")
                                print(f"        {fld}: {val}", file=fpout)
                    elif line.startswith(end_block):
                        in_fengine_block = False
                        print('#', file=fpout)
                    if not in_fengine_block:
                        print(line.strip(), file=fpout)
        print(f"{len(self.hosts_to_use)} snaps and {self.total_ants} antennas.")
        print(f"Highest index {self.max_antno}")
        with mc.MCSessionWrapper() as session:
            geo = geo_handling.Handling(session)
            loc = geo.get_location(self.ant_list, 'now')
            geo.set_graph(True)
            geo.plot_all_stations() 
            geo.plot_stations(loc, xgraph='E', ygraph='N', label='none',
                            marker_color='k', marker_shape='o', marker_size=4)
            plt.axis(xmin=540400, xmax=541400)