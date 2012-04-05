#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3",
                      description="Script to create a consistent set of a submission script and a crab configuration file for batch job submission at lxbatch, condor or via the grid. The name of the submission script and configuration file can be changed via command line. Note that batch job submission to condor is not yet tested. The script uses combine with method -M HybridNew, which imples that before the limit calculation a grid of signal strength points has to be calculated from which the limit will be derived later on. This grid corresponds to different hypotheses of signal strength. Values in between will be derived by interpolation. This script is called from the script submit_.py in the same package with option --method CLs. ARG1 corresponds to the workspace in form of a root input file containing the RooFit model or a human readable datacard in txt format. ARG2 and ARG3 correspond to the lower and upper boundary between which the signal strength grid is being created. The number of points of this grid can be changed via option -n.")
## direct options
parser.add_option("-o", "--out", dest="out", default="batch", type="string", help="Name of the output files (.sh and .cfg). [Default: batch]")
parser.add_option("-n", "--points", dest="points", default=11, type="int", help="Number of points for the CLs significance grip (including arg2 and arg3 as starting and endpoint). [Default: 11]")
parser.add_option("-I", "--interleave", dest="interl", default=1, type="int", help="If >1, excute only 1/I of the points in each job. [Default: 1]")
parser.add_option("-l", "--log", dest="log", default=False, action="store_true", help="Use a log-scale grid. [Default: False]")
parser.add_option("-r", "--random", dest="random", default=False, action="store_true", help="Use random seeds for the jobs. [Default: False]")
parser.add_option("-s", "--smart", dest="smart", default=False, action="store_true", help="Run more toys at low edge of the band, to get better estimates for the low range. [Default: False]")
parser.add_option("-v", "--verbose", dest="v", default=0, type="int", help="Verbosity level of combine [Default: 0]")
parser.add_option("--shape", dest="shape", default="shape2", type="string", help="Choose dedicated algorithm for shape uncertainties. [Default: 'shape2']")
parser.add_option("--noSystematics", dest="nosys", default=False, action="store_true", help="Use statistical uncertainties only. [Default: False]")
## combine options
egroup = OptionGroup(parser, "COMBINE (HybridNew) COMMAND OPTIONS", "Command options for the use of combine with method -M NewHybrid.")
egroup.add_option("-m", "--mass", dest="mass", default=120, type="int", help="Masspoint (needed for hgg datacards(from submit_.py this parameter is passed on internally). [Default: 120]")
egroup.add_option("-O", "--options", dest="options", default="--freq", type="string", help="Additional options to be used for combine. [Default: '--freq']")
egroup.add_option("-T", "--toysH", dest="T", default=500, type="int", help="Toys per point and per iteration. [Default: 500]")
egroup.add_option("--noPrefit", dest="nofit", default=False, action="store_true", help="Don't apply a fit before running the toys. [Default: False]")
parser.add_option_group(egroup)
## crab cfg parameters
cgroup = OptionGroup(parser, "CRAB CONFIGURATION OPTIONS", "Options for the configuration of the crab configuration file. Note that all of these parameters can be changed in the batch.cfg file later on.")
cgroup.add_option("-t", "--toys", dest="t", default=50, type="int", help="Total number of toys (can be changed in .cfg file). [Default: 50]")
cgroup.add_option("-j", "--jobs", dest="j", default=10, type="int", help="Total number of jobs (can be changed in .cfg file). [Default: 10]")
cgroup.add_option("--server", dest="server", default=False, action="store_true", help="Use crab server. [Default: False]")
cgroup.add_option("--lsf", dest="lsf", default=False, action="store_true", help="Run on LSF instead of GRID (can be changed in .cfg file). [Default: True]")
cgroup.add_option("--condor", dest="condor", default=False, action="store_true", help="Run on condor_g instead of GRID (can be changed in .cfg file). [Default: False]")
cgroup.add_option("--glidein", dest="glide", default=False, action="store_true", help="Use glide-in scheduler instead of glite. [Default: False]")
cgroup.add_option("-q", "--queue", dest="queue", default="8nh", type="string", help="LSF queue to use (can be changed in .cfg file). [Default: 8nh]")
cgroup.add_option("-P", "--priority", dest="prio", default=False, action="store_true", help="Use priority user role")
parser.add_option_group(cgroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) != 3:
    parser.print_usage()
    exit(1)

from math import *
import os

## No fork in batch jobs for now
options.fork = 1 

## convert set of inputcards and corresponding input files for a RooFit workspace
workspace = args[0]
if workspace.endswith(".txt"):
    os.system("text2workspace.py --default-morphing=%s -m %s -b %s -o %s.root" % (options.shape, options.mass, workspace, options.out))
    workspace = options.out+".root"
    print "Converted workspace to binary",workspace

## determine grid of significances from min and max
min, max = float(args[1]), float(args[2])
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
if options .nofit :
  opts+= " --fitNuisances 0"

for i,x in enumerate(points):
    seed = ("$((%d + $i))" % (i*10000)) if options.random == False else "-1"
    interleave = "(( ($i + %d) %% %d == 0 )) && " % (i, options.interl)
    toys = "$n"
    if options.smart:
        if i < 0.25 * options.points:
            toys = "$(( 4 * $n ))";
        elif i < 0.4 * options.points:
            toys = "$(( 2 * $n ))";
    script.write("{cond} ./combine {wsp} -M HybridNew {opts} --fork {fork} -T {T} --clsAcc 0 -m {mass} -v {v} -n {out} --saveHybridResult --saveToys -s {seed} -i {toys} --singlePoint {x} {opt}\n".format(
                wsp=workspace, opts=options.options, fork=options.fork, T=options.T, mass=options.mass, seed=seed, out=options.out, x=x, v=options.v,
                cond=interleave, toys=toys, opt=opts
              ))

script.write("\n");
script.write("hadd %s_grid.root higgsCombine*.root\n" % options.out)
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
additional_input_files = combine,{wsp}
return_data = 1
""".format(wsp=workspace, out=options.out, sched=sched, srv=(1 if options.server else 0), queue=options.queue, jobs=options.j, total=options.t))

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
