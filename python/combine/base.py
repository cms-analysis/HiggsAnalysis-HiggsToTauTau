#!/usr/bin/env python

import os
import stat
from functools import partial
from multiprocessing import Pool

DRY_RUN=False

JOB_PREFIX="""#!/bin/sh
ulimit -s unlimited
cd %(CMSSW_BASE)s/src
export SCRAM_ARCH=%(SCRAM_ARCH)s
eval `scramv1 runtime -sh`
cd %(PWD)s
""" % ({
  'CMSSW_BASE' : os.environ['CMSSW_BASE'],
  'SCRAM_ARCH' : os.environ['SCRAM_ARCH'],
  'PWD'        : os.environ['PWD']
 })

def run_command(dry_run, command):
    if not dry_run:
        return os.system(command)
    else:
        print '[DRY-RUN]: ' + command

class CombineToolBase:
    description = 'Base class that simply passes through all arguments and handles job creation and submission'
    requires_root = False

    def __init__(self):
      self.job_queue = []
      self.args = None
      self.passthru = []
      self.job_mode = 'interactive'
      self.parallel = 1
      self.merge = 1
      self.task_name = 'combine_task'
      self.dry_run = False

    def attach_intercept_args(self, group):
      pass

    def attach_args(self, group):
      group.add_argument('--job-mode', default=self.job_mode, choices=['interactive', 'script', 'lxbatch', 'crab3'], help='Task execution mode')
      group.add_argument('--task-name', default=self.task_name, help='Task name, used for job script and log filenames for batch system tasks')
      group.add_argument('--parallel', type=int, default=self.parallel, help='Number of jobs to run in parallel [only affects interactive job-mode]')
      group.add_argument('--merge', type=int, default=self.merge, help='Number of jobs to run in a single script [only affects batch submission]')
      group.add_argument('--dry-run', action='store_true', help='Print commands to the screen but do not run them')

    def set_args(self, known, unknown):
      self.args = known
      self.job_mode = self.args.job_mode
      self.task_name = self.args.task_name
      self.parallel = self.args.parallel
      self.merge = self.args.merge
      self.dry_run = self.args.dry_run
      self.passthru.extend(unknown)

    def put_back_arg(self, arg_name, target_name):
      if hasattr(self.args, arg_name):
        self.passthru.extend([target_name, getattr(self.args, arg_name)])
        delattr(self.args, arg_name)

    def create_job_script(self, commands, script_filename):
        # print command
        fname = script_filename
        logname = script_filename.replace('.sh', '.log')
        with open(fname, "w") as text_file:
            text_file.write(JOB_PREFIX)
            for i, command in enumerate(commands):
                tee = 'tee' if i == 0 else 'tee -a'
                if command.startswith('combine'):
                    text_file.write('eval ' + command + ' 2>&1 | %s '%tee + logname + '\n')
                else:
                    text_file.write('command')
        st = os.stat(fname)
        os.chmod(fname, st.st_mode | stat.S_IEXEC)
        #print JOB_PREFIX + command
        print 'Created job script: %s' % script_filename

    def run_method(self):
        print vars(self.args)
        ## Put the method back in because we always take it out
        self.put_back_arg('method', '-M')
        print self.passthru
        command = 'combine ' + ' '.join(self.passthru)
        self.job_queue.append(command)
        self.flush_queue()

    def flush_queue(self):
        if self.job_mode == 'interactive':
            pool = Pool(processes=self.parallel)
            result = pool.map(partial(run_command, self.dry_run), self.job_queue)
            # print 'Results are', result
        elif self.job_mode == 'script':
            for i,j in enumerate(range(0, len(self.job_queue), self.merge)):
                self.create_job_script(self.job_queue[j:j+self.merge], 'job_%s_%i.sh' % (self.task_name, i))
        del self.job_queue[:]
