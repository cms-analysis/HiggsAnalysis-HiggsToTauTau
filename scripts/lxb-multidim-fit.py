#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to setup a set of lxb jobs to do a maxlimum likelihood scan for 2-dim parameters estimates.")
parser.add_option("--name", dest="name", default="ml-scan", type="string",
                  help="Name of the output scripts. [Default: \"ml-scan\"]")
parser.add_option("--limit-options", dest="opts", default="", type="string",
                  help="Additional options for limit.py. [Default: \"\"]")
parser.add_option("--physics-model", dest="fitModel", type="string", default="",
                  help="Physics model for multi-dimensional maximum likelihood. The physics model should be defined by a model name and a path to a python implementation of the model separated by '='. For example 'ggH-qqH-model=PATH-TO-IMPLEMENTATION'. The model name is your choice. In this case a workspace of the model with given model options will be created with the name 'ggH-qqH-model.root'. It is also possible to pass on only a name of a physics model, like 'ggH-qqH-model'. In this case it will be assumed that the model with name 'ggH-qqH-model' has been created beforehand. [Default: \"\"]")
parser.add_option("--physics-model-options", dest="fitModelOptions", type="string", default="",
                  help="Potential options for the used physics model for multi-dimensional maximum likelihood. More options can be passed on separated by ','. [Default: \"\"]")
parser.add_option("--npoints", dest="npoints", default="100", type="string",
                  help="Number of points per job. [Default: \"100\"]")
parser.add_option("--batch-options", dest="bsub", default="-q 8nh", type="string",
                  help="Submission arguments for batch queue. [Default: \"-q 8nh\"]")
parser.add_option("--njobs", dest="njobs", default="100", type="string",
                  help="Number of jobs for for scan. [Default: \"100\"]")
parser.add_option("--lxq", dest="lxq", default=False, action="store_true",
                  help="Specify this option when running on lxq instead of lxb. [Default: False]")
parser.add_option("--condor", dest="condor", default=False, action="store_true",
                  help="Specify this option when running on condor instead of lxb (NOT YET IMPLEMENTED). [Default: False]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import random
import string
import os
import sys

import logging
log = logging.getLogger("lxb-multidim-fit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

## template for grid submission
script_template = '''
#!/usr/bin/bash

cd {WORKING_DIR}
eval `scram runtime -sh`

echo "Running limit.py with multidim-fit"
echo "with options {OPTIONS}"
echo "in directory {DIRECTORY}"

limit.py --multidim-fit --algo grid --points {POINTS} --firstPoint {FIRST} --lastPoint {LAST} --physics-model {MODEL} --name {OUTPUT} {OPTIONS} {DIRECTORY}
'''

lxq_fragment = '''
#!/bin/bash
export SCRAM_ARCH=$scram_arch
ini cmssw
ini autoproxy
'''

## arrange input parameters
input   = args[0]
njobs   = int(options.njobs)
npoints = int(options.npoints)
points  = njobs*npoints
model   = options.fitModel.split('=')

if options.lxq :
    script_template = script_template.replace('#!/bin/bash', lxq_fragment)

## leave footprint of grid calculation in mass directory directory
## to facilitate the reassambly later 
phys_opts = []
if ';' in options.fitModelOptions :
    phys_opts = options.fitModelOptions.split(';')
else :
    phys_opts = options.fitModelOptions.split(' ')
vals = []
for opt in phys_opts :
    if "modes" in opt :
        vals.append(opt.split('=')[1].split(',')[0])
        vals.append(opt.split('=')[1].split(',')[1])
ranges = {}
for val in vals :
    for opt in phys_opts :
        if val+"Range" in opt :
            ranges[val] = opt.split('=')[1]
footprint = open("{DIR}/.scan".format(DIR=input), "w")
footprint.write("points : {POINTS}\n".format(POINTS=points))
for val in vals :
    footprint.write("{VAL} : {RANGE}\n".format(VAL=val, RANGE=ranges[val].replace(':', '\t')))
footprint.close()

## setup of physics model
os.system("limit.py --multidim-fit --setupOnly --physics-model '{MODEL}' --physics-model-options '{OPT}' {DIR}".format(
    MODEL = options.fitModel, OPT = options.fitModelOptions, DIR = input))
## prepare submission scripts
os.system("mkdir %s" % options.name)
submit_name = '%s_submit.sh' % options.name
with open(submit_name, 'w') as submit_script:
    if options.lxq :
        submit_script.write('export scram_arch=$SCRAM_ARCH\n')
        submit_script.write('export cmssw_base=$CMSSW_BASE\n')
    for idx in range(int(njobs)) :
        log.info("Generating submission script for %s", args[0])
        script_file_name = '%s/submit_%i.sh' % (options.name, idx)
        with open(script_file_name, 'w') as script:
            script.write(script_template.format(
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
            if options.lxq :
                submit_script.write('qsub -l h_vmem=4000M -l site=hh %s -v scram_arch -v cmssw_base %s/%s\n'
                                    % (options.bsub, os.getcwd(), script_file_name))
            else:
                submit_script.write('bsub {QUEUE} -oo /tmp/{USER}/%J.log {PATH}/{FILE}\n'.format(
                    QUEUE=options.bsub, USER=os.environ['USER'], PATH=os.getcwd(), FILE=script_file_name))
os.system('chmod a+x %s' % submit_name)
## execute 
os.system('./%s' % submit_name)
## store
os.system('mv %s %s' % (submit_name, options.name))
