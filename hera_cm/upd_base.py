# -*- mode: python; coding: utf-8 -*-
# Copyright 2019 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""This is the base class for the script generators."""
import datetime
import os
import redis
import time
import socket
from . import signal_chain, cm_gsheet, util


class Update():
    """Base update class."""

    def __init__(self, script_type, script_path='default', verbose=True):
        """
        Initialize.

        Parameters
        ----------
        script_type : str
            Type of the script to generate (becomes component of dated name)
        script_path : str
            Path to the script.
        verbose : bool
            Verbose or not.
        """
        if script_path == 'default':
            from hera_mc import mc
            self.script_path = mc.get_cm_csv_path()
        else:
            self.script_path = script_path
        self.verbose = verbose
        self.cdatetime = datetime.datetime.now()
        hostname = socket.gethostname()
        if hostname != 'qmaster':
            tz = float(input(f"Host is {hostname} -- need a timezone (PST=-8/PDT=-7): "))
            self.cdatetime -= datetime.timedelta(hours=tz)
        self.cdate, self.ctime = util.YMD_HM(self.cdatetime)
        if script_type is None:
            self.script = None
        else:
            self.script = '{}_{}_{}'.format(self.cdate.replace('/', '')[2:], script_type,
                                            self.ctime.replace(':', ''))
            self.script = os.path.join(self.script_path, self.script)
        if script_type != 'no_signal_chain':
            self.hera = signal_chain.Update(script_to_run=self.script,
                                            chmod=True, verbose=verbose,
                                            cdate=self.cdate, ctime=self.ctime)
        self.update_counter = 0
        self.gsheet = None
        self.r = redis.Redis('redishost', decode_responses=True)

    def load_gsheet(self, node_csv='none', tabs=None, path='.'):
        """Get the googlesheet information from the internet."""
        if self.gsheet is None:
            self.gsheet = cm_gsheet.SheetData()
        self.gsheet.load_sheet(node_csv=node_csv, tabs=None, path=path)
        self.gsheet.load_ncm()

    def load_active(self):
        self.hera.active.load_connections()

    def load_gworkflow(self):
        if self.gsheet is None:
            self.gsheet = cm_gsheet.SheetData()
        self.gsheet.load_workflow()

    def process_redis_cm_period_log(self, alert=None):
        if alert is None:
            return
        dlog = self.r.hgetall('cm_period_log')
        lines = []
        for key in sorted(dlog.keys()):
            this_line = dlog[key]
            if util.include_this_line_in_log(this_line, lines):
                lines.append(this_line)
        self.distribute_log('Daily log', lines, alert)
        self.r.delete('cm_period_log')

    def distribute_log(self, prefix, lines, to_addr, log_entry_prefix=None):
        if not len(lines):
            return
        subj = f"{prefix} {datetime.datetime.now().isoformat(timespec='minutes')}"
        msg = subj + '\n\n'
        for this_line in lines:
            msg += util.parse_log_line(this_line, prefix=log_entry_prefix)
        self.alert_email(subj=subj, msg=msg, to_addr=to_addr)

    def alert_email(self, subj, msg, to_addr, from_addr='hera@lists.berkeley.edu'):
        from hera_mc import watch_dog
        try:
            watch_dog.send_email(subj, msg, to_addr=to_addr, from_addr=from_addr)
        except ConnectionRefusedError:
            print("No email sent - ConnectionRefusedError")

    def finish(self, cron_script=None, archive_to=None, alert=None):
        """
        Close out process.  If no updates, it deletes the script file.
        If both parameters are None, it just leaves things alone.

        Parameters
        ----------
        cron_script : str or None
            If str, copies the script file to that.  Assumes in same directory as script.
            If no updates in script, then makes empty one.
        archive_to : str or None
            If str, moves the script file to that directory.  If not, deletes.
        alert : list or None
            If list, email addresses to alert if updates.
        """
        self.hera.script_teardown()
        if self.script is None or (cron_script is None and archive_to is None):
            return
        if cron_script is not None:
            cron_script = os.path.join(self.script_path, cron_script)
            if os.path.exists(cron_script):
                os.remove(cron_script)

        if self.update_counter == 0:
            os.remove(self.script)
            if self.verbose:
                print("No updates found.  Removing {}.".format(self.script))
            if cron_script is not None:
                with open(cron_script, 'w') as fp:
                    fp.write('\n')
                if self.verbose:
                    print("Writing empty {}.".format(cron_script))
        else:
            with open(self.script, 'r') as fp:
                script_lines = fp.readlines()
            msg = ''.join(script_lines)
            logtime = int(time.time() * 10000)
            for i, line in enumerate(script_lines):
                key = f"{logtime}{i:04d}"
                self.r.hset('cm_period_log', key, line)
            if archive_to is not None:
                os.system('cp {} {}'.format(self.script, archive_to))
                if self.verbose:
                    print("Copying {}  -->  {}".format(self.script, archive_to))
            if cron_script is not None:
                os.rename(self.script, cron_script)
                if self.verbose:
                    print("Moving {}  -->  {}".format(self.script, cron_script))
            else:
                os.remove(self.script)
            if alert is not None:
                self.alert_email(subj=f"Update: {self.script}", msg=msg, to_addr=alert)

        if cron_script is not None and os.path.exists(cron_script):
            os.chmod(cron_script, 0o755)
