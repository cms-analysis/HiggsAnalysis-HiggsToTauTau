#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...",
                      description="Script to submit crabjobs to a batch system. This system can be lxbatch, condor or the grid. Note that condor submission has not been validated yet. The script expects a list of submission directories (ARG1, ARG2, ARG2, ...) in which the complete information to execute the tools for limit calculation should be hosted. Each sub-directory is expected to correspond to a single mass point. The script will perform the following actions: visit each of the sub-directories; create the batch submission script and a corresponding crab configuration file; create the jobs and submit. Input files and datacards will be made known to the batch submission script and the configuration file automatically. At the moment the following binaries and methods are supported: land (bayesian); combine (bayesian, CLs, tanb, single). The latter two methods are of type CLs in special configurations to calculate limits directly on tanb in the MSSM parameter space. For complex models like the combination of all Higgs channels even the computation of the observed limit in Bayesian can be time consuming, especially if it has to be done for many mass points. Therefore an extension has been made to allow also to do a batch job submission for the observed limit. This feature can be steered by option --observed, which will result in a subdirectory \"observed\" in the directory of the corresponding mass point in which an additional crabjob will be submitted. By definition this crabjob will contain only one subjob. Options which deal with the number of toys, number of subjobs or toy specifics will be ignored for this submission. Other options will still be applied.")
## direct options
parser.add_option("-o", "--out", dest="out", default="batch", type="string", help="Name of the output files (.sh and .cfg). [Default: batch]")
parser.add_option("-v", "--verbose", dest="v", default=0, type="int", help="Verbosity level of lands or combine. [Default: 0]")
parser.add_option("--binary", dest="binary", default="combine", type="choice", help="Binary file to be used [Default: combine]",  choices=["lands", "combine"])
parser.add_option("--method", dest="method", default="CLs", type="choice", help="Statistical method to be used [Default: CLs]",  choices=["bayesian", "CLs", "tanb", "single", "significance"])
parser.add_option("--shape",           dest="shape",           default="shape2",  type="string",             help="Choose dedicated algorithm for shape uncertainties. [Default: 'shape2']")
parser.add_option("--random", dest="random", default=False, action="store_true", help="Use random seeds. [Default: False]")
parser.add_option("--model", dest="model", default="HiggsAnalysis/HiggsToTauTau/data/out.mhmax-mu+200-{PERIOD}-{tanbRegion}-nnlo.root", type="string", help="The model that should be applied for direct limits on tanb (only applicable for --method tanb, for other methods this option will have no effect). The model should be given as the absolute path to the mssm_xsec_tool input file starting from CMSSW_BASE/src/, or feyn-higgs::saeffm , feyn-higgs::gluoph, ... in case the model is assumed to be picked from feyn-higgs. In the case of feyn-higgs the model tag following the \'::\' will be passed on the the feyn-higgs extration tool feyn-higgs-mssm. [Default: 'HiggsAnalysis/HiggsToTauTau/data/out.mhmax-mu+200-{PERIOD}-{tanbRegion}-nnlo.root']")
parser.add_option("--interpolation", dest="interpolation_mode", default='mode-1', type="choice", help="Mode for mass interpolation for direct limits tanb (only applicable for --method tanb, for other methods this option will have no effect). [Default: mode-1]", choices=["mode-0", "mode-1", "mode-2", "mode-3", "mode-4", "mode-5"])
parser.add_option("--full-mass", dest="full_mass", default=False, action="store_true", help="Do not apply acceptance corrections for masswindow that has been applied for cross section calculation. Kept for legacy. [Default: False]")
parser.add_option("--noSystematics", dest="nosys", default=False, action="store_true", help="Use statistical uncertainties only (currently only implemented for combine). [Default: False]")
## lands options for Bayesian
lgroup = OptionGroup(parser, "LANDS (Bayesian) COMMAND OPTIONS", "Command options for the use of lands with method -M bayesian.")
lgroup.add_option("-b", "--bands", dest="bands", default=1, type="int", help="--doExpectation 1; this has to be 0 or 1. [Default: 1]")
lgroup.add_option("--toysB", dest="nuisance", default=1000, type="int", help="Toys to integrate out the nuisance parameters of the model. [Default: 1000]")
parser.add_option_group(lgroup)
## combine options for Hybrid/CLs
mgroup = OptionGroup(parser, "COMBINE (HybridNew) COMMAND OPTIONS", "Command options for the use of combine with method -M HybridNew.")
mgroup.add_option("-n", "--points", dest="points", default=11, type="int", help="Number of points for the CLs significance grip (including --min and --max as starting and endpoint). [Default: 11]")
mgroup.add_option("-I", "--interleave", dest="interl", default=1, type="int", help="If >1, excute only 1/I of the points in each job. [Default: 1]")
mgroup.add_option("-O", "--options", dest="options", default="--freq", type="string", help="Additional options to be used for combine. [Default: '--freq']")
mgroup.add_option("--toysH", dest="T", default=500, type="int", help="Toys per point and per iteration. [Default: 500]")
mgroup.add_option("--min", dest="min", default="0.5", type="string", help="Minimum value of signal strength. [Default: 0.5]")
mgroup.add_option("--max", dest="max", default="80", type="string", help="Maximum value of signal strength. [Default: 80]")
mgroup.add_option("--noPrefit", dest="nofit", default=False, action="store_true", help="Don't apply a fit before running toys. [Default: False]")
parser.add_option_group(mgroup)
## combine options for MarkovChainMC/Bayesian
ngroup = OptionGroup(parser, "COMBINE (MarkovChainMC) COMMAND OPTIONS", "Command options for the use of combine with method -M MarkovChainMC.")
ngroup.add_option("-H", "--hint", dest="hint", default="Asymptotic", type="string", help="Name of the hint method that is used to guide the MarkovChainMC. [Default: Asymptotic]")
ngroup.add_option("--rMin", dest="rMin", default="0.1", type="string", help="Minimum value of signal strenth. [Default: 0.1]")
ngroup.add_option("--rMax", dest="rMax", default="100", type="string", help="Maximum value of signal strenth. [Default: 100]")
ngroup.add_option("--iterations", dest="iter", default=10000, type="int", help="Number of iterations to integrate out nuisance parameters. [Default: 10000]")
ngroup.add_option("--tries", dest="tries", default=10, type="int", help="Number of tries to run the MarkovChainMC on the same data. [Default: 10]")
ngroup.add_option("--observed", dest="observed", default=False, action="store_true", help="Calculate the observed limit via crab (in case this is time consuming). [Default: False]")
parser.add_option_group(ngroup)
pgroup = OptionGroup(parser, "COMBINE (PROFILE LIKELIHOOD) COMMAND OPTIONS", "Command options for the use of combine with the ProfileLikelihood method.")
pgroup.add_option("--fixed-mass", dest="fixed_mass", default="", type="string", help="Set a fixed mass at which to inject the signal signal (during workspace creation). If the string is empty the mass point is taken for which the significance is calculated. [Default: \"\"]")
pgroup.add_option("--signal-strength", dest="signal_strength", default="1", type="string", help="Set signal strength for expected significance calculation. [Default: \"1\"]")
parser.add_option_group(pgroup)
## crab cfg parameters
cgroup = OptionGroup(parser, "CRAB CONFIGURATION OPTIONS", "Options for the configuration of the crab configuration file. Note that all of these parameters can be changed in the batch.cfg file later on.")
cgroup.add_option("--interactive", dest="interactive",default=False, action="store_true", help="Set to true to run interactive, otherwise the script will submit the job to the grid directly [Default: False]")
cgroup.add_option("-t", "--toys", dest="t", default=1000, type="int", help="Total number of toys. (can be changed in .cfg file). [Default: 1000]")
cgroup.add_option("-j", "--jobs", dest="j", default=10, type="int", help="Total number of jobs. [Default: 10]")
cgroup.add_option("--server", dest="server", default=False, action="store_true", help="Use crab server. [Default: False]")
cgroup.add_option("--lsf", dest="lsf", default=False, action="store_true", help="Run on LSF instead of GRID (can be changed in .cfg file). [Default: True]")
cgroup.add_option("--condor", dest="condor", default=False, action="store_true", help="Run on condor_g instead of GRID (can be changed in .cfg file). [Default: False]")
cgroup.add_option("--glidein", dest="glide", default=False, action="store_true", help="Use glide-in scheduler instead of glite. [Default: False]")
cgroup.add_option("-q", "--queue", dest="queue", default="8nh", type="string", help="LSF queue to use (can be changed in .cfg file). [Default: 8nh]")
cgroup.add_option("-P", "--priority", dest="prio", default=False, action="store_true", help="Use PriorityUser role")
cgroup.add_option("--submitOnly", dest="submitOnly", default=False, action="store_true", help="Use this option to skip the re-creation of input cards and submission scripts")
parser.add_option_group(cgroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re

## define root path (to allow for direcotry
## structure of arbitrary depth)
ROOTPATH = os.getcwd()

for directory in args :
    if directory.find("common")>-1 :
        print "> skipping directory common"
        continue
    print "> entering directory %s" % directory
    ## visit subdirectories
    os.chdir("%s/%s" % (ROOTPATH, directory))
    ## determine list of datacards and list of inputfiles
    ## from what is contained in the current directory
    datacards = []
    inputfiles= []
    ## collect what is there
    basket = os.listdir(os.getcwd())
    ## skip empty directories
    if len(basket)<1 :
        continue
    for piece in basket :
        if piece.endswith('.txt') :
            datacards.append(piece)
        if piece.endswith('.root') :
            inputfiles.append(piece)
    ## optcards should be separated by ' ' -- a few workarounds are introduced at this place:
    ## - htt cards following the old naming conventions of 2011 are truncated at _mA already
    ## - the hggmva.txt datacard as of the modiond12 combination is not considered as it leads
    ##   crashed in text2workspace.py when used with ...=... option due RooFormularVars not
    ##   not found. therefore for the moment hggmva.txt is dropped completely from this line
    ##   and the datacards is used as is without the use of ...=...
    optcards = ""
    for card in datacards :
        if options.binary == "combine":
            ## add channel name for combined datacards (same as datacard name but w/o .txt)
            if card.find("mA")>1 :
                optcards += card[:card.find("_mA")]
            elif card.find("hggmva")>-1 or card.find("testcard")>-1 :
                optcards += "hgg"
            else :
                optcards += card[:card.find(".txt")]
            ## add '=' sign
            optcards += "="
        ## add datacard for combination
        optcards += card
        optcards += " "
    ## optfiles should be separated by ','
    optfiles = ""
    for ifile in inputfiles :
        optfiles += ifile
        optfiles += ","
    optfiles=optfiles.rstrip(",")
    if not options.submitOnly :
        if options.binary == "lands" :
            ## if it does not exist already
            if not os.path.exists("lands") :
                os.system("cp -s $(which lands) .")
            if options.method == "Bayesian" :
                ## -----------------------------------------------------------------------------------------
                ## Option: LandS Bayesian
                ## -----------------------------------------------------------------------------------------
                opts = "-b {bands} -T {toysB} -t {toys} -j {jobs}  -q {queue} -o {out} -i {inputs}".format(
                    out=options.out, bands=options.bands, toysB=options.nuisance, toys=options.t,
                    jobs=options.j, inputs=optfiles, queue=options.queue
                    )
                if options.v != 0 :
                    opts += " -v"
                if options.random :
                    opts += " --random"
                if options.server :
                    opts += " --server"
                if options.lsf    :
                    opts += " --lsf"
                if options.condor :
                    opts += " --condor"
                if options.glide:
                    opts += " --glidein"
                if options.prio:
                    opts += " --priority"
                if options.v != 0 :
                    print "> creating batch job for lands -M Bayesian"
                os.system("lands-bayes.py %s %s" % (opts, optcards))
        if options.binary == "combine" :
            ## create combined model from individual data cards. This is fine for all options but options
            ## single. For the latter the combined datacards are produced for each signal strength point
            ## locally
            if not options.method == "single" :
                os.system("combineCards.py -S %s > tmp.txt" % optcards)
            ## if it does not exist already, create link to executable
            if not os.path.exists("combine") :
                os.system("cp -s $(which combine) .")
            if options.method == "CLs" :
                ## -----------------------------------------------------------------------------------------
                ## Option: combine CLs
                ## -----------------------------------------------------------------------------------------
                ## determine masspoint from directory name
                masspoint = directory[directory.rfind("/")+1:]
                ## setup the batchjob creation for combine -M CLs
                opts = "-o {out} -n {points} -I {interleave} -m {mass} -O {options} -T {toysH} -t {toys} -j {jobs} -q {queue}".format(
                    out=options.out, points=options.points, interleave=options.interl, mass=masspoint, options=options.options,
                    toysH=options.T, toys=options.t, jobs=options.j, queue=options.queue
                    )
                if options.v != 0 :
                    opts += " -v"
                if options.nosys :
                    opts += " --noSystematics"
                if options.nofit :
                    opts += " --noPrefit"
                if options.random :
                    opts += " --random"
                if options.server :
                    opts += " --server"
                if options.lsf    :
                    opts += " --lsf"
                if options.condor :
                    opts += " --condor"
                if options.glide:
                    opts += " --glidein"
                if options.prio:
                    opts += " --priority"
                if options.v != 0 :
                    print "> creating batch job for combine -M CLs"
                ## create the job
                os.system("combine-cls.py %s --shape %s tmp.txt %s %s" % (opts, options.shape, options.min, options.max))
            if options.method == "tanb" :
                ## -----------------------------------------------------------------------------------------
                ## Option: combine tanb
                ## -----------------------------------------------------------------------------------------
                ## determine masspoint from directory name
                masspoint = directory[directory.rfind("/")+1:]
                ## prepare additional workspace creation
                os.system("cp $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/tanb_grid.py .")
                ## determine grid of tanb values from min and max
                dx = (float(options.max)-float(options.min))/(options.points-1)
                points = [ float(options.min) + dx*i for i in range(options.points) ]
                ## create additional workspaces
                for tanb in points :
                    os.system("python tanb_grid.py -m {mass} -t {tanb} --model {model} --interpolation {interpolation} {full_mass} tmp.txt".format(
                        mass=masspoint, tanb=tanb, model=options.model, interpolation=options.interpolation_mode, full_mass="--full-mass" if options.full_mass else "" ))
                ## setup the batchjob creation for combine -M CLs with tanb grid points instead of cross section grid points
                opts = "-o {out} -n {points} -m {mass} -O {options} -T {toysH} -t {toys} -j {jobs} -q {queue}".format(
                    out=options.out, points=options.points, mass=masspoint, options=options.options, toysH=options.T,
                    toys=options.t, jobs=options.j, queue=options.queue
                    )
                if options.v != 0 :
                    opts += " -v"
                if options.nosys :
                    opts += " --noSystematics"
                if options.nofit :
                    opts += " --noPrefit"
                if options.random :
                    opts += " --random"
                if options.server :
                    opts += " --server"
                if options.lsf    :
                    opts += " --lsf"
                if options.condor :
                    opts += " --condor"
                if options.glide:
                    opts += " --glidein"
                if options.prio:
                    opts += " --priority"
                if options.v != 0 :
                    print "> creating batch job for combine -M CLs"
                ## create the job
                os.system("combine-tanb.py %s --shape %s tmp.txt %s %s" % (opts, options.shape, options.min, options.max))
                if not os.path.exists("debug") :
                    os.system("mkdir debug")
                os.system("cp tmp*.txt debug")
            if options.method == "single" :
                ## -----------------------------------------------------------------------------------------
                ## Option: combine single
                ## -----------------------------------------------------------------------------------------
                ## determine masspoint from directory name
                masspoint = directory[directory.rfind("/")+1:]
                ## check whether a manipulation of txt and root files is necessary or not
                modify = True
                ## will be overwritten if modify turns true
                workspaces = ""
                checkbuffer = os.listdir(os.getcwd())
                for check in checkbuffer :
                    if re.match(r"batch_\d+.root", check) :
                        workspaces+=" %s" % check
                        modify = False
                if modify :
                    ## prepare additional workspace creation
                    tanbs = []
                    txtbuffer = os.listdir(os.getcwd())
                    for datacard in txtbuffer :
                        #if re.match(r"\w+_\d+.txt", datacard) :
                        if re.match(r"\w+_tanBeta\d+_modified.txt", datacard) :
                            ## determine the tanb value in question and for the following create an unambiguous
                            ## list of tanb values
                            #tanb = datacard[datacard.rfind("_")+1:datacard.rfind(".txt")]
                            tanb = datacard[datacard.rfind("tanBeta")+7:datacard.rfind("_modified.txt")]
                            if tanbs.count(tanb)<1 :
                                tanbs.append(tanb)
                            ## open the datacard in question and determine the index of all signal samples
                            ## these indices are expected to be 0 or of negative value according to the
                            ## combine convention for signal samples
                            indices = []
                            f = open(datacard)
                            for line in f :
                                line = line.strip().split("\n")[0].strip()
                                if line.startswith("process") :
                                    wordarr = line.strip().split()
                                    idx=0
                                    for word in wordarr :
                                        ## matches negative number or 0
                                        if re.match(r"-\d+", word) or word=="0" :
                                            indices.append(idx)
                                        idx=idx+1
                            f.close()
                            ## determine original rates and divide by tanb on the fly
                            f = open(datacard)
                            for line in f :
                                line = line.strip().split("\n")[0].strip()
                                if line.startswith("rate") :
                                    wordarr = line.strip().split()
                                    for idx in indices :
                                        #print "datacard: %s \t old rate: %10.3s \t new rate %10.3s" % (datacard, wordarr[idx], float(wordarr[idx])/float(tanb))
                                        os.system("perl -pi -e 's/%s/%s/g' %s" % (wordarr[idx], float(wordarr[idx])/float(tanb), datacard))
                            f.close()
                    ## combine all cards for a given signalstrength point
                    workspaces = ""
                    for tanb in tanbs :
                        ## create combined model from individual data cards
                        os.system("combineCards.py -S *tanBeta%s*.txt > tmp_%s.txt" % (tanb, tanb))
                        workspaces+= " tmp_%s.txt" % tanb
                    ## pick up all root input files which are expected to be input root files and devide the
                    ## signal strength by tanb to transform the limit on signal strength into a limit on tanb
                    rootbuffer = os.listdir(os.getcwd())
                    for rootfile in rootbuffer :
                        if rootfile.endswith('.root') :
                            ## skip those root files that might be remnants from former harvestings or batch
                            ## job submissions in that directory
                            if rootfile.find("higgsCombine")>-1 or rootfile.find("batch")>-1 :
                                continue
                            if rootfile.find("tanBeta")>-1 :
                                #tanb = datacard[datacard.rfind("_")+1:datacard.rfind(".txt")]
                                tanb = rootfile[rootfile.rfind("tanBeta")+7:rootfile.rfind("_modified.root")]
                                bash_script = '''root -l -b -q $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C+\(\"true\",\"%s\",\\\"%s\\\"\)''' % (1./float(tanb), rootfile)
                                #print bash_script
                                os.system(bash_script)
                ## setup the batchjob creation for combine -M CLs
                opts = "-o {out} -m {mass} -O {options} -T {toysH} -t {toys} -j {jobs} -q {queue}".format(
                    out=options.out, mass=masspoint, options=options.options, toysH=options.T, toys=options.t,
                    jobs=options.j, queue=options.queue
                    )
                if options.v != 0 :
                    opts += " -v"
                if options.nosys :
                    opts += " --noSystematics"
                if options.nofit :
                    opts += " --noPrefit"
                if options.random :
                    opts += " --random"
                if options.server :
                    opts += " --server"
                if options.lsf    :
                    opts += " --lsf"
                if options.condor :
                    opts += " --condor"
                if options.glide:
                    opts += " --glidein"
                if options.prio:
                    opts += " --priority"
                if options.v != 0 :
                    print "> creating batch job for combine -M CLs"
                ## create the job
                os.system("combine-single.py %s --shape %s %s" % (opts, options.shape, workspaces))
            if options.method == "Bayesian" :
                ## -----------------------------------------------------------------------------------------
                ## Option: combine Bayesian
                ## -----------------------------------------------------------------------------------------
                ## determine masspoint from directory name
                masspoint = directory[directory.rfind("/")+1:]
                ## setup the batchjob creation for combine -M MarkovChainMC [Bayesian]
                opts = "-H {hint} --rMin {rMin} --rMax {rMax} --iterations {iter} --tries {tries} -t {toys} -j {jobs} -q {queue} -m {mass}".format(
                    hint=options.hint, rMin=options.rMin, rMax=options.rMax, iter=options.iter, tries=options.tries, toys=options.t, jobs=options.j,
                    queue=options.queue, mass=masspoint
                    )
                if options.v != 0 :
                    opts += " -v"
                if options.nosys :
                    opts += " --noSystematics"
                if options.random :
                    opts += " --random"
                if options.server :
                    opts += " --server"
                if options.lsf    :
                    opts += " --lsf"
                if options.condor :
                    opts += " --condor"
                if options.glide:
                    opts += " --glidein"
                if options.prio:
                    opts += " --priority"
                if options.v != 0 :
                    print "> creating batch job for combine -M Bayesian"
                ## create the job
                os.system("combine-bayes.py --shape %s %s tmp.txt" % (options.shape, opts))
                ## in case prepare a batch submission for the observed limit
                if options.observed :
                    if os.path.exists("common") :
                        os.system("rm common")
                    os.system("ln -s ../common common")
                    if os.path.exists("observed") :
                        os.system("rm -r observed")
                    os.system("mkdir observed")
                    ## copy necessary input for workspace creation
                    os.system("cp tmp.txt observed")
                    os.system("cp *.root observed")
                    ## create job in subdirectory
                    os.chdir("%s/observed" % os.getcwd())
                    ## setup batchjob creation for combine -M MarkovChainMC [Bayesian] for data (with some reduced)
                    ## set of options
                    opts = "-H {hint} --rMin {rMin} --rMax {rMax} --iterations {iter} --tries {tries} -q {queue}".format(
                        hint=options.hint, rMin=options.rMin, rMax=options.rMax, iter=options.iter, tries=options.tries,
                        queue=options.queue)
                    if options.v != 0 :
                        opts += " -v"
                    if options.server :
                        opts += " --server"
                    if options.lsf    :
                        opts += " --lsf"
                    if options.condor :
                        opts += " --condor"
                    if options.glide:
                        opts += " --glidein"
                    if options.prio:
                        opts += " --priority"
                    os.system("combine-bayes.py --shape %s %s --observed tmp.txt" % (options.shape, opts))
                    ## cleanup and return to the head directory to go on
                    os.system("rm tmp*")
                    os.chdir("%s/.." % os.getcwd())
            if options.method == "significance" :
                ## -----------------------------------------------------------------------------------------
                ## Option: combine ProfileLikelihood (significance)
                ## -----------------------------------------------------------------------------------------
                ## determine masspoint from directory name
                masspoint  = directory[directory.rfind("/")+1:]
                ## prepare binary workspace
                mass_fixed = options.fixed_mass if options.fixed_mass!="" else masspoint
                os.system("text2workspace.py tmp.txt --default-morphing=%s -m %s -o batch.root"% (options.shape, mass_fixed))
                ## setup the batchjob creation for combine -M CLs
                opts = "-o {out} -m {mass} --signal-strength {strength} -t {toys} -j {jobs} -q {queue}".format(
                    out=options.out, mass=masspoint, strength=options.signal_strength, toys=options.t, jobs=options.j, queue=options.queue
                    )
                if options.v != 0 :
                    opts += " -v"
                if options.server :
                    opts += " --server"
                if options.lsf    :
                    opts += " --lsf"
                if options.condor :
                    opts += " --condor"
                if options.glide:
                    opts += " --glidein"
                if options.prio:
                    opts += " --priority"
                if options.v != 0 :
                    print "> creating batch job for combine -M ProfileLikelihood"
                ## create the job
                os.system("combine-sig.py %s batch.root" % opts)
            ## cleanup
            os.system("rm tmp*")
    ## do the batch job submission
    if not options.interactive :
        os.system("crab -create -cfg %s.cfg" % options.out)
        os.system("sleep 5")
        os.system("crab -submit")
        print "Snoozing for 45 seconds ..."
        os.system("sleep 45")
        os.system("crab -status")
        os.system("sleep 10")
        ## do the submission from a observed subdirectory if it exists
        if options.observed and os.path.exists("observed") :
            os.chdir("%s/observed" % os.getcwd())
            os.system("crab -create -cfg %s.cfg" % options.out)
            os.system("sleep  5")
            os.system("crab -submit")
            os.system("sleep 45")
            os.system("crab -status")
            ## need for crab server
            os.system("sleep 10")
            os.chdir("%s/.." % os.getcwd())
        #print "Snoozing for 1.5 minutes..."
        #os.system("sleep 180")
        print "Snoozing for 1.5 minutes..."
        os.system("sleep 90")
    ## step back to main working directory
    os.chdir("%s/../.." % os.getcwd())
print "> done"

