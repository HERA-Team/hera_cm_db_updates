#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

import cm_overview
x = cm_overview.Overview()

x.get_hookup()
x.get_apriori()
x.get_sheets()
x.get_part_info()
x.find_mismatches()
x.dump_data()
