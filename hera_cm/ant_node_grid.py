#! /usr/bin/env python
from hera_mc import cm_hookup, mc, geo_sysdef
import matplotlib.pyplot as plt
from copy import copy
from matplotlib import colors
import yaml


NODES = list(range(30))
PORTS = list(range(1, 13))
# Default colors
BACKGROUND_COLOR = 'k'
HIGHLIGHT_COLOR = 'orange'
ASSIGNED_COLOR = 'r'
REASSIGNED_COLOR = 'm'
NODE_INFO = geo_sysdef.read_nodes()
STATUS = {
    0: {'msg': 'ok', 'color': 'k'},
    1: {'msg': "undetermined", 'color': '0.5'},
    2: {'msg': "hookup not found via node port", 'color': 'b'},
    3: {'msg': "antenna not found from node port", 'color': 'm'},
    4: {'msg': "nodes don't match", 'color': 'g'},
    5: {'msg': "ports don't match", 'color': 'c'},
    6: {'msg': "couldn't find ant number", 'color': 'orange'},
    7: {'msg': "no-length hookup", 'color': 'purple'},
    8: {'msg': "invalid-length hookup", 'color': 'moccasin'}
}
OK = [0]
NOT_OK = [1,2,3,4,5,6,7,8]


def slim_component(component):
    return f"{component.upstream_part}:{component.upstream_output_port}>{component.downstream_part}:{component.downstream_input_port}"

class TableEntry:
    def __init__(self, node, port, hookup):
        self.node = node
        self.port = port
        self.hookup = hookup
        self.disabled = False
        self.status = 1
        self.assign = False
        self.reassign = False
        for init in ['hpn', 'number', 'cm_node', 'cm_port', 'assigned_node', 'value']:
            setattr(self, init, None)
        if self.hookup is None:
            self.status = 2
        elif not len(self.hookup):
            self.status = 7
        elif len(self.hookup) != 7:
            self.status = 8
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
        s = f"HPN: {self.hpn} -- "
        s+= f"Number: {self.number} -- "
        s+= f"Node-Port: {self.node}-{self.port}\n"
        s+= f"Status: {self.status}  ({STATUS[self.status]['msg']})\n"
        if self.status:
            s+= f"CM node-port:  {self.cm_node}-{self.cm_port}\n"
        if self.assigned is not None:
            s+= f"Assigned: {self.assigned}\n"
        if self.value is not None:
            s+= f"Value: {self.value}\n"
        s+= f"Display color: {self.display_color}\n"
        return s

    def check_node(self, error_on_node_mismatch=False):
        # Check for node mismatches
        if self.cm_node != self.node:
            print(f"Node mismatch in CM: {self.cm_node} != {self.node}")
            self.status = 4
            if error_on_node_mismatch:
                raise ValueError(f"Node mismatch in CM: {self.cm_node} != {self.node}")
        if self.assigned_node != self.node:
            print(f"Node mismatch in ASSIGN: {self.assigned_node} != {self.node}")
            self.status = 4
            if error_on_node_mismatch:
                raise ValueError(f"Node mismatch in ASSIGN: {self.assigned_node} != {self.node}")
        if self.cm_port != self.port:
            print(f"Port mismatch in CM: {self.cm_port} != {self.port}")
            self.status = 5

    def set_status_colors(self, bg=BACKGROUND_COLOR):
        """
        There are 4 signal attributes:
            display_color : color to be used for display (can be overridden for highlights)
            bg_color : background color to use if no status or highlight
            status_color : color based on status
            highlight_color : color based on highlight
        The display_color is set to bg_color initially, then can be overridden by status_color
        or highlight_color as needed.

        """
        self.bg_color = copy(bg)
        self.status_color = STATUS[self.status]['color']
        self.display_color = copy(bg)  # default to background

    def set_text(self):
        if self.number is not None:
            self.text = f"{self.number}"
        else:
            self.text = '---'

    def check_assignment(self, anum):
        if self.number is None:
            self.assign = True
            if anum < 0:
                self.assign = False
                return False
                raise ValueError("No antenna number to assign to.")
            else:
                print(f"Assigning {self.node:02d}-{self.port:02d} to {anum}")
        else:
            if self.number == anum:
                return False
            self.reassign = True
            print(f"Reassigning {self.node:02d}-{self.port:02d}:  {self.number} to {anum}")
            print("Probably should error...")
            if anum < 0:
                raise ValueError("No antenna number to reassign.")
        self.text = str(anum)
        self.number = int(anum)
        return True

class Grid:
    def __init__(self, highlight={}, nodes=NODES, ports=PORTS, disabled_nodes=[0],
                 background=BACKGROUND_COLOR, minval=None, maxval=None):
        self.set_highlight(highlight, minval=minval, maxval=maxval)
        self.nodes = nodes
        self.ports = ports
        self.disabled_nodes = disabled_nodes
        self.background = background
        self.ant_to_port = {}
        self.add_colorbar = False
        # Read in assigned nodes from NODE_INFO
        self.assigned_nodes = {}
        self.assigned_ants = {}
        for node in self.nodes:
            self.assigned_nodes[node] = copy(NODE_INFO[node]['ants'])
            for ant in NODE_INFO[node]['ants']:
                self.assigned_ants[ant] = node

    def show(self, entry, port=None):
        """
        Show information about a specific entry.
        
        Parameters
        ----------
        entry : int, tuple
            If int - antenna number; if tuple - (node, port)
        port : int, optional
            If entry is antenna number, port can be provided to avoid lookup.

        """
        key = self.get_key(entry)
        if isinstance(key, (tuple, list)):
            node, port = key
        if port is None:
            node, port = self.ant_to_port[key]
        print(self.table[node][port], end='')
        print("Hookup:", end='')
        if self.table[node][port].hookup is None:
            print("\t<none>")
        else:
            components = [f"{slim_component(component)}" for component in self.table[node][port].hookup]
            print(f"\t{','.join(components)}")

    def get_key(self, key):
        """Convert key to int or (int, int) tuple."""
        if isinstance(key, str):
            try:
                key = int(key)
            except ValueError:
                try:
                    node, port = key.split(':')
                    key = (int(node), int(port))
                except ValueError:
                    pass
        return key

    def set_highlight(self, highlight, minval=None, maxval=None, default_color='r'):
        """
        Parameter
        ---------
        highlight : str, dict, list
            If str - csv-antennas, csv-inputs(node:port), yaml filename
            If dict-of-int-keys, antennas; dict-of-str, node:port
        minval : float, optional
            Minimum value for colormap normalization (if applicable)
        maxval : float, optional
            Maximum value for colormap normalization (if applicable)
        default_color: str, optional
            Color to use for highlights if no value provided.

        Attribute
        ---------
        highlight : dict
            Dictionary of highlight entries:
            {key: {'value': value, 'color': color}, ...}
        """
        self.highlight = {}
        if isinstance(highlight, str):
            try:
                with open(highlight, 'r') as fp:
                    highlight = yaml.safe_load(fp)
            except FileNotFoundError:
                highlight = highlight.split(',')

        try:
            with open('colors.yaml', 'r') as fc:
                self.hl_color_map = yaml.safe_load(fc)
        except FileNotFoundError:
            self.hl_color_map = {}

        has_a_float = []
        if isinstance(highlight, dict):            
            # Make sure keys are either int or tuple-of-int (node, port)
            minfloat = 1E6
            maxfloat = -1E6
            for key, value in highlight.items():
                key = self.get_key(key)
                self.highlight[key] = {'value': value, 'color': value}
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
                self.highlight[key] = {'value': default_color, 'color': default_color}

        if len(has_a_float):
            self.add_colorbar = True
            self.colormap = plt.cm.rainbow
            minval = minfloat if minval is None else minval
            maxval = maxfloat if maxval is None else maxval
            self.norm = colors.Normalize(vmin=minval, vmax=maxval)
            for key in has_a_float:
                self.highlight[key]['color'] = self.colormap(float(self.norm(highlight[key])))

        self.highlight_codes = {}
        for key in self.highlight:
            self.highlight_codes[self.highlight[key]['color']] = str(key)

    def addplot(self, title=None, marker=',', markersize=None, markeroffset=[0.0, 0.0], parameter='text', colors=None):
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
            if self.add_colorbar:
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
            if colors is not None:
                fig = plt.figure('colors')
                self.axc = fig.subplots()
            if colors == 'status':
                for status_code, status_info in STATUS.items():
                    self.axc.plot([0, 1], [status_code, status_code], '-', color=status_info['color'], lw=10, label=f"{status_code}: {status_info['msg']}")
                self.axc.set_yticks(list(STATUS.keys()), [f"{key}: {STATUS[key]['msg']}" for key in STATUS.keys()])
                self.axc.set_title('Status color legend')
            elif colors == 'highlight':
                for i, (hl_color, hl_info) in enumerate(self.hl_color_map.items()):
                    self.axc.plot([0, 1], [i, i], '-', color=hl_color, lw=10, label=f"{hl_info}")
                self.axc.set_yticks(list(range(len(self.hl_color_map))), list(self.hl_color_map.values()))
                self.axc.set_title('Highlight color legend')

    def _check_duplicates(self, note):
        tabant = []
        for node in self.nodes:
            for port in self.ports:
                antnum = self.table[node][port].number
                if antnum is None:
                    continue
                if antnum in tabant:
                    print(f"{note}: Duplicate antenna found:  Antenna {antnum} at Node {node} Port {port}")
                tabant.append(antnum)

    def process_array(self):
        # Check for duplicate antennas before.
        self._check_duplicates("BEFORE")
        # Check against ok nodes/ports.
        available_node_ports = {}
        for node in self.nodes:
            available_node_ports[node] = copy(self.assigned_nodes[node])
            for port in self.ports:
                if self.table[node][port].status in OK:
                    available_node_ports[node].remove(self.table[node][port].number)
        # Arbitrarily assign remainder and update ant_to_port map.
        for node in self.nodes:
            for port in self.ports:
                if self.table[node][port].status in OK:
                    continue
                try:
                    # print(node, available_node_ports[node])
                    this_trial = available_node_ports[node][0]
                except IndexError:
                    this_trial = -1
                updated = self.table[node][port].check_assignment(this_trial)
                if updated:
                    self.ant_to_port[self.table[node][port].number] = (node, port)
                    available_node_ports[node].remove(this_trial)
        # Set disabled node antennas.
        for disabled_node in self.disabled_nodes:
            if disabled_node in self.table:
                for port in self.ports:
                    self.table[disabled_node][port].disabled = True
        # Check for duplicate antennas after.
        self._check_duplicates("AFTER")

    def set_display_color(self, show_status=False, show_misassigned=False, show_disabled=False):
        """
        Will reset display_color based to highlight.  If ingnore_status is True only background and highlight
        colors will be used.  Otherwise bg -> status -> highlight.

        """
        for node in self.nodes:
            for port in self.ports:
                if show_status:
                    self.table[node][port].display_color = copy(self.table[node][port].status_color)
                if show_misassigned and self.table[node][port].assign:
                    self.table[node][port].display_color = ASSIGNED_COLOR
                if show_misassigned and self.table[node][port].reassign:
                    self.table[node][port].display_color = REASSIGNED_COLOR
                if show_disabled and self.table[node][port].disabled:
                    self.table[node][port].display_color = '0.8'
        for i, key in enumerate(self.highlight):
            hlkey = self.get_key(key)
            if isinstance(hlkey, int):
                try:
                    this_node, this_port = self.ant_to_port[hlkey]
                except KeyError:
                    continue
            self.table[this_node][this_port].display_color = self.highlight[key]['color']
            self.table[this_node][this_port].value = self.highlight[key]['value']


    def print_all(self):
        sorted_table = {}
        for node in self.nodes:
            for port in self.ports:
                key = self.table[node][port].number
                if key is not None:
                    sorted_table[key] = (node, port)
        for key in sorted(sorted_table.keys()):
            node, port = sorted_table[key]
            if self.table[node][port].number is not None:
                self.show((node, port))
                print("-----------------------------------")

    def get_connected(self, verbose=True, error_on_node_mismatch=True):
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
                    # CM will sometimes have wrong hookup for a node port and need to check.
                    if hu_from_nbp is not None:
                        try:
                            nbp_port = int(hu_from_nbp[3].downstream_input_port[1:])
                            if nbp_port != this_port:
                                hu_from_nbp = None
                        except (IndexError, ValueError):
                            pass
                    this_entry = TableEntry(this_node, this_port, hu_from_nbp)
                    # Process found antennas
                    hu_from_ant = []
                    if this_entry.number is not None:
                        antkey = f"{this_entry.hpn}:A"
                        hu_from_ant = ant_hudict[antkey].hookup['E<ground']
                        this_entry.cm_node = int(hu_from_ant[3].downstream_part[3:])
                        this_entry.cm_port = int(hu_from_ant[3].downstream_input_port[1:])
                        this_entry.assigned_node = self.assigned_ants.get(this_entry.number, None)
                        this_entry.check_node(error_on_node_mismatch)
                        self.ant_to_port[this_entry.number] = (this_node, this_port)
                    this_entry.set_text()
                    this_entry.set_status_colors(self.background)
                    self.table[this_node][this_port] = this_entry
                    if verbose:
                        if this_entry.status in NOT_OK and this_node not in self.disabled_nodes:
                            lenhu = 0 if hu_from_nbp is None else len(hu_from_nbp)
                            antno = f"{this_entry.number:<03d}" if this_entry.number is not None else '---'
                            print(f"Node {this_node:02d} Port {this_port:02d} Ant {antno}. Status {this_entry.status}:", end=' ')
                            print(f"{STATUS[this_entry.status]['msg']} ({lenhu} / {len(hu_from_ant)})")

