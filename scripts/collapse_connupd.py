#! /usr/bin/env python
"""
Pulls the connupd information out of the add_part_conn script files.

"""

from hera_cm import collapse_connupd

cc = collapse_connupd.CollapseConn()
cc.read_files()
cc.write_cc_file()
