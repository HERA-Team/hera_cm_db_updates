#! /usr/bin/env python
from hera_mc import cm_hookup, mc
import matplotlib.pyplot as plt
import argparse

node_map_colors = [
    '#,1,2,3,4,5,6,7,8,9,10,11,12',
    '1,k,k,k,k,k,k,k,k,k,k,k,k',
    '2,k,k,k,k,k,k,k,k,k,k,k,k',
    '3,k,k,k,k,k,k,k,k,k,k,k,k',
    '4,k,k,k,k,k,k,k,k,k,k,k,k',
    '5,k,k,k,k,k,k,k,k,k,k,k,k',
    '6,k,k,k,k,k,k,k,k,k,k,k,k',
    '7,k,k,k,k,k,k,k,k,k,k,k,k',
    '8,k,k,k,k,k,k,k,k,k,k,k,k',
    '9,k,k,k,k,k,k,k,k,k,k,k,k',
    '10,k,k,k,k,k,k,k,k,k,k,k,k',
    '11,k,k,k,k,k,k,k,k,k,k,k,k',
    '12,k,k,k,k,k,k,k,k,k,k,k,k',
    '13,k,k,k,k,k,k,k,k,k,k,k,k',
    '14,k,k,k,k,k,k,k,k,k,k,k,k',
    '15,k,k,k,k,k,k,k,k,k,k,k,k',
    '16,k,k,k,k,k,k,k,k,k,k,k,k',
    '17,k,k,k,k,k,k,k,k,k,k,k,k',
    '18,k,k,k,k,k,k,k,k,k,k,k,k',
    '19,k,k,k,k,k,k,k,k,k,k,k,k',
    '20,k,k,k,k,k,k,k,k,k,k,k,k',
    '21,k,k,k,k,k,k,k,k,k,k,k,k',
    '22,k,k,k,k,k,k,k,k,k,k,k,k'   
]


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-a', '--antenna', help="List of antennas to highnmclr", default='')
    ap.add_argument('--highlight-color', dest='highlight_color', help="Color to use to highlight above", default='r')
    args = ap.parse_args()
    args.antenna = args.antenna.split(',')
else:
    args = argparse.Namespace(antenna=[], highlight_color='r')

xticks = []
yticks = []
plt.figure(figsize=(9.75,6.5))
with mc.MCSessionWrapper(session=None) as session:
    hookup = cm_hookup.Hookup(session)
    ant_hudict = hookup.get_hookup(hpn='H')
    hookup_dict = hookup.get_hookup(hpn='NBP')
    for line in node_map_colors:
        if line.startswith('#'):
            for val in line.split(',')[1:]:
                xticks.append(int(val))
            continue
        nm_colors = line.strip().split(',')
        node = int(nm_colors[0])
        yticks.append(node)
        nbp = f"NBP{node:02d}"
        key = f"{nbp}:A"
        print(f"\r{node}", end='   ')
        for i, nmclr in enumerate(nm_colors[1:]):
            this_port = i + 1
            polport = f'E<e{this_port}'
            try:
                antenna = hookup_dict[key].hookup[polport][0].upstream_part
                antkey = f"{antenna}:A"
                port_is_ok = int(ant_hudict[antkey].hookup['E<ground'][3].downstream_input_port[1:]) == this_port
            except IndexError:
                port_is_ok = False
            if not port_is_ok:
                antenna = '-----'
                print(f"\rNot connected to an antenna:  {node}:{this_port}")
            plt.plot(this_port, node, ',', color=nmclr)
            antno = -1 if antenna.startswith('-') else int(antenna[2:])
            this_color = args.highlight_color if str(antno) in args.antenna else nmclr
            if antno < 0:
                xoffset = 0.15
            elif  antno > 99:
                xoffset = 0.2
            elif antno > 9:
                xoffset = 0.15
            else:
                xoffset = 0.1
            plt.text(this_port - xoffset, node - 0.25, antenna[2:], color=this_color)
plt.xlabel('Node port')
plt.ylabel('Node')
plt.title('Node Input/Antenna Map')
plt.xticks(xticks, [str(x) for x in xticks])
plt.yticks(yticks, [str(x) for x in yticks])
for x in [3.5, 6.5, 9.5]:
    plt.plot([x, x], [-1, 30], '--', color='.7')
plt.axis([0.2, 13, 0, 22.8])
plt.show()
