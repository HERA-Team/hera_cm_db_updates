#! /usr/bin/env python
from hera_mc import cm_hookup, mc, geo_sysdef
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import yaml


NODES = list(range(30))
PORTS = list(range(1, 13))
BKCLR = 'k'
NODE_INFO = geo_sysdef.read_nodes()
STATUS = {
    0: {'msg': 'ok', 'color': None},
    1: {'msg': "undetermined", 'color': '0.5'},
    2: {'msg': "hookup not found via node port", 'color': 'b'},
    3: {'msg': "antenna not found from node port", 'color': 'm'},
    4: {'msg': "nodes don't match", 'color': 'r'},
    5: {'msg': "ports don't match", 'color': 'c'}
}

class Antenna:
    def __init__(self, node, port):
        self.node = node
        self.port = port
        self.status = 1
        self.hpn = '---'
        self.number = None

    def set_hpn(self, hpn):
        self.hpn = hpn
        self.number = int(self.hpn[2:])

class Grid:
    fyi_all_params = ['nodes', 'ports', 'background', 'antennas', 'inputs']

    def __init__(self, highlight={}, nodes=NODES, ports=PORTS, background=BKCLR, minval=None, maxval=None):
        if isinstance(highlight, str):
            with open(highlight, 'r') as fp:
                highlight = yaml.safe_load(fp)
        self.params = list(highlight.keys())
        highlight = self._proc_colors(highlight, minval=minval, maxval=maxval)
        self.antennas_to_highlight = {}
        self.nodes = nodes
        self.ports = ports
        self.background = background
        for param in self.params:
            setattr(self, param, highlight[param])

    def show(self, hu):
        for component in hu:
            print(component, end='')
        print()

    def _proc_colors(self, highlight, minval, maxval):
        self.colormap = plt.cm.rainbow
        self.add_colorbar = False
        fmm = [10000.0, -100000.0]
        found_float = []
        self.params_to_apply = []
        for param_to_check in ['antennas', 'inputs']:
            if param_to_check in self.params:
                self.params_to_apply.append(param_to_check)

        for param in self.params_to_apply:
            for inp, clr in highlight[param].items():
                if isinstance(clr, float):
                    found_float.append(inp)
                    if clr < fmm[0]:
                        fmm[0] = clr
                    elif clr > fmm[1]:
                        fmm[1] = clr
        if len(found_float):
            for param in self.params_to_apply:
                if minval is None:
                    minval = 0.9 * fmm[0]
                if maxval is None:
                    maxval = 1.1 * fmm[1]
                self.add_colorbar = True
                self.norm = colors.Normalize(vmin=minval, vmax=maxval)
                for inp in found_float:
                    highlight[param][inp] = self.colormap(self.norm(highlight[param][inp]))
        return highlight

    def addplot(self, title=None, marker=',', markersize=None, highlight_offset=[0.0, 0.0], force_text=False, show_text=True):
        newfig = title is not None
        if newfig:
            fig = plt.figure(title, figsize=(9.75,6.5))
        for j, node in enumerate(self.nodes):
            for i, port in enumerate(self.ports):
                this_input = f"{node}-{port}"
                this_color = self.node_port_colors[this_input]
                this_ant = self.ants_by_node[node][i]
                antenna_number = int(this_ant.split(':')[0])
                if antenna_number == -1:
                    try:
                        this_ant = str(NODE_INFO[node]['ants'][i])
                    except IndexError:
                        pass
                plt.plot(port, node, marker, markersize=markersize, color=this_color)
                if show_text:
                    weight = 'extra bold'
                    if force_text:
                        weight = 'normal'
                        this_color = force_text
                    x = port - self._xtxt_offset(this_ant)
                    y = node - 0.25
                    ant_txt = '---' if antenna_number < 0 else this_ant
                    plt.text(x, y, ant_txt, color=this_color, weight=weight)
        if newfig:
            if self.add_colorbar:
                fig.colorbar(plt.cm.ScalarMappable(cmap=self.colormap, norm=self.norm))
            plt.xlabel('Node input port (snap input order)')
            plt.ylabel('Node number')
            plt.title(title)
            plt.xticks(self.ports, [str(x) for x in self.ports])
            plt.yticks(self.nodes, [str(x) for x in self.nodes])
            for x in [3.5, 6.5, 9.5]:
                plt.plot([x, x], [-1, 30], '--', color='.7')
            plt.axis([0.2, 13, 0, len(self.nodes) + 2])
            for i in range(4):
                plt.text(1.5 + i*3, len(self.nodes)+0.85, f'SNAP {i}')

    def _handle_missing(self):
        not_found = []
        for i in range(350):
            if i in NODE_INFO[0]['ants']:
                continue
            if i not in self.found_antennas:
                not_found.append(i)
        print(f"Didn't find {len(not_found)}")
        print(', '.join([str(x) for x in not_found]))

    def print_ant_codes(self, this_code):
        int_code = int(this_code.split(':')[0])
        if int_code == -4:
            antenna, this_input, other_input = this_code.split(':')[1].split(',')
            print("WARNING - nodes don't match!")
            print(f"\tAntenna {antenna}")
            print(f"\tTrying {this_input}")
            print(f"\tFound {other_input}")
        elif int_code == -5:
            antenna, this_input, other_input = this_code.split(':')[1].split(',')
            print("WARNING - ports don't match!")
            print(f"\tAntenna {antenna}")
            print(f"\tTrying {this_input}")
            print(f"\tFound {other_input}")

    def get_connected(self):  # was make
        self.found_antennas = []
        self.ants_by_node = {}
        self.node_port_colors = {}
        with mc.MCSessionWrapper(session=None) as session:
            hookup = cm_hookup.Hookup(session)
            ant_hudict = hookup.get_hookup(hpn='H')
            nbp_hudict = hookup.get_hookup(hpn='NBP')
            for this_node in self.nodes:
                self.ants_by_node[this_node] = []
                nbp = f"NBP{this_node:02d}"
                key = f"{nbp}:A"
                for this_port in self.ports:
                    # Get antenna from node port or provide not_found_code
                    this_input = f"{this_node}-{this_port}"
                    polport = f'E<e{this_port}'
                    try:
                        hu_from_nbp = nbp_hudict[key].hookup[polport]
                    except KeyError:
                        hu_from_nbp = []
                    this_antenna = Antenna(this_node, this_port)
                    if not len(hu_from_nbp):
                        this_antenna.status = 2
                    else:
                        ant_from_nbp = hu_from_nbp[0].upstream_part
                        if ant_from_nbp[0] != 'H':  # This likely just means not connected.
                            this_antenna.status = 3
                        else:
                            this_antenna.set_hpn(ant_from_nbp)

                    # Process found antennas
                    antenna_number = int(this_antenna.split(':')[0])
                    if antenna_number >= 0:
                        self.found_antennas.append(antenna_number)
                        antkey = f"{this_antenna.hpn}:A"
                        hu_from_ant = ant_hudict[antkey].hookup['E<ground']
                        node_from_ant = int(hu_from_ant[3].downstream_part[3:])
                        port_from_ant = int(hu_from_ant[3].downstream_input_port[1:])
                        if not (node_from_ant == this_node):
                            this_antenna = f'-4:{antenna},{this_input},{node_from_ant}-{port_from_ant}'
                        if not (port_from_ant == this_port):  # This likely just means not connected.
                            this_antenna = f'-5:{antenna},{this_input},{node_from_ant}-{port_from_ant}'
                    self.ants_by_node[this_node].append(this_antenna)
                    # Set node-port color
                    this_color = self.background
                    if antenna_number < 0:
                        this_color = self.not_found_codes[antenna_number]['color']
                    if this_antenna in self.antennas_to_highlight:
                        this_color = self.antennas_to_highlight[antenna_number]
                    self.node_port_colors[this_input] = this_color

    def _xtxt_offset(self, antenna):
        """Offset so that the numbers line-up."""
        if antenna[0] == '!':
            return 0.15
        if len(antenna) == 3:
            return 0.2
        if len(antenna) == 2:
            return 0.15
        return 0.1