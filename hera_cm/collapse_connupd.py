#! /usr/bin/env python
"""
Pulls the connupd information out of the add_part_conn script files.

Writes the file 'cc_yymmdd_connupd_hhmm'
"""
import os
import datetime
import argparse
from hera_cm import util, script_info


class CollapseConn:
    def __init__(self):
        self.connupd_files = {}
        files = os.listdir()
        for f in sorted(files):
            if 'connupd' in f:
                parts = f.split('_')
                dtstr = f"{parts[0]}T{parts[2]}"
                dt = datetime.datetime.strptime(dtstr, '%y%m%dT%H%M')
                self.connupd_files[dt] = f

    def read_files(self):
        self.other = set()
        self.cmds = {}
        for ufile in self.connupd_files.values():
            with open(ufile, 'r') as fp:
                for line in fp:
                    if line.startswith('#') or line.startswith('source') or line.startswith('echo'):
                        self.other.add(line.strip())
                    else:
                        cmd, arg = util.parse_log_line(line, return_cmd_args=True)
                        self.cmds.setdefault(cmd, {})
                        arglist = script_info.get_arglist(arg)
                        key = []
                        for targ in arglist:
                            val = getattr(arg, targ)
                            if targ not in ['date', 'time'] and isinstance(getattr(arg, targ), str):
                                key.append(getattr(arg, targ))
                        key = ','.join(sorted(key))
                        self.cmds[cmd].setdefault(key, {})
                        vdate = getattr(arg, 'date')
                        vtime = getattr(arg, 'time')
                        datekey = datetime.datetime.strptime(f"{vdate}T{vtime}", "%Y/%m/%dT%H:%M")
                        self.cmds[cmd][key][datekey] =  line.strip()

    def write_cc_file(self, cmds=['add_part', 'stop_connection', 'add_connection']):
        now = datetime.datetime.now()
        fn = f"cc{now.strftime('%y%m%d')}_connupd_{now.strftime('%H%M')}"
        with open(fn, 'w') as fp:
            print(f"Writing {fn}")
            print("#! /bin/bash", file=fp)
            print("source ~/.bashrc", file=fp)
            print(f"echo {fn} >> scripts.log", file=fp)
            for cmd in cmds:
                print(f"# {cmd}", file=fp)
                for entry in self.cmds[cmd]:
                    early = min(self.cmds[cmd][entry])
                    print(f"{self.cmds[cmd][entry][early]}", file=fp)
