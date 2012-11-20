#!/usr/bin/env python

'''

Parellelize calls to limit.py using NAF batch.

Usage:

    lxq_limit.py submit_name "qsub opts" "ARG_GLOB" "limit.py options"

ARG_GLOB must expand to a list of directories.  Each entry in this list will be
a separate NAF batch job.  NB the use of quotes about ARG_GLOB.

Note also you may need to escape the quotes around sub-arguments.  For example,

    limit.py --tanb+ --tanb-parallel 4 --userOpt '--minosAlgo stepping' cmb/*

would be

    lxq_limit.py my_limits "-l h_cpu=1:00:00 -j y -o /dev/null" "cmb/*"  "--tanb+ --tanb-parallel 4 --userOpt '--minosAlgo stepping'"

will produce

    my_limits_submit.sh

which qsubs

    my_limits_0.sh
    ...
    my_limits_n.sh

'''

import glob
import logging
import os
import sys

log = logging.getLogger("lxq_limit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

if len(sys.argv) < 5:
    print "Usage: lxq_limit.py submit_name \"qsub args\" \"ARG_GLOB\" \"[other options]\""
    sys.exit(1)

name = sys.argv[1]
qsubargs = sys.argv[2]
dirglob = sys.argv[3]
option_str = sys.argv[4:]

script_template = '''
#!/usr/bin/bash
export SCRAM_ARCH=$scram_arch
ini cmssw
ini autoproxy
cd {working_dir}
eval `scram runtime -sh`

echo "Running limit.py:"
echo "with options {options}"
echo "in directory {directory}"


$cmssw_base/src/HiggsAnalysis/HiggsToTauTau/scripts/limit.py {options} {directory}

'''

submit_name = '%s_submit.sh' % name
with open(submit_name, 'w') as submit_script:
    submit_script.write('export scram_arch=$SCRAM_ARCH\n')
    submit_script.write('export cmssw_base=$CMSSW_BASE\n')
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
        submit_script.write('qsub -l site=hh -l h_vmem=4000M %s -v scram_arch -v cmssw_base %s\n' % (qsubargs, script_file_name))
os.system('chmod 755 %s' % submit_name)
