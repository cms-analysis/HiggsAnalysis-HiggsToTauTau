#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG", description="This is a script for simple job submission of limit.py processes to lxb/lxq. It is e.g. called from submit.py, when running this script in batch mode for several main options. The arguments ARGs correspond to the directories that are meant to be processed by limit.py")
##
## MAIN OPTIONS
##
parser.add_option("--name", dest="name", default="batch", type="string",
                  help="Add the job name here. [Default: \"batch\"]")
parser.add_option("--batch-options", dest="batch", default="", type="string",
                  help="Add all options you want to pass to lxb/lxq encapsulated by quotation marks '\"'. [Default: \"\"]")
parser.add_option("--limit-options", dest="limit", default="", type="string",
                  help="Add all options you want to pass to limit.py encapsulated by quotation marks '\"'. [Default: \"\"]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

    
'''

Parellelize calls to limit.py using LXBATCH.

Usage:

    lxb_limit.py submit_name "bsub opts" "ARG_GLOB" "limit.py options"

ARG_GLOB must expand to a list of directories.  Each entry in this list will be
a separate lxbatch job.  NB the use of quotes about ARG_GLOB.

Note also you may need to escape the quotes around sub-arguments.  For example,

    limit.py --tanb+ --userOpt '--minosAlgo stepping' cmb/*

would be

    lxb_limit.py my_limits "-q 1nh -n 6" "cmb/*"  --tanb+ --tanbparallel 6 --userOpt \'--minosAlgo stepping\'

will produce

    my_limits_submit.sh

which bsubs

    my_limits_0.sh
    ...
    my_limits_n.sh

'''
import os
import sys
import glob

import logging
log = logging.getLogger("lxb-limit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

dirglob = args[0]
print dirglob
name = options.name
print name
bsubargs = options.batch
print bsubargs
option_str = options.limit
print option_str

script_template = '''#!/bin/bash

cd {working_dir}
eval `scram runtime -sh`

echo "Running limit.py:"
echo "with options {options}"
echo "in directory {directory}"

echo "Running"
$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/limit.py {options} {directory}

'''

condor_sub_template = '''
log = condor.log
notification = never
getenv = true
## make sure AFS is accessible and suppress the default FilesystemDomain requirements of Condor
requirements = HasAFS_OSG && TARGET.FilesystemDomain =!= UNDEFINED && TARGET.UWCMS_CVMFS_Revision >= 0

'''

if not glob.glob(dirglob):
    print "No limit directories found in glob %s" % glob
    sys.exit(1)

submit_name = '%s_submit.sh' % name
with open(submit_name, 'w') as submit_script:
    if bsubargs == "condor":
        submit_script.write(condor_sub_template)
    if not os.path.exists(name):
        os.system("mkdir %s" % name)
    for i, dir in enumerate(glob.glob(dirglob)):
        ## don't submit jobs on old LSF output
        if 'LSFJOB' in dir:
            continue
        if 'common' in dir:
            continue
        log.info("Generating submission script for %s", dir)
        script_file_name = '%s/%s_%i.sh' % (name, name, i)
        with open(script_file_name, 'w') as script:
            script.write(
                script_template.format(
                working_dir=os.getcwd(),
                options=option_str,
                directory=dir
                ))
        os.system('chmod a+x %s' % script_file_name)
        if bsubargs == "condor":
            submit_script.write("\n")
            submit_script.write(
                "executable = %s/%s\n" % (os.getcwd(), script_file_name))
            submit_script.write(
                "output = %s/%s\n" % (
                    os.getcwd(), script_file_name.replace('.sh', '.stdout')))
            submit_script.write(
                "error = %s/%s\n"
                % (os.getcwd(), script_file_name.replace('.sh', '.stderr')))
            submit_script.write("queue\n")
        else:
            submit_script.write('bsub %s %s/%s\n'
                                % (bsubargs, os.getcwd(), script_file_name))
os.system('chmod a+x %s' % submit_name)
