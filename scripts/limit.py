#!/usr/bin/env python
# flake8: noqa

import glob
import hashlib
import os
import re
from optparse import OptionParser, OptionGroup
from HiggsAnalysis.HiggsToTauTau.parallelize import parallelize
from HiggsAnalysis.HiggsToTauTau.CardCombiner import create_workspace
import sys

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...",
                      description="This is a script to harvest grid jobs that have been submitted via crab. You can check the status of the submitted jobs, get the output in a parallelized way or further process the output for Bayesian or CLs limits. Parallelization of output means that for each submitted crab job a tmp script will be created and executed in batch mode to receive the output. Be careful as this can spill your machine with a sizable amount of small scripts, which do not use much CPU but which are many. Further processing of the output means that the outputs of all jobs are combined using hadd and e.g. for CLs the expected and observed limits and the expected one and two sigma bands are calculated from the returned output for each mass point. The ARGs (ARG1, ARG2, ARG3, ...) correspond to the working directores the harvesting should be performed on. This script is capable of recognizing \"observed\" directories in case crab jobs also have been submitted for observed limits in the case of Bayesian limits where also this calculation can take a sizable amount of time depending on the complexity of the model.\n")
## direct options
parser.add_option("--status", dest="status", default=False, action="store_true", help="Monitor crabjobs. [Default: False]")
parser.add_option("--getoutput", dest="getoutput", default=False, action="store_true", help="Get crab outputs. [Default: False]")
parser.add_option("--CLs", dest="prepCLs", default=False, action="store_true", help="Prepare CLs limits (expected and obeserved). [Default: False]")
parser.add_option("--tanb", dest="prepTanB", default=False, action="store_true", help="Prepare CLs limits directly in tanb (expected and obeserved, based on the tang-grip.py script). For this option you must have run the submit.py script with option --method tanb for CLs type limit calculation via the grid. [Default: False]")
parser.add_option("--tanb+", dest="prepTanB_fast", default=False, action="store_true", help="Prepare asymptotic limits directly in tanb (expected and obeserved, based on the tanb-grid.py script). For this option you must have run the submit.py script with options --method tanb+. A submission via grid is not necessary but can be run in parallel on the same derived datacards. [Default: False]")
parser.add_option("--tanb-parallel", dest="tanbparallel", type="int", default=-1, help="Run combine calls in parallel (supply nTasks) when scanning in tanBeta")
parser.add_option("--single", dest="prepSingle", default=False, action="store_true", help="Prepare CLs limits directly in tanb(expected and obeserved, using Christians method). [Default: False]")
parser.add_option("--bayesian", dest="prepBayesian", default=False, action="store_true", help="Prepare Bayesian limits (expected and obeserved). [Default: False]")
parser.add_option("--asymptotic", dest="prepAsym", default=False, action="store_true", help="Prepare Asymptotic limits (expected and obeserved). [Default: False]")
parser.add_option("--max-likelihood", dest="prepMLFit", default=False, action="store_true", help="Prepare Maximum Likelihood Fit (also used for postfit plots). [Default: False]")
parser.add_option("--multidim-fit", dest="prepMDFit", default=False, action="store_true", help="Prepare MultiDimentional Fit (also used for postfit plots). [Default: False]")
parser.add_option("--multidim-scan", dest="prepMDScan", default=False, action="store_true", help="Prepare MultiDimentional 1D Scan. [Default: False]")
parser.add_option("--significance", dest="prepPLSig", default=False, action="store_true", help="Calculate expected significance from Profile Likelihood method. [Default: False]")
parser.add_option("--mssm-xsec", dest="prepMSSMxsec", default=False, action="store_true", help="Prepare MSSM xsec limits (expected and obeserved). [Default: False]")
parser.add_option("--refit", dest="refit", default=False, action="store_true", help="Do not run the asymptotic limits again, but only run the last step, the fit for the limit determination. (Only valid for option --tanb+, for all other options will have no effect.)  [Default: False]")
parser.add_option("--cleanup", dest="cleanup", default=False, action="store_true", help="Remove all crab remainders from previous submissions. [Default: False]")
parser.add_option("--kill", dest="kill", default=False, action="store_true", help="Kill all crab jobs in case of emergencies. [Default: False]")
parser.add_option("--expectedOnly", dest="expectedOnly", default=False, action="store_true", help="Calculate the expected limit only. [Default: False]")
parser.add_option("--observedOnly", dest="observedOnly", default=False, action="store_true", help="Calculate the observed limit only. [Default: False]")
parser.add_option("--userOpt", dest="userOpt", default="", type="string", help="Any kind of user options that should be passed on to combine. [Defaul: \"\"]")
parser.add_option("--shape", dest="shape", default="shape2", type="string", help="Choose dedicated algorithm for shape uncertainties. [Default: 'shape2']")
parser.add_option("-C", "--confidence-level", dest="confidenceLevel", default="0.95", type="string", help="Choose the actual confidence level. At this step this applies only to asymptotic methods like for option --prepTanB+ and --preAsym. It does not apply to toy based methods, which have to be configured accordingly in the submission step. [Default: '0.95']")
parser.add_option("--rMin", dest="rMin", default="-5", type="string", help="Minimum value of signal strenth. [Default: -5]")
parser.add_option("--rMax", dest="rMax", default="5", type="string", help="Maximum value of signal strenth. [Default: 5]")
parser.add_option("--name", dest="name", default="Test", type="string", help="Name of the output file, passed on to combine. [Default: \"Test\"]")
parser.add_option("--no-repeat", dest="norepeat", default=False, action="store_true", help="Detect if command has already been run, and skip the job.")
parser.add_option("--ggH", dest="ggH", default=False, action="store_true", help="Switch ggH or bbH to background. [Default: False]")
parser.add_option("--working-dir", dest="workingdir", default=".", help="Optionally specify where the temporary combined datacard is produced")
mgroup = OptionGroup(parser, "COMBINE (MAXIMUM LIKELIHOOD FIT) COMMAND OPTIONS", "Command options for the use of combine with the Maximum Likelihood method.")
mgroup.add_option("--stable", dest="stable", default=False, action="store_true", help="Run maximum likelihood fit with a set of options that lead to stable results. Makes use of the common options --rMin and --rMax to define the boundaries of the fit. [Default: False]")
mgroup.add_option("--algo", dest="fitAlgo", type="string", default="contour2d", help="Algorithm for multi-dimensional maximum likelihood fit (options are singles, contour2d, grid). Option grid will make use of the option --points to determine the number of grid points in the scan. [Default: \"\"]")
mgroup.add_option("--physics-model", dest="fitModel", type="string", default="", help="Physics model for multi-dimensional maximum likelihood. The physics model should be defined by a model name and a path to a python implementation of the model separated by '='. For example 'ggH-qqH-model=PATH-TO-IMPLEMENTATION'. In this case a workspace of the model with given model options will be created with the name 'ggH-qqH-model.root'. It is also possible to pass on only a name of a physics model, like 'ggH-qqH-model'. In this case it will be assumed that the model with name 'ggH-qqH-model' has been created beforehand. [Default: \"\"]")
mgroup.add_option("--physics-model-options", dest="fitModelOptions", type="string", default="", help="Potential options for the used physics model for multi-dimensional maximum likelihood. More options can be passed on separated by ';'. [Default: \"\"]")
mgroup.add_option("--restrict-categories", dest="fitModelCategories", type="string", default="", help="Add a string to restrict the fit only to a subset of event categories. The string should contain the indexes of the allowed event categories then. The indexes should be separated by ':', example: '0:1:2:3'. If the string is empty the datacards from all event categories will be taken into account in the fit, that are located in the target directory. [Default: \"\"]")
mgroup.add_option("--setup-only", dest="setupOnly", action="store_true", default=False, help="Only setup the model, do not start the minimization. To be used with job splitting for maximum likelihood scans. If False the model will be set up and the minimzation will be executed in one go. [Default: \"False\"]")
mgroup.add_option("--points", dest="gridPoints", type="string", default="100", help="Number of grid points in case of option --algo=grid. [Default: \"100\"]")
mgroup.add_option("--firstPoint", dest="firstPoint", type="string", default="", help="Potential options for splitting the gridPoints in different jobs. Only to be used with lxq/b_gridScan.py [Default: \"\"]")
mgroup.add_option("--lastPoint", dest="lastPoint", type="string", default="", help="Potential options for splitting the gridPoints in different jobs. Only to be used with lxq/b_gridScan.py [Default: \"\"]")
mgroup.add_option("--saveResults", dest="saveResults", action="store_true", default=False, help="Store the fit output directly in a text file called multi-dim.fitresult. [Default: \"False\"]")
parser.add_option_group(mgroup)
egroup = OptionGroup(parser, "COMBINE (MCMC/BAYESIAN) COMMAND OPTIONS", "Command options for the use of combine with the MarkovChainMC/Bayesian method.")
egroup.add_option("--hint", dest="hint", default="Asymptotic", type="string", help="Name of the hint method that is used to guide the MarkovChainMC. [Default: Asymptotic]")
egroup.add_option("--iterations", dest="iter", default=10000, type="int", help="Number of iterations to integrate out nuisance parameters. [Default: 10000]")
egroup.add_option("--tries", dest="tries", default=10, type="int", help="Number of tries to run the MCMC on the same data. [Default: 10]")
parser.add_option_group(egroup)
agroup = OptionGroup(parser, "COMBINE (ASYMPTOTIC) COMMAND OPTIONS", "Command options for the use of combine with the Asymptotic method.")
agroup.add_option("--noprefit", dest="noprefit", default=False, action="store_true", help="Skip prefit before running the asymptotics limits. [Default: False]")
agroup.add_option("--minuit", dest="minuit", default=False, action="store_true", help="Switch from Minuit2 to Minuti for the prefit. [Default: False]")
agroup.add_option("--qtilde", dest="qtilde", default=False, action="store_true", help="Also allow negative signal strength. [Default: False]")
agroup.add_option("--strategy", dest="strategy", default=2, type="int", help="Change the fit strategy [Default: 2]")
parser.add_option_group(agroup)
pgroup = OptionGroup(parser, "COMBINE (PROFILE LIKELIHOOD) COMMAND OPTIONS", "Command options for the use of combine with the ProfileLikelihood method.")
pgroup.add_option("--fixed-mass", dest="fixed_mass", default="", type="string", help="Set a fixed mass at which to inject the signal signal (during workspace creation). If the string is empty the mass point is taken for which the significance is cslculated. [Default: \"\"]")
pgroup.add_option("--signal-strength", dest="signal_strength", default="1", type="string", help="Set signal strength for expected significance calculation. [Default: \"1\"]")
pgroup.add_option("--toys", dest="toys", default="100", type="string", help="Set number of toys for expected significance calculation. [Default: \"100\"]")
parser.add_option_group(pgroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

## base directory introduced to allow use of absolute file paths
base_directory = os.getcwd()

def get_hash_for_this_call():
    ''' Create a unique hash corresponding to this call to limit.py

    Returns a hexadecimal string.
    '''
    # Create the hash of the limit.py call
    hash = hashlib.md5()
    # Hash in the modification time of this script
    #hash.update(str(os.path.getmtime(os.path.realpath(__file__))))
    # Hash in the arguments
    for x in sys.argv:
        # So we can enable norepeat after running the jobs
        if x == '--norepeat':
            continue
        hash.update(x)
    return 'limit_hash_' + hash.hexdigest()[:9]

def already_run(directory):
    ''' Determine if the limit.py tool has already been run for this directory

    Checks if any .txt card file or .root file is up-to-date with the limit
    calculation.  The calls to limit.py are hashed using the arguments, and
    modification time of the limit.py script.

    '''
    dependents = glob.glob(os.path.join(directory, '*.txt')) + glob.glob(
        os.path.join(directory, '..', 'common', '*.root'))
    # Find the latest modified time of the dependents
    latest_modified = max(os.path.getmtime(x) for x in dependents)
    hash_file = os.path.join(directory, get_hash_for_this_call())
    if not os.path.exists(hash_file):
        print ">>> limit hash file %s does not exist, must compute" % hash_file
        return False
    # Check if any dependent file has been modified after the hash
    if os.path.getmtime(hash_file) < latest_modified:
        print ">>> hash file %s is out of date: %f < %f" % (hash_file, os.path.getmtime(hash_file), latest_modified)
        return False
    return True

def create_card_workspace(mass, card_glob='*.txt', output='tmp.root',
                          extra_options=None):
    ''' Create a tmp.root combining data cards in the CWD '''
    ws_options = {'-m': mass, '--default-morphing': options.shape}
    if extra_options:
        ws_options.update(extra_options)
    output = os.path.join(options.workingdir, output)
    return create_workspace(output, card_glob, ws_options)

for directory in args :
    if directory.find("common")>-1 :
        print "> skipping directory common"
        continue
    print "> entering directory %s" % directory
    ## visit subdirectories
    subdirectory = os.path.join(base_directory, directory)
    if options.norepeat and already_run(subdirectory):
        print ">> limit already computed - skipping %s" % directory
        continue
    subdirectory = subdirectory.replace(os.path.join(base_directory, base_directory), base_directory)
    print subdirectory
    os.chdir(subdirectory)
    ## check status
    if options.status :
        directoryList = os.listdir(".")
        for name in directoryList :
            if name.find("crab_0")>-1 and not name.find(".")>-1:
                os.system("crab -status -c %s" % name)
        if os.path.exists("observed") :
            os.chdir(os.path.join(subdirectory, "observed"))
            directoryList = os.listdir(".")
            for name in directoryList :
                if name.find("crab_0")>-1 and not name.find(".")>-1:
                    os.system("crab -status -c %s" % name)
            os.chdir(subdirectory)
    if options.getoutput :
        directoryList = os.listdir(".")
        for name in directoryList :
            ## create a tmp shell script for each crab_0* directory
            ## w/o duplicating the .sh that might have been produced
            ## before
            if name.find("crab_0")>-1 and not name.find(".")>-1:
                if os.path.exists("tmp_%s.sh") :
                    os.system("rm tmp_%s.sh")
                tmp = open("tmp_%s.sh" % name, "w")
                tmp.write("#!/bin/sh\n")
                tmp.write("crab -status -c %s\n" % name)
                tmp.write("crab -getoutput -c %s\n" % name)
                tmp.close()
                os.system("chmod a+x tmp_%s.sh" % name)
                os.system("./tmp_%s.sh &" % name)
               #os.system("crab -status -c %s" % name)
               #os.system("crab -getoutput -c %s" % name)
        if os.path.exists("observed") :
            os.chdir(os.path.join(subdirectory, "observed"))
            directoryList = os.listdir(".")
            for name in directoryList :
                ## create a tmp shell script for each crab_0* directory
                ## w/o duplicating the .sh that might have been produced
                ## before
                if name.find("crab_0")>-1 and not name.find(".")>-1:
                    if os.path.exists("tmp_%s.sh") :
                        os.system("rm tmp_%s.sh")
                    tmp = open("tmp_%s.sh" % name, "w")
                    tmp.write("#!/bin/sh\n")
                    tmp.write("crab -status -c %s\n" % name)
                    tmp.write("crab -getoutput -c %s\n" % name)
                    tmp.close()
                    os.system("chmod a+x tmp_%s.sh" % name)
                    os.system("./tmp_%s.sh &" % name)
                   #os.system("crab -status -c %s" % name)
                   #os.system("crab -getoutput -c %s" % name)
            os.chdir(subdirectory)
    if options.prepCLs :
        ifile=0
        directoryList = os.listdir(".")
        ## create a hadd'ed file per crab directory
        for name in directoryList :
            if name.find("crab_0")>-1 and not name.find(".")>-1:
                if os.path.exists("batch_collected_%s.root" % ifile) :
                    os.system("rm batch_collected_%s.root" % ifile)
                os.system("hadd batch_collected_%s.root %s/res/*.root" % (ifile, name))
                ifile=ifile+1
        ## and finally hadd all sub files corresponding to each crab directory
        if os.path.exists("batch_collected.root") :
            os.system("rm batch_collected.root")
        os.system("hadd batch_collected.root batch_collected_*.root")
        os.system("rm batch_collected_*.root")
        ## determine masspoint from directory name
        masspoint = directory[directory.rfind("/")+1:]
        if not options.expectedOnly :
            ## observed limit
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root" % masspoint)
        if not options.observedOnly :
            ## expected -2sigma
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root --expectedFromGrid 0.0275" % masspoint)
            ## expected -1sigma
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root --expectedFromGrid 0.1600" % masspoint)
            ## expected median
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root --expectedFromGrid 0.5000" % masspoint)
            ## expected +1sigma
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root --expectedFromGrid 0.8400" % masspoint)
            ## expected +2sigma
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root --expectedFromGrid 0.9750" % masspoint)
    if options.prepTanB or options.prepSingle :
        ifile=0
        directoryList = os.listdir(".")
        ## create a hadd'ed file per crab directory
        for name in directoryList :
            if name.find("crab_0")>-1 and not name.find(".")>-1:
                if os.path.exists("batch_collected_%s.root" % ifile) :
                    os.system("rm batch_collected_%s.root" % ifile)
                os.system("hadd batch_collected_%s.root %s/res/*.root" % (ifile, name))
                ifile=ifile+1
        ## and finally hadd all sub files corresponding to each crab directory
        if os.path.exists("batch_collected.root") :
            os.system("rm batch_collected.root")
        os.system("hadd batch_collected.root batch_collected_*.root")
        os.system("rm batch_collected_*.root")
        ## determine masspoint from directory name
        masspoint = directory[directory.rfind("/")+1:]
        ## fetch workspace for each tanb point
        for wsp in directoryList :
            if re.match(r"batch_\d+(.\d\d)?.root", wsp) :
                if not options.expectedOnly :
                    ## observed limit
                    os.system("combine %s -M HybridNew -m %s --fullGrid --noUpdateGrid --freq --grid=batch_collected.root" % (wsp, masspoint))
                if not options.observedOnly :
                    ## expected -2sigma
                    os.system("combine %s -M HybridNew -m %s --freq --fullGrid --grid=batch_collected.root --expectedFromGrid 0.0275" % (wsp, masspoint))
                    ## expected -1sigma
                    os.system("combine %s -M HybridNew -m %s --freq --fullGrid --grid=batch_collected.root --expectedFromGrid 0.1600" % (wsp, masspoint))
                    ## expected median
                    os.system("combine %s -M HybridNew -m %s --freq --fullGrid --grid=batch_collected.root --expectedFromGrid 0.5000" % (wsp, masspoint))
                    ## expected +1sigma
                    os.system("combine %s -M HybridNew -m %s --freq --fullGrid --grid=batch_collected.root --expectedFromGrid 0.8400" % (wsp, masspoint))
                    ## expected +2sigma
                    os.system("combine %s -M HybridNew -m %s --freq --fullGrid --grid=batch_collected.root --expectedFromGrid 0.9750" % (wsp, masspoint))
                ## break after first success (assuming that all workspaces are fine to do the interpolation)
                break
    if options.prepTanB_fast :
        ## determine masspoint from directory name
        masspoint = directory[directory.rfind("/")+1:]
        print "> asymptotic limits for mass %s" % masspoint
        ## prepare prefit option
        prefitopt = ""
        if options.noprefit :
            prefitopt = "-t -1"
        ## prepare fit option
        minuitopt = ""
        if options.minuit :
            minuitopt = "--minimizerAlgo minuit"
        qtildeopt = ""
        if options.qtilde :
            qtildeopt = "--qtilde 0"
        ## prepare mass argument for limit calculation if configured such
        idx = directory.rfind("/")
        if idx == (len(directory) - 1):
            idx = directory[:idx - 1].rfind("/")
        mass_string  = directory[idx + 1:]
        mass_matcher = re.compile(r"(?P<mass>[\+\-0-9\s]+)[a-zA-Z0-9]*")
        mass_value   = mass_matcher.match(mass_string).group('mass')
        massopt = "-m %i " % int(mass_value)
        ## string for tanb inputfiles
        tanb_inputfiles = ""
        ## list of all elements in the current directory
        directoryList = os.listdir(".")

        tasks = []
        ## fetch workspace for each tanb point
        for wsp in directoryList :
            if re.match(r"batch_\d+(.\d\d)?.root", wsp) :
                tanb_inputfiles += wsp.replace("batch", "point")+","
                tanb_string = wsp[wsp.rfind("_")+1:]
                if not options.refit :
                    tasks.append(
                        ["combine -M Asymptotic -n .tanb{tanb} --run both -C {CL} {minuit} {prefit} --minimizerStrategy {strategy} {mass} {user} {wsp}".format(CL=options.confidenceLevel, minuit=minuitopt, prefit=prefitopt,strategy=options.strategy,mass=massopt, wsp=wsp, user=options.userOpt, tanb=tanb_string),
                         "mv higgsCombine.tanb{tanb}.Asymptotic.mH{mass}.root point_{tanb}".format(mass=mass_value, tanb=tanb_string)
                        ]
                    )
        if options.tanbparallel == -1:
            for task in tasks:
                for subtask in task:
                    os.system(subtask)
        else:
            # Run in parallel using multiple cores
            parallelize(tasks, options.tanbparallel)

        ## strip last ','
        tanb_inputfiles = tanb_inputfiles.rstrip(",")
        ## combine limits of individual tanb point to a single file equivalent to the standard output of --prepCLs
        ## to be compatible with the output of the option --prepTanB for further processing

        # NB if the ACliC compliation crashes here, run
        # root -l -b -q HiggsAnalysis/HiggsToTauTau/macros/asymptoticLimit.C+
        # in $CMSSW_BASE/src
        CMSSW_BASE = os.environ["CMSSW_BASE"]
        ## clean up directory from former run
        os.system("rm higgsCombineTest.HybridNew*")
        if not options.expectedOnly :
            os.system(r"root -l -b -q {cmssw_base}/src/HiggsAnalysis/HiggsToTauTau/macros/asymptoticLimit.C+\(\"higgsCombineTest.HybridNew.mH{mass}.root\",\"{files}\",2\)".format(cmssw_base=CMSSW_BASE, mass=mass_value, files=tanb_inputfiles))
        if not options.observedOnly :
            os.system(r"root -l -b -q {cmssw_base}/src/HiggsAnalysis/HiggsToTauTau/macros/asymptoticLimit.C+\(\"higgsCombineTest.HybridNew.mH{mass}.quant0.027.root\",\"{files}\",2\)".format(cmssw_base=CMSSW_BASE, mass=mass_value, files=tanb_inputfiles))
            os.system(r"root -l -b -q {cmssw_base}/src/HiggsAnalysis/HiggsToTauTau/macros/asymptoticLimit.C+\(\"higgsCombineTest.HybridNew.mH{mass}.quant0.160.root\",\"{files}\",2\)".format(cmssw_base=CMSSW_BASE, mass=mass_value, files=tanb_inputfiles))
            os.system(r"root -l -b -q {cmssw_base}/src/HiggsAnalysis/HiggsToTauTau/macros/asymptoticLimit.C+\(\"higgsCombineTest.HybridNew.mH{mass}.quant0.500.root\",\"{files}\",2\)".format(cmssw_base=CMSSW_BASE, mass=mass_value, files=tanb_inputfiles))
            os.system(r"root -l -b -q {cmssw_base}/src/HiggsAnalysis/HiggsToTauTau/macros/asymptoticLimit.C+\(\"higgsCombineTest.HybridNew.mH{mass}.quant0.840.root\",\"{files}\",2\)".format(cmssw_base=CMSSW_BASE, mass=mass_value, files=tanb_inputfiles))
            os.system(r"root -l -b -q {cmssw_base}/src/HiggsAnalysis/HiggsToTauTau/macros/asymptoticLimit.C+\(\"higgsCombineTest.HybridNew.mH{mass}.quant0.975.root\",\"{files}\",2\)".format(cmssw_base=CMSSW_BASE, mass=mass_value, files=tanb_inputfiles))
    if options.prepBayesian :
        ifile=0
        directoryList = os.listdir(".")
        ## create a hadd'ed file per crab directory
        for name in directoryList :
            if name.find("crab_0")>-1 and not name.find(".")>-1:
                if os.path.exists("batch_collected_%s.root" % ifile) :
                    os.system("rm batch_collected_%s.root" % ifile)
                os.system("hadd batch_collected_%s.root %s/res/*.root" % (ifile, name))
                ifile=ifile+1
        ## and finally hadd all sub files corresponding to each crab directory
        if os.path.exists("batch_collected.root") :
            os.system("rm batch_collected.root")
        os.system("hadd batch_collected.root batch_collected_*.root")
        os.system("rm batch_collected_*.root")
        ## determine masspoint from directory name
        masspoint = directory[directory.rfind("/")+1:]
        ## clean up from legacy of former trials to get the observed limit
        if os.path.exists("higgsCombineTest.MarkovChainMC.mH%s.root" % masspoint) :
            os.system("rm higgsCombineTest.MarkovChainMC.mH%s.root" % masspoint)
        ## in case the observed was calculated via crab just copy it to the head
        ## directory else run it interactively
        if os.path.exists("observed") :
            if not options.expectedOnly :
                os.system("cp observed/crab_0_*/res/higgsCombineTest.MarkovChainMC.mH{mass}*.root ./higgsCombineTest.MarkovChainMC.mH{mass}.root".format(mass=masspoint))
        else :
            os.system("combine -M MarkovChainMC -H {hint} --rMin {rMin} --rMax {rMax} -i {iter} --tries {tries} --mass {mass} {user} -d batch.root".format(
                hint=options.hint, rMin=options.rMin, rMax=options.rMax, tries=options.tries, mass=masspoint, user=options.userOpt, iter=options.iter))
    if options.prepAsym :
        ## prepare mass argument for limit calculation if configured such
        idx = directory.rfind("/")
        if idx == (len(directory) - 1):
            idx = directory[:idx - 1].rfind("/")
        mass_value  = directory[idx + 1:]
        #mass_string  = directory[idx + 1:]
        #mass_regex   = r"(?P<mass>[\+\-0-9\s]+)[a-zA-Z0-9]*"
        #mass_matcher = re.compile(mass_regex)
        #mass_value   = mass_matcher.match(mass_string).group('mass')

        ## combine datacard from all datacards in this directory
        #os.system("combineCards.py -S *.txt > %s/tmp.txt" % options.workingdir)
        ## prepare binary workspace
        #os.system("text2workspace.py --default-morphing=%s -m %s -b %s/tmp.txt -o %s/tmp.root"% (options.shape, mass_value, options.workingdir, options.workingdir))

        create_card_workspace(mass_value)

        ## if it does not exist already, create link to executable
        if not os.path.exists("combine") :
            os.system("cp -s $(which combine) .")
        ## prepare prefit option
        prefitopt = ""
        if options.noprefit :
            prefitopt = "-t -1"
        ## prepare fit option
        minuitopt = ""
        if options.minuit :
            minuitopt = "--minimizerAlgo minuit"
        qtildeopt = ""
        if options.qtilde :
            qtildeopt = "--qtilde 0"
        ## prepare mass options
        massopt = "-m %s " % mass_value
        ## run expected limits
        if not options.observedOnly :
            os.system("combine -M Asymptotic --run expected -C {CL} {minuit} {prefit} --minimizerStrategy {strategy} -n '-exp' {mass} {user} {WDIR}/tmp.root".format(
                CL=options.confidenceLevel, minuit=minuitopt, prefit=prefitopt, strategy=options.strategy, mass=massopt, user=options.userOpt, WDIR=options.workingdir))
        ## run observed limit
        if not options.expectedOnly :
            os.system("combine -M Asymptotic --run observed -C {CL} {minuit} --minimizerStrategy {strategy} -n '-obs' {qtilde} {mass} {user} {WDIR}/tmp.root".format(
                CL=options.confidenceLevel, minuit=minuitopt, qtilde=qtildeopt, strategy=options.strategy, mass=massopt, user=options.userOpt, WDIR=options.workingdir))
    if options.prepMLFit :
        ## determine mass value from directory
        mass = directory[directory.rfind("/")+1:]
        ## combine datacard from all datacards in this directory
        create_card_workspace(mass)
        ## create sub-directory out from scratch
        if os.path.exists("out") :
            os.system("rm -r out")
        os.system("mkdir out")
        ## if it does not exist already, create link to executable
        if not os.path.exists("combine") :
            os.system("cp -s $(which combine) .")
        ## prepare fit option
        minuitopt = ""
        if options.minuit :
            minuitopt = "--minimizerAlgo minuit"
        stableopt = ""
        if options.stable :
            stableopt = "--robustFit=1 --stepSize=0.5  --minimizerStrategy=0 --minimizerTolerance=0.1 --preFitValue=0.1  --X-rtd FITTER_DYN_STEP  --cminFallbackAlgo=\"Minuit;0.001\" "
            stableopt+= "--rMin {MIN} --rMax {MAX} ".format(MIN=options.rMin, MAX=options.rMax)
        ## run expected limits
        print "Running maximum likelihood fit with options: ", "combine -M MaxLikelihoodFit -m {mass} {minuit} {stable} {user} tmp.root --out=out".format(mass=mass, minuit=minuitopt, stable=stableopt, user=options.userOpt)
        os.system("combine -M MaxLikelihoodFit -m {mass} {minuit} {stable} {user} tmp.root --out=out".format(mass=mass, minuit=minuitopt, stable=stableopt, user=options.userOpt))
        ## change to sub-directory out and prepare formated output
        os.chdir(os.path.join(subdirectory, "out"))
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A -a -f text mlfit.root > mlfit.txt")
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A -a -f latex mlfit.root > mlfit.tex")
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A -a -f html mlfit.root > mlfit.html")
        # Versions with only problematic values
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A  -f latex mlfit.root > mlfit_pulled.tex")
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A  -f html mlfit.root > mlfit_pulled.html")
        os.chdir(subdirectory)
    if options.prepMDScan :
        ## determine mass value from directory
        mass = directory[directory.rfind("/")+1:]
        ## combine datacard from all datacards in this directory
        create_card_workspace(mass)
        ## create sub-directory out from scratch
        if os.path.exists("out") :
            os.system("rm -r out")
        os.system("mkdir out")
        ## if it does not exist already, create link to executable
        if not os.path.exists("combine") :
            os.system("cp -s $(which combine) .")
        ## prepare fit option
        minuitopt = ""
        if options.minuit :
            minuitopt = "--minimizerAlgo minuit"
        stableopt = ""
        if options.stable :
            stableopt = "--robustFit=1 --stepSize=0.5  --minimizerStrategy=0 --minimizerTolerance=0.1 --preFitValue=0.1  --X-rtd FITTER_DYN_STEP  --cminFallbackAlgo=\"Minuit;0.001\" "
        ## run expected limits
        command = "combine -M MultiDimFit -m {mass} --points={points} --saveNLL --algo={algo} {minuit} {stable} {user} tmp.root".format(mass=mass, points=options.gridPoints, algo=options.fitAlgo,  minuit=minuitopt, stable=stableopt, user=options.userOpt)
        command += " --rMin {MIN} --rMax {MAX} ".format(MIN=options.rMin, MAX=options.rMax)
        command += " &> /dev/null"
        print "Running likelihood scan with options: ", command
        os.system(command)
        ## change to sub-directory out and prepare formated output
    if options.prepMDFit :
        ## determine mass value from directory
        mass = directory[directory.rfind("/")+1:]
        model = []
        if "=" in options.fitModel :
            model = options.fitModel.split('=')
            ## collect all cards that should be combined into the model
            inputcards = ""
            for card in os.listdir(".") :
                if "htt_" in card :
                    if options.fitModelCategories == "" :
                        inputcards+=card[:card.find('.')]+'='+card+' '
                    else :
                        allowed_categories = options.fitModelCategories.split(':')
                        for allowed in allowed_categories :
                            if allowed in card :
                                inputcards+=card[:card.find('.')]+'='+card+' '

            # OLD COMBINING BEHAVIOR

            ## combine datacard from all datacards in this directory. For the multi-dimensional fit
            ## it is of importance that the decay channels and run periods are well defined from the
            ## channel names. Allow for a restriction of the event categories
            if os.path.exists("tmp.txt") :
                os.system("rm tmp.txt")
            if os.path.exists("%s.root" % model[0]) :
                os.system("rm %s.root" % model[0])
            print "combineCards.py -S %s > tmp.txt" % inputcards
            os.system("combineCards.py -S %s > tmp.txt" % inputcards)
            ## create workspace with dedicated physics model
            workspaceOptions = "-m %s " % mass
            workspaceOptions+= "-o %s.root " % model[0]
            workspaceOptions+= "-P %s " % model[1]
            if not options.fitModelOptions == "" :
                ## break physics model options to list
                opts = options.fitModelOptions.split(';')
                for idx in range(len(opts)) : opts[idx] = opts[idx].rstrip(',')
                for opt in opts :
                    workspaceOptions+="--PO %s " % opt
            print "creating workspace with options:", "text2workspace.py tmp.txt %s" % workspaceOptions
            os.system("text2workspace.py tmp.txt %s" % workspaceOptions)

            # NEW BEHAVIOR
            # TODO
        else :
            model = [options.fitModel]
        if not options.setupOnly :
            ## if it does not exist already, create link to executable
            if not os.path.exists("combine") :
                os.system("cp -s $(which combine) .")
            ## prepare fit options
            minuitopt = ""
            if options.minuit :
                minuitopt = "--minimizerAlgo minuit"
            stableopt = ""
            if options.stable :
                stableopt = "--robustFit=1 --stepSize=0.5  --minimizerStrategy=0 --minimizerTolerance=0.1 --preFitValue=0.1  --X-rtd FITTER_DYN_STEP  --cminFallbackAlgo=\"Minuit;0.001\" "
            ## set up grid points in case of likelihood scan (option --grid)
            gridpoints = ""
            if options.fitAlgo == "grid" :
                if options.firstPoint == "" :
                    gridpoints = "--points %s --firstPoint 1 --lastPoint %s" % (options.gridPoints, options.gridPoints)
                else :
                    gridpoints = "--points %s --firstPoint %s --lastPoint %s" % (options.gridPoints, options.firstPoint, options.lastPoint)
            ## run expected limits
            print "Running maximum likelihood fit with options: "
            print "combine -M MultiDimFit --fastScan -m {mass} --algo={algo} -n {name} --cl {CL} {points} {minuit} {stable} {user} {input}.root ".format(mass=mass, algo=options.fitAlgo, name=options.name, CL=options.confidenceLevel, points=gridpoints, minuit=minuitopt, stable=stableopt, user=options.userOpt, input=model[0])
            fitresults=  ""
            if options.saveResults :
                fitresults = " | grep -A 10 -E '\s*--- MultiDimFit ---\s*' > multi-dim.fitresult"
            os.system("combine -M MultiDimFit -m {mass} --algo={algo} -n {name} --cl {CL} {points} {minuit} {stable} {user} {input}.root {result}".format(mass=mass, algo=options.fitAlgo, name=options.name, CL=options.confidenceLevel, points=gridpoints, minuit=minuitopt, stable=stableopt, user=options.userOpt, input=model[0], result=fitresults))
            if not options.firstPoint == "":
                os.system("mv higgsCombine{name}.MultiDimFit.mH{mass}.root higgsCombine{name}.MultiDimFit.mH{mass}-{label}.root".format(name=options.name, mass=mass, label="%s-%s" % (options.firstPoint, options.lastPoint)))
    if options.prepPLSig :
        ifile=0
        directoryList = os.listdir(".")
        ## create a hadd'ed file per crab directory
        for name in directoryList :
            if "crab_0" in name and not "." in name :
                if os.path.exists("batch_collected_%s.root" % ifile) :
                    os.system("rm batch_collected_%s.root" % ifile)
                os.system("hadd batch_collected_%s.root %s/res/*.root" % (ifile, name))
                ifile=ifile+1
        ## and finally hadd all sub files corresponding to each crab directory
        if not options.observedOnly :
            if os.path.exists("batch_collected.root") :
                os.system("rm batch_collected.root")
            os.system("hadd batch_collected.root batch_collected_*.root")
            os.system("rm batch_collected_*.root")
        ## in case there were no batch jobs run run interactively
        ## prepare binary workspace
        mass_value = directory[directory.rfind("/")+1:]
        mass_fixed = options.fixed_mass
        if options.fixed_mass == "":
            mass_fixed = mass_value

        ## combine datacard from all datacards in this directory
        create_card_workspace(mass_fixed)

        if not options.observedOnly :
            if ifile == 0 :
                ## calculate significance, batch_collected.root is the output file name expected by plot.cc
                os.system("combine -M ProfileLikelihood -t {toys} --significance --signalForSignificance={sig} -m {mass} -n batch_collected.root tmp.root".format(
                    toys=options.toys, sig=options.signal_strength, mass=mass_value))
        if not options.expectedOnly :
            ## calc observed significance
            #print "combine -M ProfileLikelihood --significance -m {mass} tmp.root".format(mass=mass_value)
            os.system("combine -M ProfileLikelihood --significance -m {mass} tmp.root".format(mass=mass_value))
    if options.prepMSSMxsec :
        ## prepare mass argument for limit calculation if configured such
        idx = directory.rfind("/")
        if idx == (len(directory) - 1):
            idx = directory[:idx - 1].rfind("/")
        mass_value  = directory[idx + 1:]
        #mass_string  = directory[idx + 1:]
        #mass_regex   = r"(?P<mass>[\+\-0-9\s]+)[a-zA-Z0-9]*"
        #mass_matcher = re.compile(mass_regex)
        #mass_value   = mass_matcher.match(mass_string).group('mass')
        ## combine datacard from all datacards in this directory
        inputcards = ""
        for card in os.listdir(".") :
            if "htt_" in card :
                if options.fitModelCategories == "" :
                    inputcards+=card[:card.find('.')]+'='+card+' '
                else :
                    allowed_categories = options.fitModelCategories.split(':')
                    for allowed in allowed_categories :
                        if allowed in card :
                            inputcards+=card[:card.find('.')]+'='+card+' '
        print "combineCards.py -S %s > tmp.txt" % inputcards
        os.system("combineCards.py -S %s > tmp.txt" % inputcards)
        ## move one signal to background
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/mssm_scaleS_movetoB.py %s -m %s tmp.txt" % (("--ggH" if options.ggH else ""), mass_value))
        ## prepare binary workspace
        os.system("text2workspace.py --default-morphing=%s -m %s -b tmp_%s.txt -o tmp.root"% (options.shape, mass_value, ("ggH" if options.ggH else "bbH")))
        ## if it does not exist already, create link to executable
        if not os.path.exists("combine") :
            os.system("cp -s $(which combine) .")
        ## prepare prefit option
        prefitopt = ""
        if options.noprefit :
            prefitopt = "-t -1"
        ## prepare fit option
        minuitopt = ""
        if options.minuit :
            minuitopt = "--minimizerAlgo minuit"
        qtildeopt = ""
        if options.qtilde :
            qtildeopt = "--qtilde 0"
        ## prepare mass options
        massopt = "-m %s " % mass_value
        ## run expected limits
        if not options.observedOnly :
            os.system("combine -M Asymptotic --run expected -C {CL} {minuit} {prefit} --minimizerStrategy {strategy} -n '-exp' {mass} {user} tmp.root".format(
                CL=options.confidenceLevel, minuit=minuitopt, prefit=prefitopt, strategy=options.strategy, mass=massopt, user=options.userOpt))
        ## run observed limit
        if not options.expectedOnly :
            os.system("combine -M Asymptotic --run observed -C {CL} {minuit} --minimizerStrategy {strategy} -n '-obs' {qtilde} {mass} {user} tmp.root".format(
                CL=options.confidenceLevel, minuit=minuitopt, qtilde=qtildeopt, strategy=options.strategy, mass=massopt, user=options.userOpt))
    if options.kill :
        directoryList = os.listdir(".")
        for name in directoryList :
            ## create a tmp shell script for each crab_0* directory
            ## w/o duplicating the .sh that might have been produced
            ## before
            if name.find("crab_0")>-1 and not name.find(".")>-1:
               os.system("crab -kill all -c %s" % name)
        if os.path.exists("observed") :
            os.chdir(os.path.join(subdirectory, "observed"))
            directoryList = os.listdir(".")
            for name in directoryList :
                ## create a tmp shell script for each crab_0* directory
                ## w/o duplicating the .sh that might have been produced
                ## before
                if name.find("crab_0")>-1 and not name.find(".")>-1:
                    os.system("crab -kill all -c %s" % name)
            os.chdir(subdirectory)
    if options.cleanup :
        os.system("rm -r crab*")
        if os.path.exists("observed") :
            os.chdir(os.path.join(subdirectiry, "observed"))
            os.system("rm -r crab*")
            os.chdir(subdirectory)
    ## always remove all tmp remainders from the parallelized harvesting
    tmps = os.listdir(os.getcwd())
    for tmp in tmps :
        if tmp.find("tmp")>-1 :
            if options.firstPoint == "" :
                os.system("rm %s" % tmp)
    if os.path.exists("observed") :
        tmps = os.listdir("%s/observed" % os.getcwd())
        for tmp in tmps :
            if tmp.find("tmp")>-1 :
                os.system("rm observed/%s" % tmp)
    # Remove any previous hashes
    os.system("rm -f limit_hash_*")
    # Create hash file for this call, so we can use the norepeat feature.
    hash_file = get_hash_for_this_call()
    os.system("touch %s" % hash_file)
    print "done"
