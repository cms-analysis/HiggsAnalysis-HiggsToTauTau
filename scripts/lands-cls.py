#!/usr/bin/env python
from math import *
import os
from optparse import OptionParser, OptionGroup
import ROOT

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] args",
                      description="Script to create a consistent set of a submission script and a crab configuration file for batchjob submission at lxbatch, condor or via grid. The name of the submission script and configuration file can be changed via command line. Note that batchjob submission to condor is not yet tested. The script uses the lands executable with the CLs method, which implies that before the limit calculation a grid has to be calculated from which the limit will be derived later on. This grid corresponds to different hypotheses of signal strength. Values in between will be derived by interpolation. The arguments passed on to this script correspond to the datacards to be passed on to lands.")
## direct options
parser.add_option("-o", "--out", dest="out", default="batch", type="string", help="Name of the output files. [Default: batch]")
parser.add_option("-n", "--points", dest="points", default=11, type="int", help="Number of points for the CLs significance grip (including arg2 and arg3 as starting and endpoint). [Default: 10]")
parser.add_option("-l", "--log", dest="log", default=False, action="store_true", help="Use a log-scale grid. [Default: False]")
parser.add_option("-r", "--random", dest="random", default=False, action="store_true", help="Use random seeds for the jobs. [Default: False]")
parser.add_option("-v", "--verbose", dest="v", default=0, type="int", help="Verbosity level of lands [Default: 0]")
parser.add_option("--noSystematics", dest="nosys", default=False, action="store_true", help="Use statistical uncertainties only. [Default: False]")
## lands options
egroup = OptionGroup(parser, "LANDS (HYBRID/CLs) COMMAND OPTIONS", "Command options for the use of lands with the NewHybrid/CLs method.")
egroup.add_option("--minR", dest="minR", default=0.5, type="string", help="Minimum of signal strength grid. [Default: 0.5]")
egroup.add_option("--maxR", dest="maxR", default=30., type="string", help="Maximum of signal strength grid. [Default: 30.]")
parser.add_option_group(egroup)
## crab cfg parameters
cgroup = OptionGroup(parser, "CRAB CONFIGURATION OPTIONS", "Options for the configuration of the crab configuration file. Note that all of these parameters can be changed in the batch.cfg file later on.")
cgroup.add_option("-t", "--toys", dest="t", default=50, type="int", help="Total number of iterations per point in the CLs significance grid to be distributed among all jobs (can be changed in .cfg file). [Default: 50]")
cgroup.add_option("-j", "--jobs", dest="j", default=10, type="int", help="Total number of jobs (can be changed in .cfg file). [Default: 10]")
cgroup.add_option("-i", "--input", dest="input", default="input.root", type="string", help="Name of the root input file(s). If more than one file it has to be a comma separated list in of type: 'file1.root, file2.root, file2.root'. [Default: input.root]")
cgroup.add_option("--server", dest="server", default=False, action="store_true", help="Use crab server. [Default: False]")
cgroup.add_option("--lsf", dest="lsf", default=False, action="store_true", help="Run on LSF instead of GRID (can be changed in .cfg file). [Default: True]")
cgroup.add_option("--condor", dest="condor", default=False, action="store_true", help="Run on condor_g instead of GRID (can be changed in .cfg file). [Default: False]")
cgroup.add_option("--glidein", dest="glide", default=False, action="store_true", help="Use glide-in scheduler instead of glite. [Default: False]")
cgroup.add_option("-q", "--queue", dest="queue", default="8nh", type="string", help="LSF queue to use (can be changed in .cfg file). [Default: 8nh]")
cgroup.add_option("-P", "--priority", dest="prio", default=False, action="store_true", help="Use PriorityUser role")
parser.add_option_group(cgroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1:
    parser.print_usage()
    exit(1)

## create string of datacards for job submission script (not ',' seperated)
cards = " "
for card in args:
    cards += card
    cards += " "
    
## determine grid of significances from min and max
min, max = float(options.minR), float(options.maxR)
dx = (max-min)/(options.points-1)
points = [ min + dx*i for i in range(options.points) ]

if options.log:
    dx = log(max/min)/(options.points-1)
    points = [ min * exp(dx*i) for i in range(options.points) ]

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

## prepare optional options
opts = ""
if options.nosys :
  opts+= " -S 0"

for i,x in enumerate(points):
    seed = "$i" if options.random == False else "-1"
    ## setup intermediate filename
    script.write("./lands -d {model} -M Hybrid --freq --bNotCalcCLssbb --bSaveM2lnQ --nToysForCLsb $n --nToysForCLb $n --singlePoint {x} -s {seed} -n {out}\n".format(
    model=cards, x=x, seed=seed, out="higgsLands_%d.root" % i
    ))
script.write("\n");
script.write("hadd %s_grid.root higgsLands*.root\n" % options.out)
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
output_file = {out}_grid.root
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

ce_white_list    = T2, T3_US_UCD
ce_black_list    = T2_CN_Beijing, T2_RU, T2_SU, T2_UA, T2_PK, T2_PL_Cracow, T2_UK_SGrid_Bristol
""")
cfg.close()
