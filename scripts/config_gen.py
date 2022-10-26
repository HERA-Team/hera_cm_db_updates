#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2022 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Script to generate yaml configs."""

import argparse
from hera_cm import cm_config

ap = argparse.ArgumentParser()
ap.add_argument('-o', '--old_config_file', help='Name of the old config file', default='snap_conf.txt')
ap.add_argument('-c', '--config_dict', help="Name of config dict.", default=None)
args = ap.parse_args()

if args.config_dict is None:
    print("Run with -c flag with one of:")
    for ec in cm_config.configs:
        print(f"\t{ec}")
else:
    cmc = cm_config.Configuration(args.old_config_file)
    cmc.get_hostnames_to_use(**cm_config.configs[args.config_dict])
    cmc.generate_new_fengines()
    cmc.write_yaml()
    cm_config.geo_handling.show_it_now()