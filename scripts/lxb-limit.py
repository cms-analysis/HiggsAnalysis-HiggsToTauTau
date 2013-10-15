#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGs", description="This is a script for simple job submission of limit.py processes to lxb/lxq. It is e.g. called from submit.py, when running this script in batch mode for several main options. The arguments ARGs correspond to the directories that are meant to be processed by limit.py")
##
## MAIN OPTIONS
##
parser.add_option("--name", dest="name", default="batch", type="string",
                  help="Add the job name here. [Default: \"batch\"]")
parser.add_option("--limit-options", dest="limit", default="", type="string",
                  help="Add all options you want to pass to limit.py encapsulated by quotation marks '\"'. [Default: \"\"]")
parser.add_option("--batch-options", dest="batch", default="", type="string",
                  help="Add all options you want to pass to lxb/lxq encapsulated by quotation marks '\"'. [Default: \"\"]")
parser.add_option("--lxq", dest="lxq", default=False, action="store_true",
                  help="Specify this option when running on lxq instead of lxb. [Default: False]")
parser.add_option("--condor", dest="condor", default=False, action="store_true",
                  help="Specify this option when running on condor instead of lxb. [Default: False]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import sys
import glob
import random
import string
import subprocess

import logging
log = logging.getLogger("lxb-limit")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

#dirglob = args[0]
name = options.name
bsubargs = options.batch
option_str = options.limit

# If we are using CONDOR, make sure any card creation happens in a writable
# directory.
if options.condor:
    option_str = " ".join([option_str, "--working-dir=${_CONDOR_SCRATCH_DIR}"])

## prepare log file directory
os.system("mkdir -p log")

script_template = '''#!/bin/bash

cd {working_dir}
eval `scram runtime -sh`

echo "Running limit.py:"
echo "with options {options}"
echo "in directory {dirhead}{tail}"

echo "Copy {dirhead}{tail} --> {tmphead}/{tail}"
mkdir -p {tmphead}
cp -r {dirhead}{tail} {tmphead}/{tail}
cp -r {dirhead}common {tmphead}

echo "Running"
$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/limit.py {options} {tmphead}/{tail}

echo "Copy {tmphead}/{tail} --> {dirhead}{tail} (root output files only)"
cp {tmphead}/{tail}/*.root {dirhead}{tail}
if [ -d {tmphead}/{tail}/out ] ;
  then
    mkdir -p {dirhead}/{tail}/out ;
    cp -u {tmphead}/{tail}/out/*.* {dirhead}/{tail}/out ;
fi
rm -r {tmphead}
'''

lxq_fragment = '''#!/bin/bash
export SCRAM_ARCH=$scram_arch
ini cmssw_cvmfs
ini autoproxy
'''

condor_sub_template = '''
log = condor.log
notification = never
getenv = true
## make sure AFS is accessible and suppress the default FilesystemDomain requirements of Condor
requirements = HasAFS_OSG && TARGET.FilesystemDomain =!= UNDEFINED && TARGET.UWCMS_CVMFS_Revision >= 0 && TARGET.CMS_CVMFS_Revision >= 0

'''


if options.lxq :
    script_template = script_template.replace('#!/bin/bash', lxq_fragment)
elif options.condor:
    pass
else: # user wants to run on lsf
    pass
    #sub = subprocess.Popen(['bsub'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stderr = ''
    #if stderr.startswith('bsub error'):
    #    errmsg = 'lxb-limit.py: if you want to run on lsf, you need to log to lxplus. ABORTING'
    #    print errmsg
    #    # raise ValueError(errmsg)
    #    sys.exit(1)

## create a random stamp fro multiply submission
stamp=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
## main submission script
submit_name = '%s_submit.sh' % name
with open(submit_name, 'w') as submit_script:
    if options.condor:
        submit_script.write(condor_sub_template)
    if options.lxq :
        submit_script.write('export scram_arch=$SCRAM_ARCH\n')
        submit_script.write('export cmssw_base=$CMSSW_BASE\n')
    if not os.path.exists(name):
        os.system("mkdir -p %s" % name)
    for i, dir in enumerate(args):
        ## don't submit jobs on old LSF output
        if 'LSFJOB' in dir:
            continue
        if 'common' in dir:
            continue
        log.info("Generating submission script for %s", dir)
        script_file_name = '%s/%s_%i.sh' % (name, name, i)
        ## create random directory in tmp. This allows to do more than one submission in parallel
        tmp_head = '/tmp/'+stamp
        if options.condor:
            tmp_head = "${_CONDOR_SCRATCH_DIR}/" + stamp
        dir_head = dir.rstrip('/')[:dir.rstrip('/').rfind('/')+1]
        dir_tail = dir.rstrip('/')[dir.rstrip('/').rfind('/')+1:]
        with open(script_file_name, 'w') as script:
            script.write(
                script_template.format(
                working_dir=os.getcwd(),
                options=option_str,
                dirhead=dir_head,
                tmphead=tmp_head,
                tail=dir_tail
                ))
        os.system('chmod a+x %s' % script_file_name)
        if options.condor :
            submit_script.write("\n")
            submit_script.write(
                "executable = %s/%s\n" % (os.getcwd(), script_file_name))
            submit_script.write(
                "output = %s/%s\n" % (
                    os.getcwd(), script_file_name.replace('.sh', '.stdout')))
            submit_script.write(
                "error = %s/%s\n"
                % (os.getcwd(), script_file_name.replace('.sh', '.stderr')))
            submit_script.write("queue\n")
        elif options.lxq :
            submit_script.write('qsub -l site=hh -l h_vmem=4000M %s -v scram_arch -v cmssw_base %s\n'
                                % (bsubargs, script_file_name))
        else :
            os.system('touch {PWD}/log/{LOG}'.format(
                PWD=os.getcwd(), LOG=script_file_name[script_file_name.rfind('/')+1:].replace('.sh', '.log')))
            submit_script.write('bsub {QUEUE} -oo {PATH}/log/{LOG} {PATH}/{FILE}\n'.format(
                QUEUE=bsubargs, LOG=script_file_name[script_file_name.rfind('/')+1:].replace('.sh', '.log'), PATH=os.getcwd(), FILE=script_file_name))
os.system('chmod a+x %s' % submit_name)
