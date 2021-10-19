#! /usr/bin/env python
import sys
from hera_cm import signal_chain
hera = signal_chain.Update(sys.argv[0], chmod=True)

hera.update_connection('stop', ['NCM04', 'A', 'rack'], ['N04', 'A', 'middle'], '2021/10/16', '10:00')  # noqa
hera.update_connection('add', ['NCM21', 'A', 'rack'], ['N04', 'A', 'middle'], '2021/10/16', '11:00')  # noqa

hera.done()
