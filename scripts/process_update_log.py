#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Process the cm update log in redis."""

import argparse
from hera_cm import upd_connect

ap = argparse.ArgumentParser()
ap.add_argument('--alert', help="Email addresses for alerts.", default='heraops@reionization.org')
args = ap.parse_args()

if '@' in args.alert:
    args.alert = args.alert.split(',')
else:
    args.alert = None
script_type = 'no_signal_chain'
script_path = '.'
disable_err = True
verbose = False

if args.alert is not None:
    update = upd_connect.UpdateConnect(script_type=script_type, script_path=script_path,
                                       disable_err=disable_err, verbose=verbose)
    update.process_redis_cm_period_log(args.alert)
