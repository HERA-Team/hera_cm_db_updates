#! /usr/bin/env python
from hera_mc import cm_hookup, mc, geo_sysdef
import matplotlib.pyplot as plt
from copy import copy
from matplotlib import colors
import yaml


NODES = list(range(30))
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
        s = f"HPN: {self.hpn}\nNode-Port: {self.node}-{self.port}\nStatus: {self.status}  ({STATUS[self.status]['msg']})\n"
        if self.status:
            s+= f"CM node-port:  {self.cm_node}-{self.cm_port}\n"
        if self.assigned is not None:
            s+= f"Assigned: {self.assigned}\n"
        if self.value is not None:
            s+= f"Value: {self.value}\n"
        s+= f"Color: {self.color}\nDisplay: {self.display_color}\n"
        s+= '-----------------------------------'
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

    def set_as_assigned(self, anum):
        if self.number is not None:
            print(f"Reassigning {self.node:02d}-{self.port:02d}:  {self.number} to {anum}")
        else:
            print(f"Assigning   {self.node:02d}-{self.port:02d}:  {anum}")
        self.assigned = anum
        self.display_color = 'moccasin'
        self.text = str(anum)
        self.number = anum

class Grid:
    def __init__(self, highlight={}, nodes=NODES, ports=PORTS, background=BKCLR, minval=None, maxval=None):
        self.set_highlight(highlight, minval=minval, maxval=maxval)
        self.nodes = nodes
        self.ports = ports
        self.background = background
        self.ant_to_entry = {}

    def show_hookup(self, node, port):
        for component in self.table[node][port].hookup:
            print(component)
        print()

    def _get_key(self, key):
        if isinstance(key, (int, tuple)):
            return key
        try:
            node, port = key.split(':')
            key = (int(node), int(port))
        except ValueError:
            key = int(key)
        return key

    def set_highlight(self, highlight, minval, maxval, highlight_color='r'):
        """
        Parameter
        ---------
        highlight : str, dict, list
            If str - csv-antennas, csv-inputs(node:port), yaml filename
            If dict-of-int-keys, antennas; dict-of-str, node:port
        """
        self.add_colorbar = False
        self.highlight = {}
        if isinstance(highlight, str):
            try:
                with open(highlight, 'r') as fp:
                    highlight = yaml.safe_load(fp)
            except FileNotFoundError:
                highlight = highlight.split(',')

        if isinstance(highlight, dict):
            # Make sure keys are either int or tuple-of-int (node, port)
            has_a_float = []
            minfloat = 1E6
            maxfloat = -1E6
            for key, value in highlight.items():
                key = self._get_key(key)
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
            if not len(has_a_float):
                return
        elif isinstance(highlight, list):
            for key in highlight:
                key = self._get_key(key)
                self.highlight[key]['value'] = highlight_color
                self.highlight[key]['color'] = highlight_color
            return

        # Is a dict with floats in it
        self.colormap = plt.cm.rainbow
        self.add_colorbar = True
        minval = minfloat if minval is None else minval
        maxval = maxfloat if maxval is None else maxval
        self.norm = colors.Normalize(vmin=minval, vmax=maxval)
        for key in has_a_float:
            self.highlight[key]['color'] = self.colormap(float(self.norm(highlight[key])))


    def addplot(self, title=None, marker=',', markersize=None, force_text=False, show_text=True, parameter='text'):
        newfig = title is not None
        if newfig:
            fig = plt.figure(title, figsize=(9.75,6.5))
        for node in self.nodes:
            for port in self.ports:
                this_color = self.table[node][port].display_color
                this_text = str(getattr(self.table[node][port], parameter))
                plt.plot(port, node, marker, markersize=markersize, color=this_color)
                if show_text:
                    weight = 'extra bold'
                    if force_text:
                        weight = 'normal'
                        this_color = force_text
                    x = port - self._xtxt_offset(this_text)
                    y = node - 0.25
                    plt.text(x, y, this_text, color=this_color, weight=weight)
        if newfig:
            if self.add_colorbar:
                print("ANG185: colorbar errors out")
                # fig.colorbar(plt.cm.ScalarMappable(cmap=self.colormap, norm=self.norm))
            plt.xlabel('Node input port (snap input order)')
            plt.ylabel('Node number')
            plt.title(title)
            plt.xticks(self.ports, [str(x) for x in self.ports])
            plt.yticks(self.nodes, [str(x) for x in self.nodes])
            xmin, xmax = min(self.ports)-0.5, max(self.ports)+0.5
            ymin, ymax = min(self.nodes)-0.7, max(self.nodes)+2.2
            for x in [3.5, 6.5, 9.5]:
                plt.plot([x, x], [ymin, ymax], '--', color='0.7')
            plt.plot([xmin, xmax], [ymax-1.35, ymax-1.35], '--', color='0.7')
            plt.axis([xmin, xmax, ymin, ymax])
            for i in range(4):
                plt.text(1.5 + i*3, ymax-1.0, f'SNAP {i}')

    def process_status(self):
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
                        self.table[node][port].set_as_assigned(assigned_nodes[node].pop(0))
                    except IndexError:
                        pass
        if 0 in self.table:
            print("Setting node 0 color to light-grey")
            for port in self.ports:
                self.table[0][port].display_color = '0.8'

    def get_connected(self):  # was make
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
                    if this_entry.number in self.highlight:
                        this_entry.display_color = self.highlight[this_entry.number]['color']
                        this_entry.value = self.highlight[this_entry.number]['value']
                    elif (this_node, this_port) in self.highlight:
                        this_entry.display_color = self.highlight[(this_node, this_port)]['color']
                        this_entry.value = self.highlight[(this_node, this_port)]['value']
                    self.table[this_node][this_port] = this_entry
        self.process_status()

    def _xtxt_offset(self, antenna):
        """Offset so that the numbers line-up."""
        if antenna[0] == '-':
            return 0.15
        if len(antenna) == 3:
            return 0.2
        if len(antenna) == 2:
            return 0.15
        return 0.1