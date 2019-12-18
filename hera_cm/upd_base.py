# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
This is the base class for the script generators
"""
import datetime
import os
from . import signal_chain, cm_gsheet


class Update(object):
    def __init__(self, script_nom, script_path, verbose):
        self.script_path = script_path
        self.verbose = verbose
        self.now = datetime.datetime.now()
        self.cdate = '{}/{:02d}/{:02d}'.format(self.now.year, self.now.month, self.now.day)
        self.ctime = '{:02d}:{:02d}'.format(self.now.hour, self.now.minute)
        if script_nom is None:
            self.script = None
        else:
            self.script = '{}_{}_{}'.format(self.cdate.replace('/', '')[2:], script_nom,
                                            self.ctime.replace(':', ''))
            self.hera = signal_chain.Update(self.script, output_script_path=script_path, chmod=True,
                                            verbose=verbose, cdate=self.cdate, ctime=self.ctime)
        self.update_counter = 0

    def load_gsheet(self, node_csv='none'):
        """
        Gets the googlesheet information from the internet
        """
        self.gsheet = cm_gsheet.SheetData()
        self.gsheet.load_sheet(node_csv=node_csv)

    def finish(self, arc_path, cron_script):
        """
        Close out process.
        """
        if self.script is None:
            return
        self.hera.done()
        apply_updates = self.update_counter > 0
        init_script_file = os.path.join(self.script_path, self.script)
        cron_script_file = os.path.join(self.script_path, cron_script)
        if os.path.exists(cron_script_file):
            os.remove(cron_script_file)
        if apply_updates:
            if arc_path is not None:
                if self.verbose:
                    print("Copying {}  -->  {}".format(init_script_file, arc_path))
                    print("Renaming {}  -->  {}".format(init_script_file, cron_script_file))
                os.system('cp {} {}'.format(init_script_file, arc_path))
                os.rename(init_script_file, cron_script_file)
        else:
            if self.verbose:
                print("Removing {}".format(init_script_file))
            os.remove(init_script_file)
            with open(cron_script_file, 'w') as fp:
                fp.write('\n')
        if os.path.exists(cron_script_file):
            os.chmod(cron_script_file, 0o755)
