#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to setup a set of script for statistical signal injection. The source directory for individual signal injections can be given by the option --inputs. This directory will be cloned in N subdirectories. N can be changed by --njob. in each subdirectory signal is injected statistically. Afterwards the limit calculation is run for each mass that is found in the subdirectory.")
parser.add_option("-n", "--name", dest="name", default="test-injection", type="string", help="Name of the output scripts. [Default: test-injected]")
parser.add_option("-i", "--input", dest="input", default="TEST/INJECT-SIGNAL", type="string", help="Input directory that should be used as starting point for signal injection. [Default: \"TEST/INJECT-SIGNAL\"]")
parser.add_option("--qsub", dest="qsub", default="-j y -o /dev/null -l h_cpu=1:00:00 ", type="string", help="Submission arguments for batch queue. [Default: '-j y -o /dev/null -l h_cpu=1:00:00']")

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

log = logging.getLogger("lxq_limit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

name     = options.name
qsubargs = options.qsub
input    = options.input
njob     = options.njob
masses   = options.masses
opts     = options.opts

random.seed()
rnd = random.randint(1, 999999)

script_template = '''
#!/usr/bin/bash
#$ -l h_cpu=4:00:00
export SCRAM_ARCH=$scram_arch
ini cmssw
ini autoproxy
cd {working_dir}
eval `scram runtime -sh`

echo "Running limit.py with signal injected:"
echo "with options {options}"
echo "for directory {input}"
echo "for random seed {rnd}"

cp -r {input} {input}_{jobID}
inject-signal.py -i {input}_{jobID} -r {rnd} {masses}
limit.py --asymptotic {options} {input}_{jobID}/*
'''

if options.collect :
    for mass in parseArgs(args) :
        ## to allow for more files to be combined distinguish by first digit in a first
        ## iteration, than cpomine the resulting 10 files to the final output file.
        for idx in range(10) :
            os.system("hadd {INPUT}/{MASS}/batch_collected_{IDX}.root {INPUT}_*{IDX}/{MASS}/higgsCombine-exp.Asymptotic.mH{MASS}.root".format(
                INPUT=input,
                MASS=mass,
                IDX=idx
                ))
        for idx in range(10) :
            os.system("hadd {INPUT}/{MASS}/batch_collected.root {INPUT}/{MASS}/batch_collected_{IDX}.root".format(
                INPUT=input,
                MASS=mass,
                IDX=idx
                ))
        os.system("rm -r {INPUT}/{MASS}/batch_collected_*.root")
else:
    submit_name = '%s_submit.sh' % name
    with open(submit_name, 'w') as submit_script:
        submit_script.write('export cmssw_base=$CMSSW_BASE\n')
        submit_script.write('export scram_arch=$SCRAM_ARCH\n')
        for idx in range(int(njob)):
            rnd = random.randint(1, 999999)
            log.info("Generating script for limit.py with injected signal for job %g", idx)
            script_file_name = '%s_%i.sh' % (name, idx)
            with open(script_file_name, 'w') as script:
                script.write(script_template.format(
                    working_dir = os.getcwd(),
                    options = opts,
                    rnd = rnd,
                    input = input,
                    jobID = idx,
                    masses = masses
                    ))
            os.system('chmod a+x %s' % script_file_name)
            submit_script.write('qsub -l site=hh -l h_vmem=4000M %s -v scram_arch -v cmssw_base %s\n' % (qsubargs, script_file_name))
    os.system('chmod a+x %s' % submit_name)
                
