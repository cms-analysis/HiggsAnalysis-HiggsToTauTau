#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="Script to create a consistent set of a submission script and a crab configuration file for batch job submission at lxbatch, condor or via grid. The name of the submission script and configuration file can be changed via command line. Note that batch job submission to condor is not yet tested. The script uses combine with method -M MarkovChainMC. It is called from the script submit_.py in the same package with option --method bayesian. The argument ARG corresponds to the workspace in form of a root input file containing the RooFit model or a human readable datacard in txt format.")
## direct options
parser.add_option("-o", "--out", dest="out", default="batch", type="string", help="Name of the output files (.sh and .cfg). [Default: batch]")
parser.add_option("-r", "--random", dest="random", default=False, action="store_true", help="Use random seeds for the jobs. [Default: False]")
parser.add_option("-v", "--verbose", dest="v", default=0, type="int", help="Verbosity level of combine. [Default: 0]")
parser.add_option("--noSystematics", dest="nosys", default=False, action="store_true", help="Use statistical uncertainties only. [Default: False]")
## combine options
egroup = OptionGroup(parser, "COMBINE (MarkovChainMC) COMMAND OPTIONS", "Command options for the use of combine with method -M MarkovChain.")
egroup.add_option("-m", "--mass", dest="mass", default=120, type="int", help="Masspoint (needed to return the output histogram via crab; from the script submit_.py this parameter is passed on internally). [Default: 120]")
egroup.add_option("--hint", dest="hint", default="Asymptotic", type="string", help="Name of the hint method that is used to guide the MarkovChainMC. [Default: Asymptotic]")
egroup.add_option("--rMin", dest="rMin", default="0.1", type="string", help="Minimum value of signal strenth. [Default: 0.1]")
egroup.add_option("--rMax", dest="rMax", default="100", type="string", help="Maximum value of signal strenth. [Default: 100]")
egroup.add_option("--iterations", dest="iter", default=10000, type="int", help="Number of iterations to integrate out nuisance parameters. [Default: 10000]")
egroup.add_option("--tries", dest="tries", default=10, type="int", help="Number of tries to run the MarkovChainMC on the same data. [Default: 10]")
egroup.add_option("--observed", dest="observed", default=False, action="store_true", help="Calculate the observed limit via crab (in case this is time consuming). [Default: False]")
parser.add_option_group(egroup)
## crab cfg parameters
cgroup = OptionGroup(parser, "CRAB CONFIGURATION OPTIONS", "Options for the configuration of the crab configuration file. Note that all of these parameters can be changed in the batch.cfg file later on.")
cgroup.add_option("-t", "--toys", dest="t", default=50, type="int", help="Total number of toys (can be changed in .cfg file). [Default: 50]")
cgroup.add_option("-j", "--jobs", dest="j", default=10, type="int", help="Total number of jobs (can be changed in .cfg file). [Default: 10]")
cgroup.add_option("--server", dest="server", default=False, action="store_true", help="Use crab server. [Default: False]")
cgroup.add_option("--lsf", dest="lsf", default=False, action="store_true", help="Run on LSF instead of GRID (can be changed in .cfg file). [Default: False]")
cgroup.add_option("--condor", dest="condor", default=False, action="store_true", help="Run on condor_g instead of GRID (can be changed in .cfg file). [Default: False]")
cgroup.add_option("--glidein", dest="glide", default=False, action="store_true", help="Use glide-in scheduler instead of glite. [Default: False]")
cgroup.add_option("-q", "--queue", dest="queue", default="8nh", type="string", help="LSF queue to use (can be changed in .cfg file). [Default: 8nh]")
cgroup.add_option("-p", "--priority", dest="prio", default=False, action="store_true", help="Use priority user role")
parser.add_option_group(cgroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) != 1:
    parser.print_usage()
    exit(1)

from math import *
import os
import random

## No fork in batch jobs for now
options.fork = 1 

## convert set of inputcards and corresponding input files for a RooFit workspace
workspace = args[0]
if workspace.endswith(".txt"):
    os.system("text2workspace.py -b %s -o %s.root" % (workspace, options.out))
    workspace = options.out+".root"
    print "Converted workspace to binary",workspace

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

## prepare random seed(s); NOTE that each individual seed
## will be used later again to get the output from crab
random.seed()
rand = random.randint(1, 999999)
seed = "$i" if options.random == False else ("$[%s+$i]" % rand)

## prepare optional options
opts = ""
if options.nosys :
  opts+= "-S 0"
  
## continue in executable script
if options.observed :
   script.write("./combine -M MarkovChainMC -H {hint} --rMin {rMin} --rMax {rMax} -i {iter} --tries {tries} --mass 999 -d {model} -v {v}".format(
   model=workspace, hint=options.hint, rMin=options.rMin, rMax=options.rMax, tries=options.tries, iter=options.iter, v=options.v))
else :
   script.write("./combine -M MarkovChainMC {hint} --rMin {rMin} --rMax {rMax} -i {iter} --tries {tries} --mass {mass} -d {model} -t $n -s {seed} -v {v} {opts}".format(
   model=workspace, hint=("-H %s" % options.hint) if not options.hint == "None" else "", rMin=options.rMin, rMax=options.rMax, tries=options.tries, iter=options.iter, mass=options.mass, v=options.v, seed=seed, opts=opts))
script.write("\n");
script.write('echo "## Done at $(date)"\n');
script.close()
os.system("chmod +x %s.sh" % options.out)

## create a link for combine
if not os.path.exists("combine"):
    print "Creating a symlink to the combine binary"
    os.system("cp -s $(which combine) .")

## create string of potential outputfiles, for observed this is
## a simple case, for the toys the seed to the random number
## generator needs to be reflected properly in the output
## name of the file  
ifile = 0
outputfiles = ""
if options.observed :
    outputfiles = "higgsCombineTest.MarkovChainMC.mH999.root"
else :
    while ifile<options.j :
        iseed = ifile
        if options.random :
            iseed = rand+ifile
        outputfiles+="higgsCombineTest.MarkovChainMC.mH{mass}.{iseed}.root".format(mass=options.mass, iseed=iseed)
        outputfiles+=","
        ifile=ifile+1
    outputfiles=outputfiles.rstrip(",")

## define scheduler
sched = "glite"
if options.lsf: sched = "lsf"
if options.condor: sched = "condor"
if options.glide: sched = "glidein"

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
output_file = {outputfile}
total_number_of_events = {total}
number_of_jobs = {jobs}

[USER]
script_exe = {out}.sh
additional_input_files = combine,{wsp}
return_data = 1
""".format(outputfile=outputfiles, wsp=workspace, mass=options.mass, out=options.out, sched=sched, srv=(1 if options.server else 0),
           queue=options.queue, jobs=(1 if options.observed else options.j), total=(1 if options.observed else options.t)))

if options.prio: cfg.write("""
[GRID]
rb               = CERN
proxy_server     = myproxy.cern.ch
retry_count      = 0
maxtarballsize   = 250

ce_white_list    = T2, T3_US_UCD
ce_black_list    = T2_CN_Beijing, T2_RU, T2_SU, T2_UA, T2_PK, T2_PL_Cracow, T2_UK_SGrid_Bristol
""")
cfg.close()
