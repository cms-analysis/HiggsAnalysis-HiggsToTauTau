#!/usr/bin/env python

'''

Parellelize calls to limit.py using NAF batch.

Usage:

    lxq_limit.py submit_name "qsub opts" "ARG_GLOB" "limit.py options"

ARG_GLOB must expand to a list of directories.  Each entry in this list will be
a separate NAF batch job.  NB the use of quotes about ARG_GLOB.

Note also you may need to escape the quotes around sub-arguments.  For example,

    limit.py --multidim-fit --stable --algo grid --points 10000 --physics-model 'HiggsAnalysis.CombinedLimit.PhysicsModel:floatingXSHiggs' --physics-model-options 'modes=ggH,qqH' cmb/125

would be

    lxq_gridScan.py my_grid "-j y -o /dev/null" "cmb/125" "10 1000" "--multidim-fit --stable --algo grid --physics-model 'HiggsAnalysis.CombinedLimit.PhysicsModel:floatingXSHiggs' --physics-model-options 'modes=ggH,qqH'"

will produce

    my_grid_submit.sh

which qsubs

    my_grid_0.sh
    ...
    my_grid_n.sh

'''

import glob
import logging
import os
import sys

log = logging.getLogger("lxq_limit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

if len(sys.argv) < 5:
    print "Usage: lxq_gridScan.py submit_name \"qsub args\" \"ARG_GLOB\" \"[other options]\""
    sys.exit(1)

name = sys.argv[1]
qsubargs = sys.argv[2]
dirglob = sys.argv[3]
option_split = sys.argv[4] ### how many jobs do you want to create according to total number of points? ATTENTION this only works for values for which second_parameter/first_parameter is a interger
option_str = sys.argv[5:]

script_template = '''
#!/usr/bin/bash
#$ -l h_cpu=4:00:00
export SCRAM_ARCH=$scram_arch
ini cmssw
ini autoproxy
cd {working_dir}
eval `scram runtime -sh`

echo "Running limit.py:"
echo "with options {options}"
echo "in directory {directory}"


$cmssw_base/src/HiggsAnalysis/HiggsToTauTau/scripts/limit.py {options} --firstPoint {FIRSTPOINT} --lastPoint {LASTPOINT} --points {GRIDPOINTS} --name {ROOTNAME} {directory}

'''

submit_name = '%s_submit.sh' % name
with open(submit_name, 'w') as submit_script:
    submit_script.write('export scram_arch=$SCRAM_ARCH\n')
    submit_script.write('export cmssw_base=$CMSSW_BASE\n')
    (njobs, gridPoints) = option_split.split(" ");
    print njobs, gridPoints
    for i in range(1,int(njobs)+1) :
        # Don't submit jobs on old LSF output
        if 'LSFJOB' in dirglob:
            continue
        log.info("Generating limit.py script for %s", dirglob)
        script_file_name = '%s_%i.sh' % (name, i)
        start = 1+(i-1)*int(gridPoints)/int(njobs)
        end = i*int(gridPoints)/int(njobs)
        print i, start, end, os.getcwd()
        with open(script_file_name, 'w') as script:
            script.write(script_template.format(
                working_dir = os.getcwd(),
                options = ' '.join(option_str),
                directory = dirglob,
                FIRSTPOINT = str(start),
                LASTPOINT = str(end),
                GRIDPOINTS = str(gridPoints),
                ROOTNAME = str(i)
            ))
        os.system('chmod 755 %s' % script_file_name)
        submit_script.write('qsub -l site=hh %s -v scram_arch -v cmssw_base %s\n' % (qsubargs, script_file_name))
os.system('chmod 755 %s' % submit_name)
