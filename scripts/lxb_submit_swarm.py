#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to send all submit jobs to setup the limit calculation in mA-tanb to lx-batch. A use example is e.g. lxb_submit_swarm.py MY-LIMIT/*, where the folder MY-LIMIT containes subfolders of type cmb, em, et, mt, mm, ... which in themselves contain the masses directories. The script will split these jobs into single setups per mass point in each subfolder and sned these jobs to 8nh queue f lxbatch.")
parser.add_option("-m", "--method", dest="method", default="--method tanb+", type="string", help="limit calculation method. [Default: \"--method tanb+\"]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os

for dir in args:
    ana = dir[:dir.rfind('/')]
    limit = dir[len(ana)+1:]
    jobname = ana[ana.rfind('/')+1:]+'-'+limit+'-setup'
    ## create submission scripts
    os.system("lxb_submit.py {JOBNAME} \"{DIR}/*\" {METHOD}".format(
        JOBNAME=jobname,
        DIR=dir,
        METHOD = options.method
        ))
    ## execute
    os.system("./{JOBNAME}_submit.sh".format(JOBNAME=jobname))
    ## shelve
    os.system("mv {JOBNAME}_submit.sh {JOBNAME}".format(JOBNAME=jobname))
