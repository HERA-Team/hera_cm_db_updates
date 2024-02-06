#! /usr/bin/env python
from hera_mc import cm_hookup, mc, geo_sysdef
import matplotlib.pyplot as plt
from copy import copy
from matplotlib import colors
import yaml


NODES = list(range(24))
PORTS = list(range(1, 13))
BKCLR = 'k'
NODE_INFO = geo_sysdef.read_nodes()
STATUS = {
    0: {'msg': 'ok', 'color': 'k'},
    1: {'msg': "undetermined", 'color': '0.5'},
    2: {'msg': "hookup not found via node port", 'color': 'b'},
    3: {'msg': "antenna not found from node port", 'color': 'm'},
    4: {'msg': "nodes don't match", 'color': 'r'},
    5: {'msg': "ports don't match", 'color': 'c'},
    6: {'msg': "couldn't find ant number", 'color': 'y'}
}
OK = [0]

class TableEntry:
    def __init__(self, node, port, hookup):
        self.node = node
        self.port = port
        self.hookup = hookup
        self.status = 1
        for init in ['hpn', 'number', 'cm_node', 'cm_port', 'assigned', 'value']:
            setattr(self, init, None)
        if self.hookup is None:
            self.status = 2
        else:
            self.hpn = self.hookup[0].upstream_part
            if self.hpn[0] != 'H':  # This likely just means not connected.
                self.status = 3
            else:
                try:
                    self.number = int(self.hpn[2:])
                    self.status = 0
                except ValueError:
                    self.number = None
                    self.status = 6

    def __repr__(self):
        s = f"HPN: {self.hpn}\n"
        s+= f"Number: {self.number}\n"
        s+= f"Node-Port: {self.node}-{self.port}\n"
        s+= f"Status: {self.status}  ({STATUS[self.status]['msg']})\n"
        if self.status:
            s+= f"CM node-port:  {self.cm_node}-{self.cm_port}\n"
        if self.assigned is not None:
            s+= f"Assigned: {self.assigned}\n"
        if self.value is not None:
            s+= f"Value: {self.value}\n"
        s+= f"Color: {self.color}\nDisplay color: {self.display_color}\n"
        return s

    def cm(self):
        if not (self.cm_node == self.node):
            self.status = 4
        if not (self.cm_port == self.port):  # This likely just means not connected.
            self.status = 5

    def set_color(self, bg):
        if self.status:
            self.color = STATUS[self.status]['color']
        else:
            self.color = bg
        self.display_color = copy(self.color)

    def set_text(self):
        if self.number is not None:
            self.text = f"{self.number}"
        else:
            self.text = '---'

    def set_as_assigned(self, anum, verbose=False):
        if verbose:
            if self.number is not None:
                print(f"Reassigning {self.node:02d}-{self.port:02d}:  {self.number} to {anum}")
            else:
                print(f"Assigning   {self.node:02d}-{self.port:02d}:  {anum}")
        self.assigned = anum
        self.color = 'moccasin'
        self.display_color = 'moccasin'
        self.text = str(anum)
        self.number = anum

class Grid:
    def __init__(self, highlight={}, nodes=NODES, ports=PORTS, background=BKCLR, minval=None, maxval=None):
        self.set_highlight(highlight, minval=minval, maxval=maxval)
        self.nodes = nodes
        self.ports = ports
        self.background = background
        self.ant_to_port = {}
        self.add_colorbar = False

    def show(self, entry, port=None):
        key = self.get_key(entry)
        if isinstance(key, (tuple, list)):
            node, port = key
        if port is None:
            node, port = self.ant_to_port[key]
        print(self.table[node][port], end='')
        print("Hookup:")
        for component in self.table[node][port].hookup:
            print(f"\t{component}")

    def get_key(self, key):
        if isinstance(key, (int, tuple, list)):
            return key
        try:
            node, port = key.split(':')
            key = (int(node), int(port))
        except ValueError:
            key = int(key)
        return key

    def set_highlight(self, highlight, minval=None, maxval=None, display_color='r'):
        """
        Parameter
        ---------
        highlight : str, dict, list
            If str - csv-antennas, csv-inputs(node:port), yaml filename
            If dict-of-int-keys, antennas; dict-of-str, node:port
        """
        self.highlight = {}
        if isinstance(highlight, str):
            try:
                with open(highlight, 'r') as fp:
                    highlight = yaml.safe_load(fp)
            except FileNotFoundError:
                highlight = highlight.split(',')

        has_a_float = []
        if isinstance(highlight, dict):            
            # Make sure keys are either int or tuple-of-int (node, port)
            minfloat = 1E6
            maxfloat = -1E6
            for key, value in highlight.items():
                key = self.get_key(key)
                self.highlight[key] = {'value': None, 'color': None}
                if isinstance(key, (int, tuple)):
                    self.highlight[key]['value'] = value
                    self.highlight[key]['color'] = value
                elif isinstance(key, str):
                    self.highlight[key]['value'] = value
                    self.highlight[key]['color'] = value
                try:
                    float_val = float(value)
                    has_a_float.append(key)
                    minfloat = float_val if float_val < minfloat else minfloat
                    maxfloat = float_val if float_val > maxfloat else maxfloat
                except (ValueError, TypeError):
                    continue
        elif isinstance(highlight, list):
            for key in highlight:
                key = self.get_key(key)
                self.highlight[key] = {'value': display_color, 'color': display_color}

        if len(has_a_float):
            self.add_colorbar = True
            self.colormap = plt.cm.rainbow
            minval = minfloat if minval is None else minval
            maxval = maxfloat if maxval is None else maxval
            self.norm = colors.Normalize(vmin=minval, vmax=maxval)
            for key in has_a_float:
                self.highlight[key]['color'] = self.colormap(float(self.norm(highlight[key])))


    def addplot(self, title=None, marker=',', markersize=None, markeroffset=[0.0, 0.0], parameter='text'):
        newfig = title is not None
        if newfig:
            fig = plt.figure(title, figsize=(9.75,6.5))
            self.ax = fig.subplots()
        for node in self.nodes:
            for port in self.ports:
                this_color = self.table[node][port].display_color
                this_text = str(getattr(self.table[node][port], parameter))
                x, y = port + markeroffset[0], node + markeroffset[1]
                self.ax.plot(x, y, marker, markersize=markersize, color=this_color)
                if marker == ',':
                    weight = 'extra bold'
                    x = port - (0.1 + 0.05 * (len(this_text) - 1.0))
                    y = node - 0.25
                    self.ax.text(x, y, this_text, color=this_color, weight=weight)
        if newfig:
            if self.add_colorbar is not None:
                fig.colorbar(plt.cm.ScalarMappable(cmap=self.colormap, norm=self.norm), ax=self.ax)
            self.ax.set_xlabel('Node input port (snap input order)')
            self.ax.set_ylabel('Node number')
            self.ax.set_title(title)
            self.ax.set_xticks(self.ports, [str(x) for x in self.ports])
            self.ax.set_yticks(self.nodes, [str(x) for x in self.nodes])
            xmin, xmax = min(self.ports)-0.5, max(self.ports)+0.5
            ymin, ymax = min(self.nodes)-0.7, max(self.nodes)+2.2
            for x in [3.5, 6.5, 9.5]:
                self.ax.plot([x, x], [ymin, ymax], '--', color='0.7')
            self.ax.plot([xmin, xmax], [ymax-1.35, ymax-1.35], '--', color='0.7')
            self.ax.axis([xmin, xmax, ymin, ymax])
            for i in range(4):
                self.ax.text(1.5 + i*3, ymax-1.0, f'SNAP {i}')

    def process_status(self, verbose=False):
        assigned_nodes = {}
        for node in self.nodes:
            assigned_nodes[node] = copy(NODE_INFO[node]['ants'])
            for port in self.ports:
                if self.table[node][port].status in OK:
                    assigned_nodes[node].remove(self.table[node][port].number)
        for node in self.nodes:
            for port in self.ports:
                if self.table[node][port].status:
                    try:
                        self.table[node][port].set_as_assigned(assigned_nodes[node].pop(0), verbose=verbose)
                    except IndexError:
                        pass
                self.ant_to_port[self.table[node][port].number] = (node, port)
        if 0 in self.table:
            print("Setting node 0 color to light-grey")
            for port in self.ports:
                self.table[0][port].display_color = '0.8'

    def get_connected(self, show_highlighted=False):
        """
        Parameter
        ---------
        show_highlighted : True, False, None, int
            if (None, False) don't print out highlighted entries
            if True print out all highlighted entries
            if int only print out int entries

        """
        if not show_highlighted:
            show_highlighted = 0
        elif show_highlighted == True:
            show_highlighted = 99
        
        self.found_antennas = []
        self.table = {}
        with mc.MCSessionWrapper(session=None) as session:
            hookup = cm_hookup.Hookup(session)
            ant_hudict = hookup.get_hookup(hpn='H')
            nbp_hudict = hookup.get_hookup(hpn='NBP')
            for this_node in self.nodes:
                self.table[this_node] = {}
                key = f"NBP{this_node:02d}:A"
                for this_port in self.ports:
                    # Get antenna from node port and provide status
                    try:
                        hu_from_nbp = nbp_hudict[key].hookup[f'E<e{this_port}']
                    except KeyError:
                        hu_from_nbp = None
                    this_entry = TableEntry(this_node, this_port, hu_from_nbp)
                    # Process found antennas
                    if this_entry.number is not None:
                        self.found_antennas.append(this_entry.number)
                        antkey = f"{this_entry.hpn}:A"
                        hu_from_ant = ant_hudict[antkey].hookup['E<ground']
                        this_entry.cm_node = int(hu_from_ant[3].downstream_part[3:])
                        this_entry.cm_port = int(hu_from_ant[3].downstream_input_port[1:])
                        this_entry.cm()
                    this_entry.set_text()
                    this_entry.set_color(self.background)
                    self.table[this_node][this_port] = this_entry
        self.process_status()
        # Process highlight
        not_found = []
        for i, key in enumerate(self.highlight):
            hlkey = self.get_key(key)
            if isinstance(hlkey, int):
                try:
                    this_node, this_port = self.ant_to_port[hlkey]
                except KeyError:
                    not_found.append(hlkey)
                    continue
            self.table[this_node][this_port].display_color = self.highlight[key]['color']
            self.table[this_node][this_port].value = self.highlight[key]['value']
            if i < show_highlighted:
                self.show(hlkey)
                print("-----------------------------------")
        if show_highlighted and show_highlighted < len(self.highlight):
            print("...")
        if len(not_found):
            print(f"Antennas not found:  {', '.join([str(x) for x in not_found])}")

