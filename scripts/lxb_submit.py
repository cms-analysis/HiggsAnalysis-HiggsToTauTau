#!/usr/bin/env python

'''

Parellelize calls to submit.py using LXBATCH.

Usage:

    submit.py submit_name "ARG_GLOB" [other options]

ARG_GLOB must expand to a list of directories.  Each entry in this list will be
a separate lxbatch job.  NB the use of quotes about ARG_GLOB.

Example:

    submit.py --method tanb+ cmb/*

would become

    lxb_submit.py cmb_create "cmb/*" "--method tanb+"

which is then submitted by:

    bash < cmb_create_submit.sh

'''

import glob
import logging
import os
import sys

log = logging.getLogger("lxb_submit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

if len(sys.argv) < 4:
    print "Usage: lxb_submit.py submit_name \"ARG_GLOB\" \"[other options]\""
    sys.exit(1)

name = sys.argv[1]
dirglob = sys.argv[2]
option_str = sys.argv[3:]

script_template = '''
#!/usr/bin/bash

cd {working_dir}
eval `scram runtime -sh`

echo "Running submit.py:"
echo "with options {options}"
echo "in directory {directory}"

$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/submit.py {options} {directory}

'''

submit_name = '%s_submit.sh' % name
with open(submit_name, 'w') as submit_script:
    for i, dir in enumerate(glob.glob(dirglob)):
        # Don't submit jobs on old LSF output
        if 'LSFJOB' in dir:
            continue
        log.info("Generating submit.py script for %s", dir)
        script_file_name = '%s_%i.sh' % (name, i)
        with open(script_file_name, 'w') as script:
            script.write(script_template.format(
                working_dir = os.getcwd(),
                options = ' '.join(option_str),
                directory = dir
            ))
        os.system('chmod 755 %s' % script_file_name)
        submit_script.write('bsub -q 1nh %s\n' % script_file_name)
os.system('chmod 755 %s' % submit_name)
