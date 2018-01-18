#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2017 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Script to handle updating the sqlite db from files.
"""

from __future__ import absolute_import, division, print_function
from hera_mc import cm_transfer
cm_transfer.convert_all_csv_to_sqlite3()
