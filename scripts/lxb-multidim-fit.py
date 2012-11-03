#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="Script to setup a set of scripts for maxlimum likelihood scan for 2-dim parameters estimates.")
parser.add_option("-n", "--name", dest="name", default="ml-scan", type="string", help="Name of the output scripts. [Default: \"ml-scan\"]")
parser.add_option("--bsub", dest="bsub", default="-q 8nh", type="string", help="Submission arguments for batch queue. [Default: \"-q 8nh\"]")
parser.add_option("--njobs", dest="njobs", default="100", type="string", help="Number of jobs for for scan. [Default: \"100\"]")
parser.add_option("--npoints", dest="npoints", default="100", type="string", help="Number of points per job. [Default: \"100\"]")
parser.add_option("--physics-model", dest="fitModel", type="string", default="", help="Physics model for multi-dimensional maximum likelihood. The physics model should be defined by a model name and a path to a python implementation of the model separated by '='. For example 'ggH-qqH-model=PATH-TO-IMPLEMENTATION'. In this case a workspace of the model with given model options will be created with the name 'ggH-qqH-model.root'. It is also possible to pass on only a name of a physics model, like 'ggH-qqH-model'. In this case it will be assumed that the model with name 'ggH-qqH-model' has been created beforehand. [Default: \"\"]")
parser.add_option("--physics-model-options", dest="fitModelOptions", type="string", default="", help="Potential options for the used physics model for multi-dimensional maximum likelihood. More options can be passed on separated by ','. [Default: \"\"]")
parser.add_option("--options", dest="opts", default="", type="string", help="Additional options for limit.py. [Default: \"\"]")
parser.add_option("--collect", dest="collect", default=False,  action="store_true", help="Collect the individual jobs of a single batch submission after completion. [Default: False)")
parser.add_option("--stable", dest="stable", default=False, action="store_true", help="Run maximum likelihood fit with a set of options that lead to stable results. Makes use of the common options --rMin and --rMax to define the boundaries of the fit. [Default: True]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import random
import string
import logging
import os
import sys

log = logging.getLogger("lxb_limit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

script_template = '''
#!/usr/bin/bash

cd {WORKING_DIR}
eval `scram runtime -sh`

echo "Running limit.py with multidim-fit"
echo "with options {OPTIONS}"
echo "in directory {DIRECTORY}"

limit.py --multidim-fit {STABEL} --algo grid --points {POINTS} --firstPoint {FIRST} --lastPoint {LAST} --physics-model {MODEL} --name {OUTPUT} {OPTIONS} {DIRECTORY}
'''

input = args[0]
njobs = int(options.njobs)
npoints = int(options.npoints)
points = njobs*npoints
model = options.fitModel.split('=')
    
if options.collect :
    os.system("hadd {DIR}/higgsCombine{MODEL}.MultiDimFit.mH{MASS}.root {DIR}/higgsCombine*.MultiDimFit.mH{MASS}-[0-9]*-[0-9]*.root".format(
        DIR=input,
        MASS=input[input.rfind("/")+1:],
        MODEL=options.name
        ))
    #os.system("rm {DIR}/higgsCombine*.MultiDimFit.mH{MASS}-[0-9]*-[0-9]*.root".format(
    #    DIR=input,
    #    MASS=input[input.rfind("/")+1:]
    #    ))
    print "root -l -b -q HiggsAnalysis/HiggsToTauTau/macros/contours2D.C+\\(\\\"{DIR}\\\",\\\"{MODEL}-contours\\\",\\\"{XVAL}\\\",\\\"{YVAL}\\\",\\\"scan\\\",\\\"{MODEL}\\\",\\\"{MASS}\\\"\\)"
else :
    os.system("limit.py --multidim-fit {STABEL} --setup-only --physics-model '{MODEL}' --physics-model-options '{OPT}' {DIR}".format(
        STABEL = "--stable" if options.stable else "",
        MODEL = options.fitModel,
        OPT = options.fitModelOptions,
        DIR = input
        ))
    os.system("mkdir %s" % options.name)
    submit_name = '%s_submit.sh' % options.name
    with open(submit_name, 'w') as submit_script:
        for idx in range(int(njobs)) :
            log.info("Generating limit.py script for %s", args[0])
            script_file_name = '%s/submit_%i.sh' % (options.name, idx)
            with open(script_file_name, 'w') as script:
                script.write(script_template.format(
                    STABEL = "--stable" if options.stable else "",
                    WORKING_DIR = os.getcwd(),
                    DIRECTORY = input,
                    OPTIONS = options.opts,
                    POINTS = str(points),
                    FIRST = str(idx*npoints+1),
                    LAST = str((idx+1)*npoints),
                    MODEL = model[0],
                    OUTPUT = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                    ))
            os.system('chmod a+x %s' % script_file_name)
            submit_script.write('bsub %s %s/%s\n' % (options.bsub, os.getcwd(), script_file_name))
    os.system('chmod 755 %s' % submit_name)
