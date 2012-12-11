#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="This is a script to submit a set of jobs to set up the datacards structure for direct mA-tanb limit calculation to lxb (lxq)")
parser.add_option("--name", dest="name", default="setup-tanb", type="string",
                  help="Set the name of the submission. All scripts concerned with the submission will be located in a directory with that name in your working directory. [Default: \"setup-tanb\"]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import sys
import glob

import logging
log = logging.getLogger("lxb-tanb-setup")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

name = options.name
dirglob = args

## tamplate for the submission script
script_template = '''
#!/usr/bin/bash

cd {working_dir}
eval `scram runtime -sh`

echo "Running submit.py:"
echo "in directory {directory}"

$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/submit.py --tanb+ --setup {directory}
'''

def submit(name, dirs) :
    '''
    prepare the submission script
    '''
    submit_name = '%s_submit.sh' % name
    if not os.path.exists(name):
        os.system("mkdir %s" % name)
    with open(submit_name, 'w') as submit_script:
        for dir in dirs :
            for i, dir in enumerate(glob.glob(dir+'/*')):
                if not is_number(dir[dir.rstrip('/').rfind('/')+1:]) :
                    continue
                ## do not submit jobs on old LSF output
                if 'LSFJOB' in dir:
                    continue
                log.info(" Generating submision script for %s", dir)
                script_file_name = '%s/%s_%i.sh' % (name, name, i)
                with open(script_file_name, 'w') as script:
                    script.write(script_template.format(
                        working_dir = os.getcwd(),
                        directory = dir
                        ))
                os.system('chmod a+x %s' % script_file_name)
                submit_script.write('bsub -q 8nh %s\n' % script_file_name)
                os.system('chmod a+x %s' % submit_name)

def get_mass(directory) :
    '''
    Returns the mass from a directory string. directories
    are expected to end with a floating point number of
    with an integer number. Trailing slashes are removed.
    The mass is returned as a string.
    '''
    idx = directory.rfind("/")
    if idx == (len(directory) - 1):
        idx = directory[:idx - 1].rfind("/")
    mass  = directory[idx + 1:]
    return mass.rstrip('/')

def is_number(s):
    '''
    check if the string is a number or not (works for int and float)
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False

dirs = []
for dir in args :
    ## chop off masses directory if present as this will be added automatically by the submission script
    if is_number(get_mass(dir)) or get_mass(dir) == "common" :
        dir = dir[:dir.rstrip('/').rfind('/')]
    if not dir in dirs :
        dirs.append(dir)

for dir in dirs:
    ana = dir[:dir.rfind('/')]
    limit = dir[len(ana)+1:]
    jobname = ana[ana.rfind('/')+1:]+'-'+limit+'-'+options.name
    ## create submission scripts
    submit(jobname, dirs)
    ## execute
    #os.system("./{JOBNAME}_submit.sh".format(JOBNAME=jobname))
    ## shelve
    os.system("mv {JOBNAME}_submit.sh {JOBNAME}".format(JOBNAME=jobname))


