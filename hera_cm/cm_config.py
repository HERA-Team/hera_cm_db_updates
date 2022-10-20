# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Series of database checks."""
from hera_mc import mc, cm_hookup, geo_handling
import yaml
import matplotlib.pyplot as plt


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


def snap_config(old_config_file, new_config_file='snap_config.out', ant_limit=208,
                use_nodes=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,18,19,20],
                min_connected=2, ignore_outriggers=True, include_hosts=['heraNode12Snap1'],
                skip_hosts=['heraNode12Snap0'],  # just put one in not used to remind
                start_block='fengines:', end_block='# Data is sent assuming a total'):
    key2use = 'HH' if ignore_outriggers else 'all'
    snap_conn = get_snap_connections()
    print(f"Reading old config file {old_config_file}")
    with open(old_config_file, 'r') as fp:
        sc = yaml.load(fp, Loader=yaml.Loader)
    antno = 0
    total_ants = 0
    phase_switch_index = 1
    hostname_order = []
    ant_list = []
    print("Generating new config.")
    for node in use_nodes:
        for sloc in range(4):
            hostname = f"heraNode{node}Snap{sloc}"
            if hostname not in snap_conn:
                print(f"\tSkipping {hostname} since no connections.")
                continue
            if hostname in skip_hosts:
                print(f"\tSkipping {hostname} since marked to skip.")
                continue
            if hostname not in sc['fengines']:
                print(f"\tFYI: {hostname} wasn't enabled in {old_config_file}")
            antconn = len(snap_conn[hostname][key2use])
            if antconn >= min_connected or hostname in include_hosts:
                this_set = []
                for ctr in range(3):
                    this_set.append(antno)
                    antno += 1
                if antno < ant_limit:
                    ant_per_host = len(snap_conn[hostname]['all'])
                    if ant_per_host > 3:
                        print(f"Warning:  more than 3 antennas:  {snap_conn[hostname]['all']}")
                        continue
                    for ant in snap_conn[hostname]['all']:
                        ant_list.append(ant.split(':')[0])
                    total_ants += ant_per_host
                    hostname_order.append(hostname)
                    sc['fengines'].setdefault(hostname, {'ants': [], 'phase_switch_index': []})
                    sc['fengines'][hostname]['ants'] = f"[{','.join([str(i) for i in this_set])}]"
                    this_set = []
                    for ctr in range(6):
                        this_set.append(phase_switch_index)
                        phase_switch_index += 1
                        if phase_switch_index > 24:
                            phase_switch_index = 1
                    sc['fengines'][hostname]['phase_switch_index'] = f"[{','.join([str(i) for i in this_set])}]"
            else:
                print(f"Skipping {hostname} due to {min_connected} < {antconn}")
            if antno >= ant_limit:
                break
        if antno >= ant_limit:
            break
    print(f"Writing new config file {new_config_file}")
    with open(old_config_file, 'r') as fpin:
        with open(new_config_file, 'w') as fpout:
            in_fengine_block = False
            for line in fpin:
                if line.startswith(start_block):
                    in_fengine_block = True
                    print('#\nfengines:', file=fpout)
                    for hostname in hostname_order:
                        print(f"    {hostname}:", file=fpout)
                        for fld in ['ants', 'phase_switch_index']:
                            val = sc['fengines'][hostname][fld].strip("'")
                            print(f"        {fld}: {val}", file=fpout)
                elif line.startswith(end_block):
                    in_fengine_block = False
                    print('#', file=fpout)
                if not in_fengine_block:
                    print(line.strip(), file=fpout)
    print(f"{len(hostname_order)} snaps and {total_ants} antennas.")
    print(f"Highest index {len(hostname_order) * 3}")
    with mc.MCSessionWrapper() as session:
        geo = geo_handling.Handling(session)
        loc = geo.get_location(ant_list, 'now')
        geo.set_graph(True)
        geo.plot_all_stations()
        geo.plot_stations(loc, xgraph='E', ygraph='N', label='none',
                          marker_color='k', marker_shape='o', marker_size=4)
    return ant_list