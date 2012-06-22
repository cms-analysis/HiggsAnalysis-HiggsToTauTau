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

script_template = '''
#!/usr/bin/bash

cd {working_dir}
eval `scram runtime -sh`

echo "Running limit.py:"
echo "with options {options}"
echo "in directory {directory}"

$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/limit.py {options} {directory}

'''

submit_name = '%s_submit.sh' % name
with open(submit_name, 'w') as submit_script:
    for i, dir in enumerate(glob.glob(dirglob)):
        # Don't submit jobs on old LSF output
        if 'LSFJOB' in dir:
            continue
        log.info("Generating limit.py script for %s", dir)
        script_file_name = '%s_%i.sh' % (name, i)
        with open(script_file_name, 'w') as script:
            script.write(script_template.format(
                working_dir = os.getcwd(),
                options = ' '.join(option_str),
                directory = dir
            ))
        os.system('chmod 755 %s' % script_file_name)
        submit_script.write('bsub %s %s\n' % (bsubargs, script_file_name))
os.system('chmod 755 %s' % submit_name)
