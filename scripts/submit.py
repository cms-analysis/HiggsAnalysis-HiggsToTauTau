#!/usr/bin/env python
#flake8: noqa
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="This is a script for job submission via crab or batch on a large scale or for the submission. In some cases, which require a more complex configuration it can also be used to execute a single interactive job with a pre-defined default configuration as it is generally used for analysis. The corresponding analysis processes are called and configured via command line options. The arguments ARG1, ARG2, ARG3, ... correspond to the job directories that have been prepared for submission. These directories should contain all datacards and input files needed for the execution of the job. They are supposed to end with a floating point number or with an integer number corresponding to the mass, for which the process is to be applied. There is a few exception to this common rule as explained in this parameter description. A small set of options and sub-options can still be passed on to this script. More dedicated options that should act on the scripts that are to be executed within this script can be piped through via the common option --options, enbraced by '...'. More explanation are given in section COMMON OPTIONS of this parameter description. This is meant to facilitate expert use if necessary.")
##
## MAIN OPTIONS
##
agroup = OptionGroup(parser, "MAIN OPTIONS", "These are the command line options that list all available processes that can be executed via this script. Each process is run with a default configuration that has been recently used for analysis. Depending on the process the execution of the script will result in the submission of a pre-defined set of batch jobs via lxb (lxq) or in a submission of a pre-defined set of jobs via crab. The options that will lead submission to lxb (lxq) are: --max-likelihood, --likelihood-scan, --multidim-fit, --asymptotic, --tanb+. The options that will lead to crab submission are: --significance, --CLs, --bayesian, --tanb. The latter requires the proper setup of a glite and a crab environment. Note that this is the case even if the submission would only take place via lxb (lxq), as the grid environment is used internally by crab. All options are explained in the following. All command line options in this section are exclusive. For the options --likelihood-scan, --asymptotic, --tanb+ it is possible to force interactive running. If run in batch mode the jobs will be split per mass.")
agroup.add_option("--goodness-of-fit", dest="optGoodnessOfFit", default=False, action="store_true",
                  help="Determine the goodness of fit equivalent to a chisquared. For the vexpected goodness of fit this is a toys based procedure. The fit will be applied to the SM with single signal modifier. When submitting to lxb (lxq) you can configure the queue to which the jobs will be submitted as described in section BATCH OPTIONS of this parameter description. [Default: False]")
agroup.add_option("--max-likelihood", dest="optMLFit", default=False, action="store_true",
                  help="Perform a maximum likelihood fit scan to determine the signal strength from the datacards in the directory/ies corresponding to ARGs. This fit will be applied to the SM with single signal modifier. The pre-configuration corresponds to --stable, --rMin -5, --rMax 5. This pre-configuration will be applied irrespective of the mass, for which the process should be executed. The process will be executed via lxb (lxq), split by each single mass point that is part of ARGs or as a single interactive job when using the option --interactive. When submitting to lxb (lxq) you can configure the queue to which the jobs will be submitted as described in section BATCH OPTIONS of this parameter description. [Default: False]")

agroup.add_option("--likelihood-scan", dest="optNLLScan", default=False, action="store_true",
                  help="Perform a maximum likelihood scan to determine the signal strength from the datacards in the directory/ies corresponding to ARGs. This scan will be applied to the SM with single signal modifier. The pre-configuration corresponds to --points 100, --rMin -2, --rMax 2. This pre-configuration will be applied irrespective of the mass, for which the process should be executed. The process will be executed via lxb (lxq), split by each single mass point that is part of ARGs or as a single interactive job when using the option --interactive. When submitting to lxb (lxq) you can configure the queue to which the jobs will be submitted as described in section BATCH OPTIONS of this parameter description. When running in batch mode you can go one level up in the expected directory structure as described in the head of this section. [Default: False]")
agroup.add_option("--multidim-fit", dest="optMDFit", default=False, action="store_true",
                  help="Perform a maximum likelihood fit in two dimensions to determine the signal strength from the datacards in the directory/ies corresponding to ARGs. This option requires the configuration of a dedicated physics model as described in section MODEL OPTIONS of this parameter description. The process will be executed via lxb (lxq). [Default: False]")
agroup.add_option("--significance", dest="optSig", default=False, action="store_true",
                  help="Calculate the expected significance from likelihood profiling. The expected significance and its uncertainties are based on toys. This script will submit toys to a batch system or to the grid using crab. This action will require a grid certificate. You can configure this script to submit to the grid or to submit to lxb (lxq) as described in section SIGNIFICANCE OPTIONS in this parameter description. You can monitor and receive the results of your jobs once finished using the script limit.py using the CRAB OPTIONS as explained in the parameter description, there. [Default: False]")
agroup.add_option("--significance-frequentist", dest="optSigFreq", default=False, action="store_true",
                  help="Calculate the expected and observed frequentist significance a la HCG. [Default: False]")
agroup.add_option("--pvalue-frequentist", dest="optPValue", default=False, action="store_true",
                  help="Calculate the expected and observed frequentist p-value a la HCG. [Default: False]")
agroup.add_option("--asymptotic", dest="optAsym", default=False, action="store_true",
                  help="Calculate asymptotic CLs limits from the datacards in the directory/ise corresponding to ARGs. The process will be executed via lxb (lxq), split by each single mass point that is part of ARGs or as a single interactive job when using the option --interactive. When submitting to lxb (lxq) you can configure the queue to which the jobs will be submitted as described in section BATCH OPTIONS of this parameter description. When running in batch mode you can go one level up in the expected directory structure as described in the head of this section. [Default: False]")
agroup.add_option("--CLs", dest="optCLs", default=False, action="store_true",
                  help="Calculate the observed and expected full CLs limits. This method is completely toy based. This script will submit toys to the grid using crab. This action will require a grid certificate. As this operation is very computing intensive there is no pre-defined option to submit to lxb (lxq). You can monitor and receive the results of your jobs once finished using the script limit.py using the CRAB OPTIONS as explained in the parameter description, there. [Default: False]")
agroup.add_option("--bayesian", dest="optBayes", default=False, action="store_true",
                  help="Calculate the observed and expected bayesian limits. This method is completely toy based. This script will submit toys, which are needed for the markov chain integration to the grid using crab. This action will require a grid certificate. As this operation is very computing intensive there is no pre-defined option to submit to lxb (lxq). You can monitor and receive the results of your jobs once finished using the script limit.py using the CRAB OPTIONS as explained in the parameter description, there. [Default: False]")
agroup.add_option("--tanb", dest="optTanb", default=False, action="store_true",
                  help="Calculate the observed and expected limits directly in the MSSM mA-tanb plane based on full CLs limits. This method is completely toy based. This script will prepare the directory structure to do these calculations and submit toys to the grid using crab. This action will require a grid certificate. As this operation is very computing intensive there is no pre-defined option to submit to lxb (lxq). You can monitor and receive the results of your jobs once finished using the script limit.py using the CRAB OPTIONS as explained in the parameter description, there. [Default: False]")
agroup.add_option("--tanb+", dest="optTanbPlus", default=False, action="store_true",
                  help="Calculate the observed and expected limits directly in the MSSM mA-tanb plane based on asymptotic CLs limits. This script will prepare the directory structure to do these calculations and submit and submit the required asymptotic limit calculation for each corresponding point in mA to lxb (lxq). The process will be executed via lxb (lxq), split by each single mass point that is part of ARGs or as a single interactive job when using the option --interactive. When submitting to lxb (lxq) you can configure the queue to which the jobs will be submitted as described in section BATCH OPTIONS of this parameter description. When running in batch mode you can go one level up in the expected directory structure as described in the head of this section. [Default: False]")
agroup.add_option("--injected", dest="optInject", default=False, action="store_true",
                  help="Calculate expected asymptotic CLs limits, frequentist significance or p-value with a SM signal injected from the datacards in the directory/ies corresponding to ARGs. You can determine what calculations should be applied by the option --injected-method. These calculations are fully toy based and will require a large number of toys, which will be submitted via lxb (lxq). For each toy a pseudo-dataset will be created and an observed limit, observed frequentist significance or p-value will be calculated. It is possible to give an input file from which the pulls of the nuisance parameters will be taken, when running the calculations. The median and quantiles of the tossed toys define the expected limit with signal injected and the uncertainties. This script internally calls the script lxb-injected.py. [Default: False]")
parser.add_option_group(agroup)
##
## COMMON OPTIONS
##
bgroup = OptionGroup(parser, "COMMON OPTIONS", "These are command line options that are not specific to one or the other main option. Where such restrictions exist they are specified in the corresponding parameter description below.")
bgroup.add_option("--printOnly", dest="printOnly", default=False, action="store_true",
                  help="Only print the command line option(s) to the screen. Do not execute them. This can be used if you only want to know the command line option to use it elsewhere in a slightly modified way. [Default: False]")
bgroup.add_option("--cycles", dest="cycles", default=1, type="int",
                  help="Number of submission cycles for crab job submission. This option only applies to the main options --CLs and --tanb. For all other main options it has no effect. One submission cycle consists of 50 crab jobs. [Default: 1]")
bgroup.add_option("--options", dest="opt", default="", type="string",
                  help="You can use this string for additional options that can be passed on to the scripts that are executed within this script. NB: these options should be enclosed by \"...\". [Default: \"\"]")
parser.add_option_group(bgroup)
##
## BATCH OPTIONS
##
cgroup = OptionGroup(parser, "BATCH OPTIONS", "These are the command line options that can be used to configure lxb (lxq) batch job submission via the script lxb_submit.py. Batch job submission of this type is applicable for the following options: --likelihood-scan, --asymptotic, --tanb+. When using batch job submission in one of these main options it is possible to go up by one level in the directory structure when specifying ARGs as described in the head of this parameter description. Note: when runnign in batch mode batch jobs are split by each mass directory that can be found in the directory structure.")
cgroup.add_option("--toys", dest="toys", default="5000", type="string",
                  help="Set the number toys that you want to use to calculate the toy based expectations. This is valid for the calculation of the expected significance (--significance) and for the calculation of the expected 95% CL upper asymptotic CLs limit with a SM signal injected (--injected). [Default: 5000]")
cgroup.add_option("-q", "--queue", dest="queue", default="-q 8nh", type="string",
                  help="The queue, to which to submit the jobs. [Default: \"-q 8nh\"]")
cgroup.add_option("--interactive", dest="interactive", default=False, action="store_true",
                  help="Force interactive running. Do not run in batch mode. This will lead to one large execution. [Default: False]")
cgroup.add_option("--lxq", dest="lxq", default=False, action="store_true",
                  help="Specify this option when running on lxq instead of lxb for simple batch job submissions. [Default: False]")
cgroup.add_option("--condor", dest="condor", default=False, action="store_true",
                  help="Specify this option when running on condor instead of lxb for simple batch job submissions. [Default: False]")
parser.add_option_group(cgroup)
##
## MODEL OPTIONS
##
dgroup = OptionGroup(parser, "MODEL OPTIONS", "These are the command line options that can be used to configure the submission of multi-dimensional fits or asymptotic limits that do require specific models. Specific models can be used for option --multidim-fit and for option --asymptotic. Possible model options for option --multidim-fit are: ggH-bbH (MSSM), ggH-qqH (SM), rV-rF (SM) and cV-cF (SM). Possible model options for option --asymptotic are: \"\" (SM), ggH (MSSM) and bbH (MSSM).")
dgroup.add_option("--physics-model", dest="fitModel", default="", type="choice", choices=["cb-ctau", "cl-cq", "ggH-bbH", "ggH-qqH", "rV-rF", "cV-cF", "ggH", "bbH", ""],
                  help="Define the model for which you want to submit the process with option --multidim-fit ('ggH-bbH' (MSSM), 'ggH-qqH' (SM) and 'cV-cF' (SM)) or option --asymptotic ('ggH' (MSSM), 'bbH' (MSSM) and '' (SM)). [Default: \"\"]")
parser.add_option_group(dgroup)
##
## LIKELIHOOD-SCAN
##
egroup = OptionGroup(parser, "LIKELIHOOD-SCAN OPTIONS", "These are the command line options that can be used to configure the submission of the likelihood scan. The number of scan points the minimum and the maximum of the scan can be given. Note that the likelihood scan is only possible for the SM case with all signal contributions as single POI. At the moment there is no job splitting implemented, yet.")
egroup.add_option("--points", dest="points", default="100", type="string",
                  help="Number of scan points for the likelihood scan. [Default: 100]")
egroup.add_option("--rMin", dest="rMin", default="-2.0", type="string",
                  help="Minimum of the scan. [Default: -2.0]")
egroup.add_option("--rMax", dest="rMax", default="+4.0", type="string",
                  help="Maximum of the scan. [Default: +4.0]")
parser.add_option_group(egroup)
##
## MULTIDIM-FIT
##
jgroup = OptionGroup(parser, "MULTIDIM-FIT OPTIONS", "These are the command line options that can be used to configure the submission of multi-dimensional maximum likelihood fits. You can configure whether you want to run with option --fastScan or not.")
jgroup.add_option("--fastScan", dest="fastScan", default=False, action="store_true",
                  help="In general the central values of all nuisance parameters are re-evaluated at each scan point of the maximum likelihood function. Choose this option if you want the central values of the nuisance parameters only evaluated in the minimum of the likelihood fit. [Default: False]")
parser.add_option_group(jgroup)
##
## SIGNIFICANCE
##
fgroup = OptionGroup(parser, "SIGNIFICANCE OPTIONS", "These are the command line options that can be used to configure the submission of toys for significance calculations. The toys can be submitted to the grid or to lxb (lxq) using crab. The number of toys per mass that will be the same for all masses can be configured via the option --toys as described in section BATCH OPTIONS. The number of crab jobs that will be the same for all masses can be configured via the option --jobs as described in this section.")
fgroup.add_option("--jobs", dest="jobs", default="100", type="string",
                  help="Set the number crab jobs that you want to submit to calculate the toy based expected significance. [Default: 100]")
fgroup.add_option("--seed", dest="seed", default="", type="string",
                  help="Per default toys are run with a random seed. In case you want to run on pseudo toys with a well defined seed add the seed here. If \"\" this option will have no effect. [Default: \"\"]")
fgroup.add_option("--uncapped", dest="uncapped", default=False, action="store_true",
                  help="Use uncapped option, a la ATLAS, to allow for p-values larger than 0.5 and negatove significances in case of deficits in the data. [Default: False]")
fgroup.add_option("--grid", dest="grid", default=False, action="store_true",
                  help="Use this option if you want to submit your jobs to the grid. Otherwise they will be submitted to lxb (lxq). [Default: False]")
parser.add_option_group(fgroup)
##
## INJECTED OPTIONS
##
ggroup = OptionGroup(parser, "INJECTED OPTIONS", "These are the command line options that can be used to configure lxb (lxq) batch job submission for 95% CL upper asymptotic CLs limits, (frequentist) significance or p-value calculations with a SM signal injected via the script lxb-injected.py, which uses the script limit.py. The expected limit with a SM signal injected is obtained from a large sample of toys. For each toy a pseudo data set is prepared and the observed limit/significance/p-value is calculated. After the toys have been produced you can collect the output using the script limit.py with option --injected. You can also use this script to do this using the option --collect-injected-toys, which will collect the injected toys and runthe observe limit on data. The expected limit and the uncertainties are obtained from the median and the quantiles of the collected toys. The number of toys (--toys) and the batch queue options (--queue) can be configured using the options described in section BATCH OPTIONS of this parameter description. The option --bunch-masses as described below can be used to define a maximal number of masses that will be bunched into a single job before a new job is created. The option --external-pulls can be used to pass a pre-defined set of nuisance parameters to limit.py that will be used instead of determining the central values of the nuisances by the prefit for each toy on its own.")
ggroup.add_option("--injected-method", dest="injected_method", default="--asymptotic", type="choice", choices=["--asymptotic", "--significance-frequentist", "--pvalue-frequentist","--max-likelihood"],
                  help="Indicate here the method that you want to use the injected signal toys for. Available choices are '--asymptotic', '--significance-frequentist','--pvalue-frequentist' and '--max-likelihood' [Default: --asymptotic]")
ggroup.add_option("--bunch-masses", dest="nmasses", default="10", type="string",
                  help="This is the maximal number of masses that will be bunched into a single job, before a new job will be created. If you want to do the calculation for nine masses, 1000 tos and maximal 4 masses per bunch you will create 3000 jobs, 2000 jobs for 4 masses each and 1000 jobs for a single mass. [Default: 10]")
ggroup.add_option("--external-pulls", dest="nuisances", default="", type="string",
                  help="Specify the full path to a root output file of limit.py with option --max-likelihood (e.g. mlfit.root) to enforce the use of pre-calculated central values of the nuisance parmeters involved in this fit. It is in the responsibility of the user that the nuisance parameter names in the output file and the nuisance parameter names in the current workspace fit together. The limit will be run w/ option --no-prefit. For more details have a look to the description of option --external-pulls of the script limit.py. [Default: \"\"]")
ggroup.add_option("--injected-mass", dest="injected_mass", type="string", default="125",
                  help="Mass of the signal that should be injected into the background only hypothesis from simulation. [Default: 125]")
ggroup.add_option("--SplusB", dest="signal_plus_BG", default=True, action="store_true",
                  help="When using options --external-pulls, use the fit results with signal plus background. If 'False' the fit result of the background only hypothesis is used. [Default: False]")
ggroup.add_option("--collect-injected-toys", dest="calculate_injected", default=False, action="store_true",
                  help="Collect toys and calculate observed limit/significance/p-value using lxb (lxq). To run with this options the toys have to be produced beforehand. [Default: False]")
parser.add_option_group(ggroup)
##
## TANB+
##
hgroup = OptionGroup(parser, "TANB+ OPTIONS", "These are the command line options that can be used to configure the submission of tanb+. This option is special in the way that it needs modifications of the directory structure before the limits can be run. Via the script submit.py this setup can only be run interactively using the commend option --setup. Once the directory structure has been set up the limit calculation can be run interactively or in batrch mode.")
hgroup.add_option("--setup", dest="setup", default=False, action="store_true",
                  help="Use the script to setup the directory structure for direct mA-tanb limits interactively. If false the the script will assume that this has already been done and execute the limit calculation either in batch mode or interactive. [Default: False]")
hgroup.add_option("--old", dest="old", default=False, action="store_true",
                  help="Switch between tanb_grid.py and tanb_grid_new.py. If validated this could be deleted [Default: False]")
parser.add_option_group(hgroup)

##
## FULL CLs
##
igroup = OptionGroup(parser, "CLS OPTIONS", "These are the command line options that can be used to configure the submission of full CLs limits in the SM.")
igroup.add_option("--priority", dest="priority", default=False, action="store_true",
                  help="Do grid submission with priority user roles (if available). This is only of relevance for vgrid submissions. [Default: False]")
igroup.add_option("--lsf", dest="lxbsubmit", default=False, action="store_true",
                  help="Do the submission on lxb. [Default: False]")
igroup.add_option("--skip-server", dest="skipserver", default=False, action="store_true",
                  help="Do not submit via crab server. [Default: False]")
parser.add_option_group(igroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import re
import os
import random

from HiggsAnalysis.HiggsToTauTau.utils import contained
from HiggsAnalysis.HiggsToTauTau.utils import is_number
from HiggsAnalysis.HiggsToTauTau.utils import get_mass

def subvec(vec, min, max):
    '''
    Create a subvector of a vector of strings that contains
    an integer and a / as substring
    '''
    subvec = []
    for directory in vec :
        if re.search(r"^.*/\d+?$", directory) :
            mass = int(directory[directory.rfind("/")+1:])
            if min <= mass and mass <= max:
                subvec.append(directory)
    return subvec

def vec2str(vec, delim=" "):
    '''
    Return a string concatenated from elements of a vector
    seperate these elements by a deliminator as specified
    by delim. The default deliminator is " "
    '''
    str = ""
    for i in vec:
        str+=i
        str+=delim
    return str

def directories(args) :
    ## prepare structure of parent directories
    dirs = []
    for dir in args :
        if is_number(get_mass(dir)) or get_mass(dir) == "common" :
            dir = dir[:dir.rstrip('/').rfind('/')]
        if not dir in dirs :
            dirs.append(dir)
    ## prepare mapping of masses per parent directory
    masses = {}
    for dir in dirs :
        buffer = []
        for path in args :
            if dir+'/' in path :
                if is_number(get_mass(path)) :
                    mass = get_mass(path)
                    if not contained(mass, buffer) :
                        buffer.append(mass)
        masses[dir] = list(buffer)
    return (dirs, masses)

def lxb_submit(dirs, masses, cmd='--asymptotic', opts='', cycle='') :
    '''
    do a lxb submission for jobs that can be executed via limit.py.
    dirs corresponds to a list of input directories, masses to a
    dictionary of masses per dir, cmd to the complete main option
    of limit.py and opts to additional options that should be passed
    on to limit.py.
    '''
    for dir in dirs:
        if 'asymptotic' in cmd :
            cmd_ext = '-limit'
        elif 'max-likelihood' in cmd :
            cmd_ext = '-mlfit'
        elif 'pvalue' in cmd :
            cmd_ext = '-pval'
        elif 'significance' in cmd :
            cmd_ext = '-sig'
        else :
            cmd_ext = ''
        ana = dir[:dir.rfind('/')]
        limit = dir[len(ana)+1:]
        jobname = dir.replace('/', '-').replace('LIMITS','scripts')+cmd_ext+cycle
        ## add compliance with lxq or condor
        sys = ''
        if options.lxq :
            sys = ' --lxq'
        elif options.condor :
            sys = ' --condor'
        ## create inputs corresponding to the masses per parent directory in dirs
        inputs = ""
        for mass in masses[dir] :
            inputs+= dir+'/'+mass+' '
        ## create submission scripts
        if options.printOnly :
            print "lxb-limit.py --name {JOBNAME} {CONDOR} --batch-options \"{QUEUE}\" --limit-options \"{METHOD} {OPTS}\" {SYS} {DIR}".format(
                JOBNAME=jobname, DIR=inputs.rstrip(), QUEUE=options.queue, METHOD=cmd, OPTS=opts.rstrip(), SYS=sys, CONDOR="--condor" if options.condor else "")
        else:
            os.system("lxb-limit.py --name {JOBNAME} {CONDOR} --batch-options \"{QUEUE}\" --limit-options \"{METHOD} {OPTS}\" {SYS} {DIR}".format(
                JOBNAME=jobname, DIR=inputs.rstrip(), QUEUE=options.queue, METHOD=cmd, OPTS=opts.rstrip(), SYS=sys, CONDOR="--condor" if options.condor else ""))
            ## execute
            if not options.condor:
                os.system("./{JOBNAME}_submit.sh".format(JOBNAME=jobname))
            else:
                os.system("condor_submit {JOBNAME}_submit.sh".format(JOBNAME=jobname))
            ## store
            os.system("mv {JOBNAME}_submit.sh {JOBNAME}".format(JOBNAME=jobname))

##
## GOODNESS OF FIT
##
if options.optGoodnessOfFit :
    if options.interactive :
        for dir in args :
            mass = get_mass(dir)
            if mass == 'common' :
                continue
            if options.printOnly :
                if options.calculate_injected :
                    print "limit.py --goodness-of-fit --collect-injected-toys {USER} {DIR}".format(USER=options.opt, DIR=dir, )
                else :
                    print "limit.py --goodness-of-fit --expectedOnly --toys {TOYS} --seed {SEED} {USER} {DIR}".format(
                        TOYS=options.toys, SEED=random.randint(1, 999999), USER=options.opt, DIR=dir, )
            else :
                if options.calculate_injected :
                    os.system("limit.py --goodness-of-fit --collect-injected-toys {USER} {DIR}".format(USER=options.opt, DIR=dir, ))
                    os.system("limit.py --goodness-of-fit --observedOnly {USER} {DIR}".format(USER=options.opt, DIR=dir))
                else:
                    os.system("limit.py --goodness-of-fit --expectedOnly --toys {TOYS} --seed {SEED} {USER} {DIR}".format(
                        TOYS=options.toys, SEED=random.randint(1, 999999), USER=options.opt, DIR=dir, ))
    else :
        ## directories and mases per directory
        struct = directories(args)
        if options.calculate_injected :
            for dir in struct[0] :
                for mass in struct[1][dir] :
                    os.system("limit.py --goodness-of-fit --collect-injected-toys {DIR}/{MASS}".format(DIR=dir, MASS=mass))
            lxb_submit(struct[0], struct[1], "--goodness-of-fit", "--observedOnly {USER}".format(USER=options.opt))
        else: 
            cycle = options.cycles
            while cycle>0 :
                lxb_submit(struct[0], struct[1], "--goodness-of-fit", "--expectedOnly --toys {TOYS} --seed {SEED} {USER}".format(TOYS=options.toys, SEED=random.randint(1, 999999), USER=options.opt), "-{CYCLE}".format(CYCLE=cycle-1))
                cycle = cycle-1
##
## MAX-LIKELIHOOD
##
if options.optMLFit :
    if options.interactive :
        for dir in args :
            mass = get_mass(dir)
            if mass == 'common' :
                continue
            if options.printOnly :
                print"limit.py --max-likelihood --stable-old --rMin -5 --rMax 5 {DIR}".format(DIR=dir)
            else :
                os.system("limit.py --max-likelihood --stable-old --rMin -5 --rMax 5 {USER} {DIR}".format(USER=options.opt, DIR=dir))
    else :
        ## directories and mases per directory
        struct = directories(args)
        lxb_submit(struct[0], struct[1], "--max-likelihood", "--stable-old --rMin -5 --rMax 5 {USER}".format(USER=options.opt))
##
## LIKELIHOOD-SCAN
##
if options.optNLLScan :
    ## add the footprint of the scan
    #for dir in args :
    #    footprint = open("{DIR}/.scan".format(DIR=dir), "w")
    #    footprint.write("points : {POINTS}\n".format(POINTS=options.points))
    #    footprint.write("r : {RMIN} \t {RMAX}\n".format(RMIN=options.rMin, RMAX=options.rMax))
    #    footprint.close()
    if options.interactive :
        for dir in args :
            mass = get_mass(dir)
            if mass == 'common' :
                continue
            if options.printOnly :
                print "limit.py --likelihood-scan --points {POINTS} --rMin {RMIN} --rMax {RMAX} {USER} {DIR}".format(
                    POINTS=options.points, RMIN=options.rMin, RMAX=options.rMax, USER=options.opt, DIR=dir)
            else :
                os.system("limit.py --likelihood-scan --points {POINTS} --rMin {RMIN} --rMax {RMAX} {USER} {DIR}".format(
                    POINTS=options.points, RMIN=options.rMin, RMAX=options.rMax, USER=options.opt, DIR=dir))
    else :
        ## directories and mases per directory
        struct = directories(args)
        lxb_submit(struct[0], struct[1], "--likelihood-scan", "--points {POINTS} --rMin {RMIN} --rMax {RMAX} {USER}".format(
            POINTS=options.points, RMIN=options.rMin, RMAX=options.rMax, USER=options.opt))
##
## MULTIDIM-FIT
##
if options.optMDFit :
    for dir in args :
        mass = get_mass(dir)
        if mass == 'common' :
            continue
        ## define jobname prefix that will be combined with the model name
        prefix = dir[:dir.rfind(mass)].rstrip('/')
        head = prefix[:prefix.rfind('/')]
        prefix = prefix[head.rfind('/')+1:].replace('/', '-')
        ## define command line, model and model options
        cmd   = ""
        model = ""
        opts  = ""
        ## MSSM ggH versus bbH
        if "ggH-bbH" in options.fitModel :
            from HiggsAnalysis.HiggsToTauTau.mssm_multidim_fit_boundaries import mssm_multidim_fit_boundaries as bounds
            cmd   = "lxb-multidim-fit.py --name {PRE}-GGH-BBH-{MASS} --njob 50 --npoints 800".format(PRE=prefix, MASS=mass)
            model = "--physics-model 'ggH-bbH=HiggsAnalysis.HiggsToTauTau.PhysicsBSMModel:floatingMSSMXSHiggs'"
            opts  = "--physics-model-options 'modes=ggH,bbH;ggHRange=0:{GGH};bbHRange=0:{BBH}'".format(GGH=bounds["ggH-bbH",mass][0], BBH=bounds["ggH-bbH",mass][1])
            print mass, bounds["ggH-bbH",mass][0], bounds["ggH-bbH",mass][1]
        ## MSSM cb versus ctau
        if "cb-ctau" in options.fitModel :
            from HiggsAnalysis.HiggsToTauTau.mssm_multidim_fit_boundaries import mssm_multidim_fit_boundaries as bounds
            cmd   = "lxb-multidim-fit.py --name {PRE}-CB-CTAU-{MASS} --njob 50 --npoints 800".format(PRE=prefix, MASS=mass)
            model = "--physics-model 'cb-ctau=HiggsAnalysis.HiggsToTauTau.BSMHiggsCouplings:CbCtauMSSMHiggs'"
            opts  = "--physics-model-options 'cbRange=0:{CB};ctauRange=0:{CTAU}'".format(CB=bounds["cb-ctau",mass][0], CTAU=bounds["cb-ctau",mass][1])
        ## MSSM cb versus ctau
        if "cl-cq" in options.fitModel :
            from HiggsAnalysis.HiggsToTauTau.mssm_multidim_fit_boundaries import mssm_multidim_fit_boundaries as bounds
            cmd   = "lxb-multidim-fit.py --name {PRE}-CL-CQ-{MASS} --njob 50 --npoints 800".format(PRE=prefix, MASS=mass)
            model = "--physics-model 'cl-cq=HiggsAnalysis.HiggsToTauTau.BSMHiggsCouplings:ClCqMSSMHiggs'"
            opts  = "--physics-model-options 'clRange=0:{CL};cqRange=0:{CQ}'".format(CL=bounds["cl-cq",mass][0], CQ=bounds["cl-cq",mass][1])
        ## SM ggH versus qqH (this configuration is optimized for mH=125)
        elif "ggH-qqH" in options.fitModel :
            cmd   = "lxb-multidim-fit.py --name {PRE}-GGH-QQH-{MASS} --njob 400 --npoints 16".format(PRE=prefix, MASS=mass)
            model = "--physics-model 'ggH-qqH=HiggsAnalysis.CombinedLimit.PhysicsModel:floatingXSHiggs'"
            opts  = "--physics-model-options 'modes=ggH,qqH ggHRange=0:4 qqHRange=0:4'"
        ## SM rV versus rF (this configuration is optimized for mH=125)
        elif "rV-rF" in options.fitModel :
            cmd   = "lxb-multidim-fit.py --name {PRE}-RV-RF-{MASS} --njob 400 --npoints 16".format(PRE=prefix, MASS=mass)
            model = "--physics-model 'rV-rF=HiggsAnalysis.CombinedLimit.PhysicsModel:rVrFXSHiggs'"
            #opts  = "--physics-model-options 'rVRange=0:5 rFRange=0:4'"
            opts  = "--physics-model-options 'rVRange=-3:5 rFRange=-2:4'"
        ## SM cV versus cF (this configuration is optimized for mH=125)
        elif "cV-cF" in options.fitModel :
            cmd   = "lxb-multidim-fit.py --name {PRE}-CV-CF-{MASS} --njob 300 --npoints 12".format(PRE=prefix, MASS=mass)
            model = "--physics-model 'cV-cF=HiggsAnalysis.CombinedLimit.HiggsCouplings:cVcF'"
            opts  = "--physics-model-options 'cVRange=0:3 cFRange=0:2'"            
        ## add lxq compliance
        sys = ""
        if options.lxq :
            sys = " --lxq"
        ## add batch options
        queue = " --batch-options '%s'" % options.queue
        ## add fastScan option
        fastScan = " --limit-options '--fastScan'" if options.fastScan else ""
        if options.printOnly :
            print "{CMD} {MODEL} {OPTS} {FAST} {QUEUE} {SYS} {USER} {DIR}".format(
                CMD=cmd, MODEL=model, OPTS=opts, FAST=fastScan, QUEUE=queue, SYS=sys, USER=options.opt, DIR=dir)
        else :
            os.system("{CMD} {MODEL} {OPTS} {FAST} {QUEUE} {SYS} {USER} {DIR}".format(
                CMD=cmd, MODEL=model, OPTS=opts, FAST=fastScan, QUEUE=queue, SYS=sys, USER=options.opt, DIR=dir))
##
## SIGNIFICANCE
##
if options.optSig :
    opt = ' --lsf' if not options.grid else ''
    opt+= ' --seed %s' % options.seed if not options.seed == "" else ''
    if options.printOnly :
        print "submit-slave.py --method significance -t {TOYS} -j {JOBS} {USER} {OPT} {MASSES}".format(
            TOYS=options.toys, JOBS=options.jobs, USER=options.opt, OPT=opt, MASSES=' '.join(args))
    else :
        os.system("submit-slave.py --method significance -t {TOYS} -j {JOBS} {USER} {OPT} {MASSES}".format(
            TOYS=options.toys, JOBS=options.jobs, USER=options.opt, OPT=opt, MASSES=' '.join(args)))
##
## SIGNIFICANCE (FREQUENTIST) OR PVALUE 
##
if options.optSigFreq or options.optPValue :
    method = ''
    if options.optSigFreq :
        method = '--significance-frequentist'
    elif options.optPValue :
        method = '--pvalue'
    uncapped = ''
    if options.uncapped :
        uncapped = '--uncapped'
    if options.interactive :
        for dir in args :
            mass = get_mass(dir)
            if mass == 'common' :
                continue
            if options.printOnly :
                print "limit.py {METHOD} {UNCAPPED} {USER} {DIR}".format(METHOD=method, UNCAPPED=uncapped, USER=options.opt, DIR=dir)
            else :
                os.system("limit.py {METHOD} {UNCAPPED} {USER} {DIR}".format(METHOD=method, UNCAPPED=uncapped, USER=options.opt, DIR=dir))
    else :
        ## directories and mases per directory
        struct = directories(args)
        lxb_submit(struct[0], struct[1], method, "{UNCAPPED} {USER}".format(UNCAPPED=uncapped, USER=options.opt))
##
## ASYMPTOTIC (with dedicated models)
##
if options.optAsym :
    ## define command line, model and model options
    cmd   = "--asymptotic"
    model = ""
    opts  = ""
    ## MSSM ggH while bbH is profiled (GGH-BOUND will be resolved in limit.create_card_workspace_with_physics_model)
    if "ggH" in options.fitModel :
        model = "--physics-model 'tmp=HiggsAnalysis.HiggsToTauTau.PhysicsBSMModel:floatingMSSMXSHiggs'"
        opts  = "--physics-model-options 'modes=ggH;ggHRange=0:GGH-BOUND'"
    ## MSSM bbH while ggH is profiled (BBH-BOUND will be resolved in limit.create_card_workspace_with_physics_model)
    elif "bbH" in options.fitModel :
        model = "--physics-model 'tmp=HiggsAnalysis.HiggsToTauTau.PhysicsBSMModel:floatingMSSMXSHiggs'"
        opts  = "--physics-model-options 'modes=bbH;bbHRange=0:BBH-BOUND'"
    ## prepare calculation
    if options.interactive :
        for dir in args :
            mass = get_mass(dir)
            if mass == 'common' :
                continue
            if options.printOnly :
                print "limit.py {CMD} {MODEL} {OPTS} {USER} {DIR}".format(CMD=cmd, MODEL=model, OPTS=opts, USER=options.opt, DIR=dir)
            else :
                os.system("limit.py {CMD} {MODEL} {OPTS} {USER} {DIR}".format(CMD=cmd, MODEL=model, OPTS=opts, USER=options.opt, DIR=dir))
    else :
        ## directories and mases per directory
        struct = directories(args)
        lxb_submit(struct[0], struct[1], cmd, "{MODEL} {OPTS} {USER}".format(MODEL=model, OPTS=opts, USER=options.opt))
##
## INJECTED (asymptotic limits with signal injected, implementation for SM only)
##
if options.optInject :
    ## the input for lxb-injected.py should be a path, that is passed on as an
    ## option and the masses in question. Prepare here the corresponding paths
    ## and directories.
    paths = []
    dirs = {}
    for dir in args :
        head = dir[:dir.rstrip('/').rfind('/')]
        if not contained(head, paths) :
            paths.append(head)
            dirs[head] = []
    for dir in args :
        for path in paths :
            if path in dir :
                tail = dir[dir.rstrip('/').rfind('/')+1:]
                if is_number(tail) :
                    dirs[path].append(tail)
    if not options.calculate_injected :
        ## prepare options
        opts = options.opt
        if options.injected_method == "--max-likelihood" :
            folder_extension = "-mlfit"
        elif options.injected_method == "--asymptotic" :
            folder_extension = "-limit"
        elif options.injected_method == "--significance-frequentist" :
            folder_extension = "-sig"
        elif options.injected_method == "--pvalue-frequentist" :
            folder_extension = "-pval"
        if not options.injected_method == "--max-likelihood" :
            opts+=" --observedOnly"
        if not options.nuisances == "" :
            opts+=" --no-prefit --external-pulls \"{PATH}\" --signal-plus-background {SPLUSB}".format(PATH=options.nuisances, SPLUSB=options.signal_plus_BG)
        method = options.injected_method
        ## do the submit
        for path in paths :
            jobname = "injected-"+path[path.rstrip('/').rfind('/')+1:]+folder_extension
            if options.printOnly :
                print "lxb-injected.py --name {NAME} --method {METHOD} --input {PATH} {LXQ} {CONDOR} --batch-options \"{SUB}\" --toys {NJOB} --mass-points-per-job {NMASSES} --limit-options \"{OPTS}\" --injected-mass {INJECTEDMASS} {MASSES}".format(
                    NAME=jobname, METHOD=options.injected_method, PATH=path, SUB=options.queue, NJOB=options.toys, NMASSES=options.nmasses, OPTS=opts, INJECTEDMASS=options.injected_mass, MASSES=' '.join(dirs[path]), LXQ="--lxq" if options.lxq else "", CONDOR="--condor" if options.condor else "")
            else :
                os.system("lxb-injected.py --name {NAME} --method {METHOD} --input {PATH} {LXQ} {CONDOR} --batch-options \"{SUB}\" --toys {NJOB} --mass-points-per-job {NMASSES} --limit-options \"{OPTS}\" --injected-mass {INJECTEDMASS} {MASSES}".format(
                    NAME=jobname, METHOD=options.injected_method, PATH=path, SUB=options.queue, NJOB=options.toys, NMASSES=options.nmasses, OPTS=opts, INJECTEDMASS=options.injected_mass, MASSES=' '.join(dirs[path]), LXQ="--lxq" if options.lxq else "", CONDOR="--condor" if options.condor else ""))
    else :
        ## directories and masses per directory
        print "Collecting results"
        struct = directories(args)
        ## subtract global minimum of NLL as function of all available masses for MLFIT outputs for mass likelihood estimate
        ## before collecting all toys; for all other options follow the standard procedures defined in limit.py
        if options.injected_method == "--max-likelihood" :
            ## first collect all toys that have been run
            for dir in struct[0] :
                print "subtracting global minimum from NLL for dir:", dir
                os.system("massDeltaNLL.py --histname higgsCombineMLFIT*.root {DIR}".format(DIR=dir))
                for mass in struct[1][dir] :
                    os.system("limit.py --max-likelihood --collect-injected-toys {DIR}/{MASS}".format(DIR=dir, MASS=mass))
            ## finally obtain the result on data 
            lxb_submit(struct[0], struct[1], "--max-likelihood", "{USER}".format(USER=options.opt))
        else :
            lxb_submit(struct[0], struct[1], "{METHOD} --collect-injected-toys".format(METHOD=options.injected_method), "{USER}".format(USER=options.opt))
##
## CLs
##
if options.optCLs :
    cycle = options.cycles
    while cycle>0 :
        print "***********************************************************"
        print " %s cycle(s) to finish" % cycle
        print "***********************************************************"
        cmd = "submit-slave.py --bin combine --method CLs"
        sub = "--toysH 50 -t 500 -j 500 --random"
        if not options.skipserver :
            sub+= " --server"
        if options.priority :
            sub+= " --priority"
        if options.lxbsubmit :
            sub+= " --lsf"
        if len(subvec(args, 90, 150))>0 :
            dirs = vec2str(subvec(args, 90, 150))
            if options.printOnly :
                print "{CMD} -n 5 --min   0.3  --max   1.5 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                print "{CMD} -n 5 --min   2.0  --max   4.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
            else :
                os.system("{CMD} -n 5 --min   0.3  --max   1.5 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs))
                os.system("{CMD} -n 5 --min   2.0  --max   4.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs))
        cycle = cycle-1
##
## BAYES
##
if options.optBayes :
    cycle = options.cycles
    while cycle>0 :
        print "***********************************************************"
        print " %s cycle(s) to finish" % cycle
        print "***********************************************************"
        if len(subvec(args, 90, 150))>0 :
            cmd = "submit-slave.py --bin combine --method Bayesian"
            sub = "-t 1000 -j 100 --server --random --priority"
            if options.printOnly :
                print "{CMD} {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=vec2str(subvec(args, 90, 150)))
            else :
                os.system("{CMD} {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=vec2str(subvec(args, 90, 150))))
        cycle = cycle-1
##
## TANB
##
if options.optTanb or options.optTanbPlus :
    cycle = options.cycles
    while cycle>0 :
        if options.optTanb :
            print "***********************************************************"
            print " %s cycle(s) to finish" % cycle
            print "***********************************************************"
        cmd = ""
        if options.optTanb :
            cycle = 1
            cmd = "submit-slave.py --bin combine --method tanb"
        elif options.optTanbPlus :
            if options.setup :
                cmd = "submit-slave.py --bin combine --method tanb {OLD}".format(OLD="--old" if options.old else "")
        if not cmd == "" :
            grid= []
            sub = "--interactive" if options.optTanbPlus else "--toysH 100 -t 200 -j 100 --random --server --priority"
            if len(subvec(args,  90, 249))>0 :
                dirs = vec2str(subvec(args,  90,  249))
                grid = [
                     "{CMD} -n  6 --min  0.5  --max  1.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  4 --min  2.0  --max  8.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs) 
                    ,"{CMD} -n  3 --min  9.0  --max 15.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 20.0  --max 30.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    #,"{CMD} -n  2 --min 35.0  --max 40.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    #,"{CMD} -n  3 --min 50.0  --max 70.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                ]
            if len(subvec(args, 250, 299))>0 :
                dirs = vec2str(subvec(args, 250,  299))
                grid = [
                     "{CMD} -n  2 --min  0.5  --max  1.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min  3.0  --max 15.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 20.0  --max 40.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    #,"{CMD} -n  3 --min 50.0  --max 70.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                ]                
            if len(subvec(args, 300, 399))>0 :
                dirs = vec2str(subvec(args, 300,  399))
                grid = [
                     "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 13.0  --max 25.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 30.0  --max 40.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 50.0  --max 70.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                ]                                
            if len(subvec(args, 400, 599))>0 :
                dirs = vec2str(subvec(args, 400,  599))
                grid = [
                     "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  2 --min 15.0  --max 20.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 25.0  --max 45.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 50.0  --max 70.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                ]                                
            if len(subvec(args, 600, 1000))>0 :
                dirs = vec2str(subvec(args, 600, 1000))
                grid = [
                     "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  2 --min 15.0  --max 20.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 30.0  --max 50.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                    ,"{CMD} -n  4 --min 55.0  --max 70.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=options.opt, USER=options.opt, DIRS=dirs)
                ]                                                
            for point in grid :
                if options.printOnly :
                    print point
                else :
                    os.system(point)
        else :
            if options.interactive :
                for dir in args :
                    mass = get_mass(dir)
                    if mass == 'common' :
                        continue
                    if options.printOnly :
                        print "limit.py --tanb+ {OPTS} {DIR} {OLD}".format(OPTS=options.opt, DIR=dir, OLD="--old" if options.old else "")
                    else :
                        os.system("limit.py --tanb+ {OPTS} {DIR} {OLD}".format(OPTS=options.opt, DIR=dir, OLD="--old" if options.old else ""))
            else :
                dirs = []
                for dir in args :
                    ## chop off masses directory if present as this will be added automatically by the submission script
                    if is_number(get_mass(dir)) or get_mass(dir) == "common" :
                        dir = dir[:dir.rstrip('/').rfind('/')]
                    if not dir in dirs :
                        dirs.append(dir)
                ## directories and mases per directory
                struct = directories(args)
                lxb_submit(struct[0], struct[1], "--tanb+", options.opt)
        cycle = cycle-1


