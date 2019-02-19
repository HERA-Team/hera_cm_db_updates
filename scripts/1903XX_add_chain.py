#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import sys
import signal_chain


hera = signal_chain.Chain(sys.argv[0])

hera.add(ant=0, feed=1, fem=2, pam=3, snap='A27', snap_input='e10,n8', cdate='2019/02/20')
