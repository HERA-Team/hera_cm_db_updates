#! /usr/bin/env python
import argparse
from hera_mc import cm_active, mc, cm_hookup, cm_utils
from copy import copy

ap = argparse.ArgumentParser()
ap.add_argument('--header-term', dest='header_term',
                help="Part info header to track.", default='H6C')
args = ap.parse_args()


data = {}


with mc.MCSessionWrapper() as session:
    active = cm_active.ActiveData(session)
    active.load_info()
    if len(active.info):
        hookup = cm_hookup.Hookup(session)
        hu = hookup.get_hookup_from_db('HH', 'all', 'now')
        for part, information in active.info.items():
            for note in information:
                if note.comment.lower().startswith(args.header_term.lower()):
                    try:
                        note.node = f"{hu[part].hookup['E<ground'][-1].downstream_part:<3s}"
                    except KeyError:
                        note.node = '-x-'
                    data[f"{note.posting_gpstime}{part}"] = copy(note)

        for out in sorted(data.keys()):
            popart = data[out].hpn.split(':')[0]
            aptime = cm_utils.get_astropytime(data[out].posting_gpstime, float_format='gps')
            potime = aptime.datetime.strftime("%Y-%m-%d")
            print(f"{popart}    {data[out].node}   {potime}")
