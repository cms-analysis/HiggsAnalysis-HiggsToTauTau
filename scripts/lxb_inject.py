#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to setup a set of script for statistical signal injection. The source directory for individual signal injections can be given by the option --inputs. This directory will be cloned in N subdirectories. N can be changed by --njob. in each subdirectory signal is injected statistically. Afterwards the limit calculation is run for each mass that is found in the subdirectory.")
parser.add_option("-n", "--name", dest="name", default="test-injection", type="string", help="Name of the output scripts. [Default: \"test-injected\"]")
parser.add_option("-i", "--input", dest="input", default="TEST/INJECT-SIGNAL", type="string", help="Input directory that should be used as starting point for signal injection. [Default: \"TEST/INJECT-SIGNAL\"]")
parser.add_option("--bsub", dest="bsub", default="-q 8nh", type="string", help="Submission arguments for batch queue. [Default: \"-q 8nh\"]")

parser.add_option("--njob", dest="njob", default="100", type="string", help="Number of jobs for which to inject signal. [Default: \"100\"]")
parser.add_option("--masses", dest="masses", default="110-145:5", type="string", help="Masses argument for signal injection. [Default: \"100-145:5\"]")
parser.add_option("--options", dest="opts", default="--observedOnly", type="string", help="Options for limit calculation with limit.py. [Default: \"--observedOnly\"]")
parser.add_option("--collect", dest="collect", default=False,  action="store_true", help="Collect the individual jobs of a single batch submission. [Default: False)")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import random
import logging
import os
import sys

log = logging.getLogger("lxb_limit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

name     = options.name
bsubargs = options.bsub
input    = options.input
njob     = options.njob
masses   = options.masses
opts     = options.opts

random.seed()

script_template = '''
#!/usr/bin/bash

cd {WORKING_DIR}
eval `scram runtime -sh`

echo "Running limit.py with signal injected:"
echo "with options {OPTIONS}"
echo "for directory {INPUT}"
echo "for random seed {RND}"

cp -r {INPUT} {INPUT}_{JOBID}
inject-signal.py -i {INPUT}_{JOBID} -r {RND} {MASSES}
limit.py --asymptotic {OPTIONS} {INPUT}_{JOBID}/*
'''
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

if options.collect :
    for mass in parseArgs([masses]) :
        ## to allow for more files to be combined distinguish by first digit in a first
        ## iteration, than cpomine the resulting 10 files to the final output file.
        for idx in range(10) :
            os.system("hadd {INPUT}/{MASS}/batch_collected_{IDX}.root {INPUT}_*{IDX}/{MASS}/higgsCombine-obs.Asymptotic.mH{MASS}.root".format(
                INPUT=input,
                MASS=mass,
                IDX=idx
                ))
        os.system("hadd {INPUT}/{MASS}/batch_collected.root {INPUT}/{MASS}/batch_collected_*.root".format(
            INPUT=input,
            MASS=mass,
            IDX=idx
            ))
        os.system("rm -r {INPUT}/{MASS}/batch_collected_*.root".format(INPUT=input, MASS=mass))
else:
    submit_name = '%s_submit.sh' % name
    with open(submit_name, 'w') as submit_script:
        for idx in range(int(njob)):
            rnd = random.randint(1, 999999)
            log.info("Generating script for limit.py with injected signal for job %g", idx)
            script_file_name = '%s_%i.sh' % (name, idx)
            with open(script_file_name, 'w') as script:
                script.write(script_template.format(
                    WORKING_DIR = os.getcwd(),
                    OPTIONS = opts,
                    MASSES = masses,
                    INPUT = input,
                    JOBID = idx,
                    RND = rnd
                    ))
            os.system('chmod a+x %s' % script_file_name)
            submit_script.write('bsub %s %s\n' % (bsubargs, script_file_name))
    os.system('chmod a+x %s' % submit_name)
