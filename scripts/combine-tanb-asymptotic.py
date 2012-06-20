#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG1",
                      description="Script to create a consistent set of a submission script and a crab configuration file for batch job submission at lxbatch, condor or via the grid. The name of the submission script and configuration file can be changed via command line. Note that batch job submission to condor is not yet tested. The script uses combine with the asymptotic CLs option. This script is called from the script submit_.py in the same package with option --method tanb. It works in analogy to the script combine-cls.py, with the main difference that it expects to find an own workspace for each signal strength point in the directory where executed. These workspaces have to produced beforehand. They are expected to correspond to the limit inputs scaled to the anticipated cross section per given value of tanb and divided by the value of tanb. This procedure allows for the calculation of a limit directly in the MSSM parameter tanb. ARG1 corresponds to the workspace in form of a human readable datacard in txt format.")
## direct options
parser.add_option("-o", "--out", dest="out", default="batch", type="string", help="Name of the output files (.sh and .cfg). [Default: batch]")
parser.add_option("-r", "--random", dest="random", default=False, action="store_true", help="Use random seeds for the jobs. [Default: False]")
parser.add_option("-v", "--verbose", dest="v", default=0, type="int", help="Verbosity level of combine [Default: 0]")
parser.add_option("--shape", dest="shape", default="shape2", type="string", help="Choose dedicated algorithm for shape uncertainties. [Default: 'shape2']")
parser.add_option("--noSystematics", dest="nosys", default=False, action="store_true", help="Use statistical uncertainties only. [Default: False]")
## combine options
egroup = OptionGroup(parser, "COMBINE (Asymptotic) COMMAND OPTIONS", "Command options for the use of combine with method -M Asymptotic.")
egroup.add_option("-m", "--mass", dest="mass", default=120, type="int", help="Masspoint (needed for hgg datacards(from submit_.py this parameter is passed on internally). [Default: 120]")
egroup.add_option("-O", "--options", dest="options", default="--minosAlgo stepping", type="string", help="Additional options to be used for combine. [Default: '--minosAlgo stepping']")
egroup.add_option("--noPrefit", dest="nofit", default=False, action="store_true", help="Don't apply a fit before running the toys. [Default: False]")
parser.add_option_group(egroup)
## crab cfg parameters
cgroup = OptionGroup(parser, "CRAB CONFIGURATION OPTIONS", "Options for the configuration of the crab configuration file. Note that all of these parameters can be changed in the batch.cfg file later on.")
cgroup.add_option("--server", dest="server", default=False, action="store_true", help="Use crab server. [Default: False]")
cgroup.add_option("--lsf", dest="lsf", default=False, action="store_true", help="Run on LSF instead of GRID (can be changed in .cfg file). [Default: True]")
cgroup.add_option("--condor", dest="condor", default=False, action="store_true", help="Run on condor_g instead of GRID (can be changed in .cfg file). [Default: False]")
cgroup.add_option("--glidein", dest="glide", default=False, action="store_true", help="Use glide-in scheduler instead of glite. [Default: False]")
cgroup.add_option("-q", "--queue", dest="queue", default="8nh", type="string", help="LSF queue to use (can be changed in .cfg file). [Default: 8nh]")
cgroup.add_option("-P", "--priority", dest="prio", default=False, action="store_true", help="Use priority user role")
parser.add_option_group(cgroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) != 1:
    parser.print_usage()
    exit(1)

from math import *
import os

## No fork in batch jobs for now
options.fork = 1

## convert set of inputcards and corresponding input files for a RooFit workspace
workspace = args[0]
workspaces=[]
if workspace.endswith(".txt"):
    inputname = workspace
    outputname = "%s.root" % (options.out)
    #os.system("text2workspace.py --default-morphing=%s -m %s -b %s -o %s" % (options.shape, options.mass, inputname, outputname))
    # TEMP DEBUG FIXME
    os.system("text2workspace.py --X-no-check-norm --default-morphing=%s -m %s -b %s -o %s" % (options.shape, options.mass, inputname, outputname))
    workspaces.append(outputname)
print "Converted workspaces to binary",workspaces

## create job submission script
print "> creating executable script ",options.out+".sh"
script = open(options.out+".sh", "w")
script.write("""
#!/bin/bash

echo "## Starting at $(date)"
""")

## prepare optional options
opts = ""
if options.nosys :
  opts+= " -S 0"
if options.nofit :
  opts+= " --fitNuisances 0"

seed = 0xBEEF
if options.random:
    seed = -1

script.write("./combine {wsp} -M Asymptotic {opts} --fork {fork} -m {mass} -v {v} -n {out} -s {seed} {opt}\n".format(
    wsp=workspaces[0], opts=options.options, fork=options.fork, mass=options.mass, seed=seed, out=options.out, v=options.v,
    opt=opts
))

script.write("\n");
# There will be only one output, but this works as well
script.write("hadd %s.root higgsCombine*.root\n" % options.out)
script.write('echo "## Done at $(date)"\n');
script.close()
os.system("chmod +x %s.sh" % options.out)

## create a link for combine
if not os.path.exists("combine"):
    print "Creating a symlink to the combine binary"
    os.system("cp -s $(which combine) .")

## define scheduler
sched = "glite"
if options.lsf: sched = "lsf"
if options.condor: sched = "condor"
if options.glide: sched = "glidein"

## create string of workspaces for crab submission script
wsps = ""
for wsp in workspaces:
    wsps += wsp
    wsps += ","
wsps=wsps.rstrip(",")

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
output_file = {out}.root
total_number_of_events = 1
number_of_jobs = 1

[USER]
script_exe = {out}.sh
additional_input_files = combine,{wsps}
return_data = 1
""".format(wsps=wsps, out=options.out, sched=sched, srv=(1 if options.server else 0), queue=options.queue))

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
