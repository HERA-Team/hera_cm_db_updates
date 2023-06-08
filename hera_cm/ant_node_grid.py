#! /usr/bin/env python
from hera_mc import cm_hookup, mc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import yaml


NODES = list(range(1, 23))
PORTS = list(range(1, 13))
BKCLR = 'k'

class Grid:
    def __init__(self, data={}, nodes=NODES, ports=PORTS, background=BKCLR, minval=None, maxval=None):
        if isinstance(data, str):
            with open(data, 'r') as fp:
                data = yaml.safe_load(fp)
        self.params = list(data.keys())
        fyi_all_params = ['nodes', 'ports', 'background', 'antennas', 'inputs']
        data = self._proc_colors(data, minval=minval, maxval=maxval)
        self.antennas = {}
        self.inputs = {}
        self.nodes = nodes
        self.ports = ports
        self.background = background
        for param in self.params:
            setattr(self, param, data[param])
        self.antenna_tracker = {}
        self._pdat = {}

    def show(self, hu):
        for component in hu:
            print(component, end='')
        print()

    def _proc_colors(self, data, minval, maxval):
        self.colormap = plt.cm.rainbow
        self.add_colorbar = False
        fmm = [10000.0, -100000.0]
        found_float = []
        self.params_to_apply = []
        for param_to_check in ['antennas', 'inputs']:
            if param_to_check in self.params:
                self.params_to_apply.append(param_to_check)

        for param in self.params_to_apply:
            for inp, clr in data[param].items():
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
                    data[param][inp] = self.colormap(self.norm(data[param][inp]))
        return data

    def addplot(self, title=None, symbol=',', data_offset=[0.0, 0.0], force_text=False, show_text=True):
        newfig = title is not None
        if newfig:
            fig = plt.figure(title, figsize=(9.75,6.5))
        for j, node in enumerate(self.nodes):
            for i, port in enumerate(self.ports):
                this_color = self._pdat['colors'][j][i]
                this_ant = self._pdat['ants'][j][i]
                if this_ant[0] != '-':
                    plt.plot(port+data_offset[0], node+data_offset[1], symbol, color=this_color)
                if show_text:
                    weight = 'extra bold'
                    if force_text:
                        weight = 'normal'
                        this_color = force_text
                    plt.text(port - self._xoffset(this_ant), node - 0.25, this_ant, color=this_color, weight=weight)
        if newfig:
            if self.add_colorbar:
                fig.colorbar(plt.cm.ScalarMappable(cmap=self.colormap, norm=self.norm))
            plt.xlabel('Node port')
            plt.ylabel('Node')
            plt.title(title)
            plt.xticks(self.ports, [str(x) for x in self.ports])
            plt.yticks(self.nodes, [str(x) for x in self.nodes])
            for x in [3.5, 6.5, 9.5]:
                plt.plot([x, x], [-1, 30], '--', color='.7')
            plt.axis([0.2, 13, 0, 22.8])

    def make(self):
        self._pdat = {'ants': [], 'colors': []}
        with mc.MCSessionWrapper(session=None) as session:
            hookup = cm_hookup.Hookup(session)
            ant_hudict = hookup.get_hookup(hpn='H')
            nbp_hudict = hookup.get_hookup(hpn='NBP')
            for this_node in self.nodes:
                nbp = f"NBP{this_node:02d}"
                key = f"{nbp}:A"
                this_row_ants = []
                this_row_colors = []
                for this_port in self.ports:
                    this_input = f"{this_node}-{this_port}"
                    polport = f'E<e{this_port}'
                    hu_from_nbp = nbp_hudict[key].hookup[polport]
                    this_antenna = -1
                    if not len(hu_from_nbp):
                        # print(f"{this_node},{this_port} found no hookup")
                        antenna = '!H---'
                    else:
                        ant_from_nbp = hu_from_nbp[0].upstream_part
                        if ant_from_nbp[0] != 'H':  # This likely just means not connected.
                            # print("WARNING - found non-antenna")
                            # print(f"\tTrying {this_node}-{this_port}")
                            # print(f"\tFound {ant_from_nbp}")
                            antenna = '!A---'
                        else:
                            antenna = ant_from_nbp
                            this_antenna = int(antenna[2:])
                    if this_antenna >= 0:
                        self.antenna_tracker.setdefault(antenna, [])
                        self.antenna_tracker[antenna].append(this_input)
                        antkey = f"{antenna}:A"
                        hu_from_ant = ant_hudict[antkey].hookup['E<ground']
                        node_from_ant = int(hu_from_ant[3].downstream_part[3:])
                        port_from_ant = int(hu_from_ant[3].downstream_input_port[1:])
                        if not (node_from_ant == this_node):
                            print("WARNING - nodes don't match!")
                            print(f"\tAntenna {antenna}")
                            print(f"\tTrying {this_node}-{this_port}")
                            print(f"\tFound {node_from_ant}-{port_from_ant}")
                            antenna = f"!N{antenna[2:]}"
                        if not (port_from_ant == this_port):  # This likely just means not connected.
                            # print("WARNING - ports don't match!")
                            # print(f"\tAntenna {antenna}")
                            # print(f"\tTrying {this_node}-{this_port}")
                            # print(f"\tFound {node_from_ant}-{port_from_ant}")
                            antenna = '!P---'
                    this_color = self.background
                    if this_antenna in self.antennas:
                        this_color = self.antennas[this_antenna]
                    elif this_input in self.inputs:
                        this_color = self.inputs[this_input]
                    if antenna[0] == '!':
                        this_color = self._special_color(antenna[1])
                    this_row_ants.append(antenna[2:])
                    this_row_colors.append(this_color)
                self._pdat['ants'].append(this_row_ants)
                self._pdat['colors'].append(this_row_colors)
 
    
    def check(self, color='r'):
        """This is probably not needed, likely relates to bug in hera_mc"""
        for antenna, inputs in self.antenna_tracker.items():
            if len(inputs) > 1:
                print("WARNING - found multiple ports for antenna!")
                print(f"\tAntenna {antenna}")
                print(f"\tInputs {', '.join(inputs)}")
                for this_input in inputs:
                    this_node, this_port = int(this_input.split('-')[0]), int(this_input.split('-')[1])
                    plt.text(this_port - self._xoffset(antenna)+0.03, this_node - 0.25, antenna[2:], color=color, weight='extra bold')

    def _special_color(self, val):
        if val == 'H':  # Didn't find a hookup
            return '0.5'
        if val == 'A':  # Didn't find an antenna
            return 'm'
        return 'r'  # Other problem

    def _xoffset(self, antenna):
        """Offset so that the numbers line-up."""
        if antenna[0] == '!':
            return 0.15
        if len(antenna) == 3:
            return 0.2
        if len(antenna) == 2:
            return 0.15
        return 0.1