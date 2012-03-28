#!/usr/bin/env python
import os
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] arg1 arg2 arg3 ...",
                      description="Script to create a consistent set of a submission script and a crab configuration file for batch job submission at lxbatch, condor or via the grid. The name of the submission script and configuration file can be changed via the command option line. Note that batch job submission to condor is not yet tested.  The script uses the lands executable with the Bayesian method. It is preferentially called from the submit_.py script. The arguments [args] correspond to the datacards that form the model.")
## direct options
parser.add_option("-o", "--out", dest="out", default="batch", type="string", help="Name of the output files. [Default: batch]")
parser.add_option("-v", "--verbose", dest="v", default=0, type="int", help="Verbosity level of lands. [Default: 0]")
parser.add_option("-r", "--random", dest="random", default=False, action="store_true", help="Use random seeds for the jobs. [Default: False]")
## lands options
lgroup = OptionGroup(parser, "LANDS (BAYESIAN) COMMAND OPTIONS", "Command options for the use of LandS with the Bayesian method.")
lgroup.add_option("-b", "--bands", dest="bands", default=1, type="int", help="--doExpectation 1; this has to be 0 or 1. [Default: 1]")
lgroup.add_option("-T", "--toysB", dest="nuisance", default=1000, type="int", help="Toys to integrate out the nuisance parameters of the model. [Default: 1000]")
parser.add_option_group(lgroup)
## crab cfg parameters
cgroup = OptionGroup(parser, "CRAB CONFIGURATION OPTIONS", "Options for the configuration of the crab configuration file. Note that all of these parameters can be changed in the batch.cfg file later on.")
cgroup.add_option("-t", "--toys", dest="t", default=1000, type="int", help="Total number of toys summed over all jobs (can be changed in .cfg file). [Default: 1000]")
cgroup.add_option("-j", "--jobs", dest="j", default=10, type="int", help="Total number of jobs (can be changed in .cfg file). [Default: 10]")
cgroup.add_option("-i", "--input", dest="input", default="input.root", type="string", help="Name of the root input file(s). If more than one file it has to be a comma separated list in of type: 'file1.root, file2.root, file2.root'. [Default: input.root]")
cgroup.add_option("--server", dest="server", default=False, action="store_true", help="Use crab server. [Default: False]")
cgroup.add_option("--lsf", dest="lsf", default=True, action="store_true", help="Run on LSF instead of GRID (can be changed in .cfg file). [Default: True]")
cgroup.add_option("--condor", dest="condor", default=False, action="store_true", help="Run on condor_g instead of GRID (can be changed in .cfg file). [Default: False]")
cgroup.add_option("--glidein", dest="glide", default=False, action="store_true", help="Use glide-in scheduler instead of glite. [Default: False]")
cgroup.add_option("-q", "--queue", dest="queue", default="8nh", type="string", help="LSF queue to use (can be changed in .cfg file). [Default: 8nh]")
cgroup.add_option("-P", "--priority", dest="prio", default=False, action="store_true", help="Use PriorityUser role (this is not supported by submitBatchjob.py)")
parser.add_option_group(cgroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

## create string of datacards for job submission script (not ',' seperated)
cards = " "
for card in args:
    cards += card
    cards += " "

## create job submission script
print "> creating executable script ",options.out+".sh"
script = open(options.out+".sh", "w")
script.write("""
#!/bin/bash

i="$1"
if [ "$i" = "" ]; then
  echo "Error: missing job index"
  exit 1;
fi
echo "max events from CRAB: $MaxEvents"
n="$MaxEvents"
if [ "$n" = "" ]; then
  n="$2"
fi
if [ "$n" = "" ]; then
  echo "Error: missing number of experiments"
  exit 2;
fi

echo "## Starting at $(date)"
""")
seed = "$i" if options.random == False else "-1"
script.write("./lands -M Bayesian -d {model} -n {name} --doExpectation {exp} -tB {nuisance} -t $n -s {seed} -v {v}".format(
                model=cards, name=options.out, exp=options.bands, nuisance=options.nuisance, v=options.v, seed=seed))
script.write('\n');
script.write('echo "## Done at $(date)"\n');
script.close()
os.system("chmod +x %s.sh" % options.out)

## define scheduler
sched = "glite"
if options.lsf: sched = "lsf"
if options.condor: sched = "condor"
if options.glide: sched = "glidein"

## create string of crab configuration file (',' seperated)
workspace = " "
for card in args:
    if card == args[0] :
        workspace += card
    else :
        workspace += ", "
        workspace += card

## create crab configuration file for job submission
print "> creating crab cfg ",options.out+".cfg"
cfg = open(options.out+".cfg", "w")
cfg.write("""
[CRAB]
jobtype = cmssw
scheduler = {sched}
use_server = {srv}

[LSF]
queue = {queue}

[CMSSW]
datasetpath = None
pset = None
output_file = {out}_limits_tree.root 
total_number_of_events = {total}
number_of_jobs = {jobs}

[USER]
script_exe = {out}.sh
additional_input_files = lands,{wsp},{input}
return_data = 1
""".format(wsp=workspace, input=options.input, out=options.out, sched=sched, srv=(1 if options.server else 0), queue=options.queue, jobs=options.j, total=options.t))

if options.prio: cfg.write("""
[GRID]
rb               = CERN
proxy_server     = myproxy.cern.ch
role             = priorityuser
retry_count      = 0
maxtarballsize   = 250

ce_white_list    = T2, T3_US_UCD
ce_black_list    = T2_CN_Beijing, T2_RU, T2_SU, T2_UA, T2_PK, T2_PL_Cracow, T2_UK_SGrid_Bristol
""")
cfg.close()
