#!/usr/bin/env python

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

import glob
import logging
import os
import sys

log = logging.getLogger("lxb_limit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

if len(sys.argv) < 5:
    print "Usage: lxb_limit.py submit_name \"bsub args\" \"ARG_GLOB\" \"[other options]\""
    sys.exit(1)

name = sys.argv[1]
bsubargs = sys.argv[2]
dirglob = sys.argv[3]
option_str = sys.argv[4:]

script_template = '''#!/bin/bash

cd {working_dir}
eval `scram runtime -sh`

echo "Running limit.py:"
echo "with options {options}"
echo "in directory {directory}"

$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/limit.py {options} {directory}

'''

condor_sub_template = '''
log = condor.log
notification = never
getenv = true
# make sure AFS is accessible and suppress Condor's default FilesystemDomain requirements
requirements = HasAFS_OSG && TARGET.FilesystemDomain =!= UNDEFINED

'''

if not glob.glob(dirglob):
    print "No limit directories found in glob %s" % dirglob
    sys.exit(1)

submit_name = '%s_submit.sh' % name
with open(submit_name, 'w') as submit_script:
    if bsubargs == "condor":
        submit_script.write(condor_sub_template)
    if not os.path.exists(name) :
        os.system("mkdir %s" % name)
    for i, dir in enumerate(glob.glob(dirglob)):
        ## don't submit jobs on old LSF output
        if 'LSFJOB' in dir:
            continue
        if 'common' in dir:
            continue
        log.info("Generating limit.py script for %s", dir)
        script_file_name = '%s/%s_%i.sh' % (name, name, i)
        with open(script_file_name, 'w') as script:
            script.write(script_template.format(
                working_dir = os.getcwd(),
                options = ' '.join(option_str),
                directory = dir
            ))
        os.system('chmod 755 %s' % script_file_name)
        if bsubargs == "condor":
            submit_script.write("\n")
            submit_script.write("executable = %s/%s\n" % (os.getcwd(), script_file_name))
            submit_script.write("output = %s/%s\n" % (os.getcwd(), script_file_name.replace('.sh', '.stdout')))
            submit_script.write("error = %s/%s\n" % (os.getcwd(), script_file_name.replace('.sh', '.stderr')))
            submit_script.write("queue")
        else:
            submit_script.write('bsub %s %s/%s\n' % (bsubargs, os.getcwd(), script_file_name))

os.system('chmod 755 %s' % submit_name)
