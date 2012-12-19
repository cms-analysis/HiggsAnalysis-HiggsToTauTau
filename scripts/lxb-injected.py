#!/usr/bin/env python
from optparse import OptionParser, OptionGroup
## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to set up a set of scripts for statistical signal injection. The source directory for individual signal injections can be given by the option --inputs. This directory will be cloned in N subdirectories. N can be changed by --njob. in each subdirectory a signal is injected statistically. Afterwards the limit calculation is run for each mass that is found in the subdirectory. ARGS corresponds to the masses which are to be analysed.")
parser.add_option("-n", "--name", dest="name", default="TEST", type="string", help="Name of the batch submission scripts. [Default: \"TEST\"]")
parser.add_option("-i", "--input", dest="input", default="TEST/INJECT", type="string", help="Name of the input directory that should be used as starting point for signal injection. [Default: \"TEST/INJECT\"]")
parser.add_option("--bsub", dest="bsub", default="-q 1nd", type="string", help="Submission arguments for the batch queue. [Default: \"-q 1nd\"]")

parser.add_option("--njob", dest="njob", default="100", type="string", help="Number of toys for which to inject signal. (One toy per job). [Default: \"100\"]")
parser.add_option("--mass-points-per-job", dest="per_job", type="int", default=10, help="Maximum number of mass points to run per batch job. If more mass points given as arguments the number of jobs will be increased. NOTE: this will be true for each toy. This will increase the number of jobs quadratically. [Default: \"10\"]")
parser.add_option("--options", dest="opts", default="--observedOnly", type="string", help="Options for limit calculation with limit.py. [Default: \"--observedOnly\"]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import random
import string
import logging
import os
import sys

log = logging.getLogger("lxb-injected")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

name     = options.name
bsubargs = options.bsub
input    = options.input.rstrip('/')
njob     = options.njob
opts     = options.opts

random.seed()

script_template = '''#!/usr/bin/env python

import os

print "Running limit.py with signal injected:"
print "with options {OPTS}"
print "for directory {PATH}/{DIR}"
print "for random seed {RND}"
print "for masses {MASSES}"
os.system("pwd")

print "Copying limit folder {PWD}/{PATH}/{DIR} => {TMPDIR}/{USER}/{DIR}_{JOBID}"
os.system("mkdir -p {TMPDIR}/{USER}")
os.system("cp -r {PWD}/{PATH}/{DIR} {TMPDIR}/{USER}/{DIR}_{JOBID}")
os.system("python {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/scripts/inject-signal.py -i {TMPDIR}/{USER}/{DIR}_{JOBID} -o {JOBID} -r {RND} {MASSES} &> /dev/null")

masses = "{MASSES}".strip().rstrip().replace(" ", "_").split("_")
for m in masses :
    if m :
      print "limit.py --asymptotic {OPTS} {TMPDIR}/{USER}/{DIR}_{JOBID}/%s" % m
      os.system("limit.py --asymptotic {OPTS} {TMPDIR}/{USER}/{DIR}_{JOBID}/%s" % m)
      os.system("cp -v {TMPDIR}/{USER}/{DIR}_{JOBID}/%s/higgsCombine-obs.Asymptotic.mH%s.root {PWD}/{PATH}/{DIR}/%s/higgsCombine-obs.Asymptotic.mH%s-{JOBID}.root" % (m, m, m, m))
os.system("rm -r {TMPDIR}/{USER}/{DIR}_{JOBID}")
'''

condor_sub_template = '''
universe=vanilla
log = condor.log
notification = never
getenv = true
# make sure AFS is accessible and suppress default FilesystemDomain requirements of Condor
requirements = HasAFS_OSG && TARGET.FilesystemDomain =!= UNDEFINED && TARGET.UWCMS_CVMFS_Revision >= 0
transfer_input_files=
when_to_transfer_output=on_exit
should_transfer_files=yes

'''

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

masses_str = []
for mass in parseArgs(args) :
    masses_str.append(str(mass))
    
## split up masses into groups
def group_into_chunks(iterable, n):
    output = []
    for x in iterable:
        output.append(x)
        if len(output) == n:
            yield output
            output = []
    # any leftovers
    if output:
        yield output

mass_groups = []
for group in group_into_chunks(masses_str, options.per_job):
    mass_groups.append(group)

os.system("mkdir %s" % name)
submit_name = '%s_submit.sh' % name
with open(submit_name, 'w') as submit_script:
    tmpdir = '/tmp'
    if options.bsub == "condor":
        tmpdir='${_CONDOR_SCRATCH_DIR}'
        submit_script.write(condor_sub_template)
    for idx in range(int(njob)):
        rnd = random.randint(1, 999999)
        log.info("Generating script for limit.py with injected signal for toy %g - %i subjobs will be created", idx, len(mass_groups))
        for mass_grp_idx, mass_group in enumerate(mass_groups):
            script_file_name = '%s/%s_%i_%i.py' % (name, name, idx, mass_grp_idx)
            with open(script_file_name, 'w') as script:
                script.write(script_template.format(
                    CMSSW_BASE=os.environ["CMSSW_BASE"],
                    PWD= os.getcwd(),
                    MASSES = ' '.join(mass_group),
                    USER = os.environ['USER'],
                    OPTS = opts,
                    PATH = input[:input.rfind('/')],
                    DIR = input[input.rfind('/')+1:],
                    JOBID = "%s_%s" % (idx, mass_grp_idx),
                    RND = rnd,
                    TMPDIR=tmpdir,
                    ))
            with open(script_file_name.replace('.py', '.sh'), 'w') as sh_file:
                sh_file.write("#!/bin/bash\n")
                sh_file.write("cd {PWD}; eval `scram runtime -sh`\n".format(PWD=os.getcwd()))
                sh_file.write("python %s/%s\n" % (os.getcwd(), script_file_name))

            os.system('chmod a+x %s' % script_file_name.replace('.py', '.sh'))
            bsubargs = options.bsub
            if bsubargs == "condor":
                submit_script.write("\n")
                submit_script.write("executable = %s/%s\n" % (os.getcwd(), script_file_name.replace('.py', '.sh')))
                submit_script.write("output = %s/%s\n" % (os.getcwd(), script_file_name.replace('.py', '.stdout')))
                submit_script.write("error = %s/%s\n" % (os.getcwd(), script_file_name.replace('.py', '.stderr')))
                submit_script.write("queue\n")
            else:
                submit_script.write('bsub %s %s/%s\n' % (bsubargs, os.getcwd(), script_file_name.replace('.py', '.sh')))
## change mode
os.system('chmod a+x %s' % submit_name)
## execute 
os.system('./%s' % submit_name)
## clean up
os.system('mv %s %s' % (submit_name, name))
