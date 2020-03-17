#! /usr/bin/env python
"""Fix some FEMs."""
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)

hera.stop_active_connections('FEM059', cdate='2020/03/10')
hera.stop_active_connections('FEM046', cdate='2020/03/10')
hera.stop_active_connections('FEM164', cdate='2020/02/18')
hera.done()
print("\n!!! NOW EDIT {} !!!".format(hera.output_script))
