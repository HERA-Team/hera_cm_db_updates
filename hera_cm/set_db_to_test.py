#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

from hera_mc import cm_transfer
cm_csv_path = '/Users/ddeboer/Documents/ubase/Projects/HERA/ops/hera_mc/hera_mc/data/test_data'
cm_transfer.initialize_db_from_csv(session=None, tables='all', maindb=False, testing=False, cm_csv_path=cm_csv_path)
