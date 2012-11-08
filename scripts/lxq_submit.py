#!/usr/bin/env python

'''

Parellelize calls to submit.py using NAF batch.

Usage:

    submit.py submit_name "ARG_GLOB" [other options]

ARG_GLOB must expand to a list of directories.  Each entry in this list will be
a separate batch job.  NB the use of quotes about ARG_GLOB.

Example:

    submit.py --method tanb+ --options '--interpolation=mode-1' cmb/*

would become

    lxq_submit.py cmb_create "cmb/*" "--method tanb+" "--options '--interpolation=mode-1'"

which is then submitted by:

    bash < cmb_create_submit.sh

'''

import glob
import logging
import os
import sys

log = logging.getLogger("lxq_submit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

if len(sys.argv) < 4:
    print "Usage: lxq_submit.py submit_name \"ARG_GLOB\" \"[other options]\""
    sys.exit(1)

name = sys.argv[1]
dirglob = sys.argv[2]
option_str = sys.argv[3:]

script_template = '''
#!/usr/bin/bash
#$ -l h_cpu=1:00:00
export SCRAM_ARCH=$scram_arch
ini cmssw
ini autoproxy
cd {working_dir}
eval `scram runtime -sh`

echo "Running submit.py:"
echo "with options {options}"
echo "in directory {directory}"


$cmssw_base/src/HiggsAnalysis/HiggsToTauTau/scripts/submit.py {options} {directory}

'''

submit_name = '%s_submit.sh' % name
with open(submit_name, 'w') as submit_script:
    submit_script.write('export cmssw_base=$CMSSW_BASE\n')
    submit_script.write('export scram_arch=$SCRAM_ARCH\n')
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
        submit_script.write('qsub -l site=hh -j y -o /dev/null -l h_vmem=4000M -v scram_arch -v cmssw_base %s\n' % script_file_name)
os.system('chmod 755 %s' % submit_name)
