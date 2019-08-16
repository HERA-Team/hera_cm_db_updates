#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

import cm_overview
x = cm_overview.Overview()

x.compare(antkeys='all', output=None)
x.get_sheet_commands()
x.get_mismatch_commands()
x.process_commands()
