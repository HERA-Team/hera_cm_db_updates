#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 David DeBoer
# Licensed under the 2-clause BSD license.

"""Setup tools for hera_cm_db_updates."""

from setuptools import setup

setup_args = {
    'name': "hera_cm_db_updates",
    'description': "Various configuration management tools",
    'license': "BSD",
    'url': "https://github.com/HERA-Team/hera_mc",
    'author': "HERA Team",
    'author_email': "hera-sw@lists.berkeley.edu",
    'version': '1.0',
    'packages': ['hera_cm'],
    'scripts': ['scripts/write_sqlite.py', 'scripts/update_info.py', 'scripts/update_connect.py'],
    'include_package_data': True,
    'install_requires': []
}

if __name__ == '__main__':
    setup(**setup_args)
