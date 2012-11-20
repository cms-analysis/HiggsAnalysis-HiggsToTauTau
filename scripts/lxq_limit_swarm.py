#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script send all limit calculations of in a structure as created by the setup-htt.py script to NAF batch. A use example is e.g. lxq_limit_swarm.py MY-LIMIT/*, where the folder MY-LIMIT containes subfolders of type cmb, em et mt mm tt, ... which in themselves contain the masses directories. The script will split these jobs into single limit calculations per mass point in each subfolder.")
parser.add_option("-q", "--qsub", dest="qsub", default="-l h_cpu=1:00:00 -j y -o /dev/null", type="string", help="Arguments for qsub. [Default: \"-l h_cpu=1:00:00 -j y -o /dev/null\"]")
parser.add_option("-m", "--method", dest="method", default="--asymptotic", type="string", help="limit calculation method. [Default: \"--asymptotic\"]")
parser.add_option("--options", dest="options", default="", type="string", help="Options that should be passed on to combine. [Default: \"\"]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os

for dir in args:
    ana = dir[:dir.rfind('/')]
    limit = dir[len(ana)+1:]
    jobname = ana[ana.rfind('/')+1:]+'-'+limit
    ## create submission scripts
    os.system("lxq_limit.py {JOBNAME} \"{QSUB}\" \"{DIR}/*\" {METHOD} {OPTS}".format(
        JOBNAME=jobname,
        DIR=dir,
        QSUB=options.qsub,
        METHOD = options.method,
        OPTS = options.options
        ))
    ## execute
    os.system("./{JOBNAME}_submit.sh".format(JOBNAME=jobname))
    ## shelve
    os.system("mv {JOBNAME}_submit.sh {JOBNAME}".format(JOBNAME=jobname))
