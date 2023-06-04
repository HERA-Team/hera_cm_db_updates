#! /usr/bin/env python
from hera_mc import cm_hookup, mc
import matplotlib.pyplot as plt
import yaml


NODES = list(range(1, 23))
PORTS = list(range(1, 13))
BKCLR = 'k'

class Grid:
    def __init__(self, data={}, nodes=NODES, ports=PORTS, background=BKCLR):
        if isinstance(data, str):
            with open(data, 'r') as fp:
                data = yaml.safe_load(fp)
        self.antennas = {}
        self.inputs = {}
        self.nodes = nodes
        self.ports = ports
        self.background = background
        for param in ['nodes', 'ports', 'background', 'antennas', 'inputs']:
            if param in data:
                setattr(self, param, data[param])
        self.antenna_tracker = {}

    def show(self, hu):
        for component in hu:
            print(component, end='')
        print()

    def make(self):
        plt.figure(figsize=(9.75,6.5))
        with mc.MCSessionWrapper(session=None) as session:
            hookup = cm_hookup.Hookup(session)
            ant_hudict = hookup.get_hookup(hpn='H')
            nbp_hudict = hookup.get_hookup(hpn='NBP')
            for this_node in self.nodes:
                nbp = f"NBP{this_node:02d}"
                key = f"{nbp}:A"
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
                        if ant_from_nbp[0] != 'H':  #This is probably ok, bug in hera_mc
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
                        # if not (port_from_ant == this_port):  #This is probably ok, bug in hera_mc
                            # print("WARNING - ports don't match!")
                            # print(f"\tAntenna {antenna}")
                            # print(f"\tTrying {this_node}-{this_port}")
                            # print(f"\tFound {node_from_ant}-{port_from_ant}")
                            # antenna = f"!P{antenna[2:]}"
                    this_color = self.background
                    if this_antenna in self.antennas:
                        this_color = self.antennas[this_antenna]
                    elif this_input in self.inputs:
                        this_color = self.inputs[this_input]
                    if antenna[0] == '!':
                        this_color = self._special_color(antenna[1])
                    plt.plot(this_port, this_node, ',', color=this_color)
                    plt.text(this_port - self._xoffset(antenna), this_node - 0.25, antenna[2:], color=this_color)
        plt.xlabel('Node port')
        plt.ylabel('Node')
        plt.title('Node Input/Antenna Map')
        plt.xticks(self.ports, [str(x) for x in self.ports])
        plt.yticks(self.nodes, [str(x) for x in self.nodes])
        for x in [3.5, 6.5, 9.5]:
            plt.plot([x, x], [-1, 30], '--', color='.7')
        plt.axis([0.2, 13, 0, 22.8])
    
    def check(self, color='r'):
        """This is probably not needed, likely relates to bug in hera_mc"""
        for antenna, inputs in self.antenna_tracker.items():
            if len(inputs) > 1:
                print("WARNING - found multiple ports for antenna!")
                print(f"\tAntenna {antenna}")
                print(f"\tInputs {', '.join(inputs)}")
                for this_input in inputs:
                    this_node, this_port = int(this_input.split('-')[0]), int(this_input.split('-')[1])
                    plt.text(this_port - self._xoffset(antenna)+0.03, this_node - 0.25, antenna[2:], color=color)

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
        if len(antenna) == 3+2:
            return 0.2
        if len(antenna) == 2+2:
            return 0.15
        return 0.1