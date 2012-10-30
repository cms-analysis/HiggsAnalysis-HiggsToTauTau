#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to setup a set of scripts for statistical signal injection. The source directory for individual signal injections can be given by the option --inputs. This directory will be cloned in N subdirectories. N can be changed by --njob. in each subdirectory signal is injected statistically. Afterwards the limit calculation is run for each mass that is found in the subdirectory. ARGS corresponds to the masses which are to be analysed.")
parser.add_option("-n", "--name", dest="name", default="test-injection", type="string", help="Name of the output scripts. [Default: \"test-injected\"]")
parser.add_option("-i", "--input", dest="input", default="TEST/INJECT-SIGNAL", type="string", help="Input directory that should be used as starting point for signal injection. [Default: \"TEST/INJECT-SIGNAL\"]")
parser.add_option("--bsub", dest="bsub", default="-q 1nd", type="string", help="Submission arguments for batch queue. [Default: \"-q 1nd\"]")

parser.add_option("--njob", dest="njob", default="100", type="string", help="Number of jobs for which to inject signal. [Default: \"100\"]")
parser.add_option("--options", dest="opts", default="--observedOnly", type="string", help="Options for limit calculation with limit.py. [Default: \"--observedOnly\"]")
parser.add_option("--collect", dest="collect", default=False,  action="store_true", help="Collect the individual jobs of a single batch submission. [Default: False)")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import random
import string
import logging
import os
import sys

log = logging.getLogger("lxb_limit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

name     = options.name
bsubargs = options.bsub
input    = options.input
njob     = options.njob
opts     = options.opts

random.seed()

script_template = '''
#!/usr/bin/env python

import os

print "Running limit.py with signal injected:"
print "with options {OPTS}"
print "for directory {PATH}/{DIR}"
print "for random seed {RND}"
print "for masses {MASSES}"

print "Copying limit folder {PWD}/{PATH}/{DIR} => /tmp/{USER}/{DIR}_{JOBID}"
os.system("cp -r {PWD}/{PATH}/{DIR} /tmp/{USER}/{DIR}_{JOBID}")
os.system("inject-signal.py -i /tmp/{USER}/{DIR}_{JOBID} -o {JOBID} -r {RND} {MASSES}")

masses = "{MASSES}".split()
for m in masses :
    os.system("limit.py --asymptotic {OPTS} /tmp/{USER}/{DIR}_{JOBID}/%s" % m)
    os.system("cp /tmp/{USER}/{DIR}_{JOBID}/%s/higgsCombine-obs.Asymptotic.mH%s.root {PWD}/{PATH}/{DIR}/%s/higgsCombine-obs.Asymptotic.mH%s-{JOBID}.root" % (m, m, m, m))
os.system("rm -r /tmp/{USER}/{DIR}_{JOBID}")
'''

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

masses = args[0]
masses_str = []
for mass in parseArgs([masses]) :
    masses_str.append(str(mass))

if options.collect :
    for mass in parseArgs([masses]) :
        ## to allow for more files to be combined distinguish by first digit in a first
        ## iteration, than cpomine the resulting 10 files to the final output file.
        for idx in range(10 if int(options.njob)>10 else int(options.njob)) :
            os.system("hadd {INPUT}/{MASS}/batch_collected_{IDX}.root {INPUT}/{MASS}/higgsCombine-obs.Asymptotic.mH{MASS}-*{IDX}.root".format(
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
    os.system("mkdir %s" % name)
    submit_name = '%s_submit.sh' % name
    with open(submit_name, 'w') as submit_script:
        for idx in range(int(njob)):
            rnd = random.randint(1, 999999)
            print "Random: ",rnd
            log.info("Generating script for limit.py with injected signal for job %g", idx)
            script_file_name = '%s/%s_%i.py' % (name, name, idx)
            with open(script_file_name, 'w') as script:
                script.write(script_template.format(
                    PWD= os.getcwd(),
                    MASSES = ' '.join(masses_str),
                    USER = os.environ['USER'],
                    OPTS = opts,
                    PATH = input[:input.rfind('/')],
                    DIR = input[input.rfind('/')+1:],
                    JOBID = idx,
                    RND = rnd
                    ))
            os.system("echo \"cd {PWD}; eval \`scram runtime -sh\`\" >".format(PWD=os.getcwd())+script_file_name.replace('.py', '.sh'))
            os.system(("echo \"python %s/%s" % (os.getcwd(), script_file_name))+"\" >> "+script_file_name.replace('.py', '.sh'))
            os.system('chmod a+x %s' % script_file_name.replace('.py', '.sh'))
            submit_script.write('bsub %s %s/%s\n' % (options.bsub, os.getcwd(), script_file_name.replace('.py', '.sh')))
    os.system('chmod a+x %s' % submit_name)
