#!/usr/bin/env python
# flake8: noqa

import glob
import hashlib
import os
import re
from optparse import OptionParser, OptionGroup
from HiggsAnalysis.HiggsToTauTau.parallelize import parallelize
from HiggsAnalysis.HiggsToTauTau.CardCombiner import create_workspace, extract_pull_options
import sys

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="This is a script do to final calculations or harvesting of batch or grid jobs that have been submitted via crab, and everything that is connected to this. You can check the status of the submitted jobs, get the output of your jobs, or further process this output for the calculation of Bayesian or CLs limits, toy based significance calculations, likelihood scans or maximum-likelihood fits. What exactly you want the script to do is passed on with a large set of command line options, which are explained below. Apart from these comman line options the script expects the arguments ARG1, ARG2, ARG3, ..., which correspond to the working directories the corresponding operation should be applied to. The script expects that these directories follow a stucture, that ends with a directory corresponding to the mass, on which the operation is to be applied. The name of this directory should correspond to an interger or floating point number. It should contain all datacards and necessary information to execute the operations on.\n")
##
## MAIN OPTIONS
##
agroup = OptionGroup(parser, "MAIN OPTIONS", "These are the command line options for the common use of limits.py. These options can be considered as the main switches of limit.py. They comprise several options to determine fits to the signal strength, multi-dimensional fits in 2d-planes, for user defined models, asymptotic limits, toy based significance calculations and toy based limit calculations like bayesian and full CLs limits. All toy based calculations have to be prepared and submitted to some batch system or to the grid. Use the script submit.py with corresponding command line options as descripbed for each individual calculation method, to which this applies below. All command line options in this section are exclusive.")
agroup.add_option("--max-likelihood", dest="optMLFit", default=False, action="store_true",
                  help="Perform a maximum likelihood fit from the datacards in the directory/ies. corresponding to ARGs The results of this fit are used for htt postfit plots. [Default: False]")
agroup.add_option("--likelihood-scan", dest="optNLLScan", default=False, action="store_true",
                  help="Perform a maximum likelihood scan to determine the signal strength from the datacards in the directory/ies corresponding to ARGs. [Default: False]")
agroup.add_option("--multidim-fit", dest="optMDFit", default=False, action="store_true",
                  help="Perform a maximum likelihood fit in two dimensions to determine the signal strength from the datacards in the directory/ies corresponding to ARGs. This option requires the configuration of several sub-option that can be found in section MULTIDIM-FIT OPTIONS of this parameter description. [Default: False]")
agroup.add_option("--significance", dest="optSig", default=False, action="store_true",
                  help="Calculate the observed and expected significance from likelihood profiling. The expected significance and its uncertainties are based on toys. This requires that the toys have been run beforehand using the script submit.py with option --significance. This script will submit toys to a batch system or to the grid using crab. This action will require a grid certificate. You can monitor and receive the results of your jobs once finished using the command options explained in section COMMON CRAB COMMAND OPTIONS of this parameter description. [Default: False]")
agroup.add_option("--asymptotic", dest="optAsym", default=False, action="store_true",
                  help="Calculate asymptotic CLs limits from the datacards in the directory/ise corresponding to ARGs. [Default: False]")
agroup.add_option("--CLs", dest="optCLs", default=False, action="store_true",
                  help="Calculate the observed and expected full CLs limits. This method is completely toy based. It requires that the toys have been run beforehand using the script submit.py with option --CLs. This script will submit toys to a batch system or to the grid using crab. This action will require a grid certificate. You can monitor and receive the results of your jobs once finished using the command options explained in section COMMON CRAB COMMAND OPTIONS of this parameter description.[Default: False]")
agroup.add_option("--bayesian", dest="optBayes", default=False, action="store_true",
                  help="Calculate the observed and expected bayesian limits. This method is completely toy based. It requires that the toys have been run beforehand using the script submit.py with option --bayesian. This script will submit toys to a batch system or to the grid using crab. This action will require a grid certificate. You can monitor and receive the results of your jobs once finished using the command options explained in section COMMON CRAB COMMAND OPTIONS of this parameter description. [Default: False]")
agroup.add_option("--tanb", dest="optTanb", default=False, action="store_true",
                  help="Calculate the observed and expected limits directly in the MSSM mA-tanb plane based on full CLs limits. This method is completely toy based. It requires that the toys have been run beforehand using the script submit.py with option --tanb. This script will submit toys to a batch system or to the grid via crab. This action will require a grid certificate. You can monitor and receive the results of your jobs once finished using the command options explained in section COMMON CRAB COMMAND OPTIONS of this parameter description. [Default: False]")
agroup.add_option("--tanb+", dest="optTanbPlus", default=False, action="store_true",
                  help="Calculate the observed and expected limits directly in the MSSM mA-tanb plane based on asymptotic CLs limits. This method requires that the directory structure to calculate these limits has been set up beforehand using the script submit.py with option --tanb+. [Default: False]")
parser.add_option_group(agroup)
##
## COMMON OPTIONS
##
bgroup = OptionGroup(parser, "COMMON OPTIONS", "These are the command line options for the common use of limits.py. These options are not specific to one or the other main comman line option. They can be used together with several other command line options. If there are restrictions they will be given in the explanation of each corresponding command line option below.")
bgroup.add_option("--name", dest="name", default="Test", type="string",
                  help="Specify a name-label that will be added to the output file of your fit, limit or significance calculation. [Default: \"Test\"]")
bgroup.add_option("--no-repeat", dest="norepeat", default=False, action="store_true",
                  help="Detect if a command has already been run, and do not execute the command again if this is the case. [Default: False]")
bgroup.add_option("--shape", dest="shape", default="shape2", type="string",
                  help="Choose a dedicated algorithm for vertical shape morphing during roofit model creation. [Default: 'shape2']")
bgroup.add_option('--external-pulls', dest='externalPulls', default=None, type="string",
                  help="Optionally constrain nuisance parameters using the result of a ML fit result (e.g. mlfit.root) that has been created beforehand. [Defasult: None]")
bgroup.add_option("--confidence-level", dest="confidenceLevel", default="0.95", type="string",
                  help="Choose the confidence level at which to calculate the limit. This option only applies to asymptotic limit calculations. It does not apply to toy based methods, which have to be configured accordingly in the submission step (using the script submit.py). [Default: '0.95']")
bgroup.add_option("--rMin", dest="rMin", default="-5", type="string",
                  help="Set the minimum value of signal strenth used for fits and prior to the limit or significance calculation. [Default: -5]")
bgroup.add_option("--rMax", dest="rMax", default= "5", type="string",
                  help="Set the maximum value of signal strenth used for fits and prior to the limit or significance calculation. [Default: -5]")
bgroup.add_option("--expectedOnly", dest="expectedOnly", default=False, action="store_true",
                  help="Calculate the expected limit only. This option applies to limit and significance calculations only. [Default: False]")
bgroup.add_option("--observedOnly", dest="observedOnly", default=False, action="store_true",
                  help="Calculate the observed limit only. This option applies to limit and significance calculations only. [Default: False]")
bgroup.add_option("--userOpt", dest="userOpt", default="", type="string",
                  help="With this option you can specify any kind of user option that is not covered by limit.py and that you would like to be passed on to the combine tool. [Defaul: \"\"]")
bgroup.add_option("--working-dir", dest="workingdir", default=".",
                  help="Optionally specify where the temporary combined datacard tmp.txt should be produced. [Default '.']")
parser.add_option_group(bgroup)
##
## CRAB OPTIONS 
##
cgroup = OptionGroup(parser, "CRAB OPTIONS", "These are command line options for the common use of crab within limits.py. You need the following requirements to be able to execute limits.py with these options: have set up the glite environment; have set up the crab environment; have a valid grid certificate. These options apply to all toy based calculations that have been submitted to the grid. you can use them to monitor the jobs of each crab job that has been submittred from the directoriy/ies corresponding to ARGs and to receive their output once finished.")
cgroup.add_option("--status", dest="status", default=False, action="store_true",
                  help="Check the status of all crab jobs that have been submitted in the directory/ies corresponding to ARGs. [Default: False]")
cgroup.add_option("--getoutput", dest="getoutput", default=False, action="store_true",
                  help="Get the output of all crab jobs that have been submitted in the directory/ies corresponding to ARGs. [Default: False]")
cgroup.add_option("--kill", dest="kill", default=False, action="store_true",
                  help="Kill all crab jobs that have been submitted from the directory/ies corresponding to ARGs. [Default: False]")
cgroup.add_option("--cleanup", dest="cleanup", default=False, action="store_true",
                  help="Remove all crab remainders of previous submissions from the directory/ies corresponding to ARGs. [Default: False]")
parser.add_option_group(cgroup)
##
## MODEL OPTIONS
##
dgroup = OptionGroup(parser, "MODEL OPTIONS", "These are the command line options for the use of limit.py with special physics models. Dedicated physics models can be used with option --multidim-fit, with option --likelihood-scan or with option --asymptotic.")
dgroup.add_option("--physics-model", dest="fitModel", type="string", default="",
                  help="Specify the physics model that you want to be used for the construction of the multi-dimensional maximum likelihood function. The physics model should be defined by a model name and a path to a python implementation of the model separated by '='. For example 'MODEL-NAME=PATH-TO-IMPLEMENTATION'. In this case a roofit workspace of the model with given model options will be created with the name 'MODEL-NAME.root'. It is also possible to pass only a name of a physics model, like 'MODEL-NAME'. In this case it will be assumed that the model with name 'MODEL-NAME' has been created beforehand. If not found an exception is thrown. [Default: \"\"]")
dgroup.add_option("--physics-model-options", dest="fitModelOptions", type="string", default="",
                  help="Specify potential options for the used physics model for the creation of the multi-dimensional maximum likelihood function. More than one option can be passed on. The options should then be separated by ';'. [Default: \"\"]")
dgroup.add_option("--restrict-categories", dest="fitModelCategories", type="string", default="",
                  help="Add a string to restrict the fit only to a subset of event categories. The string should contain the indexes of the allowed event categories. These indexes should be separated by ':', for example: '0:1:2:3'. If the string is empty the datacards from all event categories will be taken into account in the likelihood evaluation, that are located in the target directory. [Default: \"\"]")
parser.add_option_group(dgroup)
##
## MAX LIKELIHOOD OPTIONS
##
fgroup = OptionGroup(parser, "MAX-LIKELIHOOD OPTIONS", "these are the command line options for the use of limit.py with the option --max-likelihood. Running limit.py --max-likelihood ARGs will result in an extra directory 'out' in the directory/ies corresponding to ARGs, that contains the output of the fit in roofit, html, txt and tex format. The signal strength for the background and signal plus background model and the pulls of all nuisance parameters are available in html, txt and tex format. This fit does not separate between individual components of the signal like ggH or qqH. The outputs are used for the postfit plotting in the HiggsTotauTau package.")
fgroup.add_option("--stable", dest="stable", default=False, action="store_true",
                  help="Run maximum likelihood fit with a pre-defined set of options that lead to more stable results. This option requires further input via the common options --rMin and --rMax to define the boundaries of the fit. [Default: False]")
fgroup.add_option("--minuit", dest="minuit", default=False, action="store_true",
                  help="Switch from minuit2 to minuit for the fit that is performed before the asymptotic limits are calculated. [Default: False]")
fgroup.add_option("--qtilde", dest="qtilde", default=False, action="store_true",
                  help="Also allow negative signal strength in the fit that is performed before the asymptotic limits are calculated. [Default: False]")
fgroup.add_option("--strategy", dest="strategy", default=2, type="int",
                  help="Change the strategy of the fit that is performed before the asymptotic limits are calculated. Possible strategies are 0, 1, 2. [Default: 2]")
parser.add_option_group(fgroup)
##
## LIKELIHOOD-SCAN OPTIONS
##
ggroup = OptionGroup(parser, "LIKELIHOOD-SCAN OPTIONS", "These are the command line options for the use of limit.py with the option --likelihood-scan. Running limit.py --likelihood-scan ARGs will result in a scan of the likelihood function with the SM and only Higgs signal strength combined for all production channels as single POI. Internally this scan uses the option multidim-fit reduced to one dimension. For the likelihood scan you have to specify the number of points (option --points) and the range in which to perform the scan (options --rMin and --rMax), as explained in section MULTIDIM-FIT OPTIONS and in section COMMON OPTIONS in this parameter description.")
parser.add_option_group(ggroup)
##
## MULTIDIM-FIT OPTIONS
##
hgroup = OptionGroup(parser, "MULTIDIM-FIT OPTIONS", "These are the command line options for the use of limit.py with the option --multidim-fit. Running limit.py --multidim-fit ARGs will result in a two dimensional fit corresponding to a user defined fit model and based on the datacards in the directory/ies corresponding to ARGs. Each multi-dimensional fit requires the specification of a predefined physics model (option --physics-model) and eventually of a set of physics model options (option --physics-model-options). The fit can be performed using several algorithms (single, contour2d, grid). The option --algo=grid will initiate a scan of the likelihood function. This options requires to specify the number of points for the scan (option --points), the definition of the boundaries that must be implemented options of the model that has been specified and eventually the a first and a last point that should be evaluated in the current scan (options --firstPoint and --lastPoint). It is advisable to perform grid scans via a batch system using the submit.py script with option --multidim-fit and corresponding sub-options to perform predefined likelihood scans. The output of the fit can be safed in a dedicated file called multi-dim.fitresult, which can be subsequently used for plotting.")
hgroup.add_option("--algo", dest="fitAlgo", type="string", default="",
                  help="Specify the algorithm to be used for the multi-dimensional maximum likelihood fit (options are singles, contour2d, grid). Option grid will require further input via the options --points and eventually --firstPoint and --lastPoint. [Default: \"\"]")
hgroup.add_option("--fastScan", dest="fastScan", action="store_true", default=False,
                  help="When doing a likelihood scan (with option --algo=grid), usually at each point in the grid the nuisance parameters are re-evaluated. This can be very time consuming especially if the combined model has many nuisance parameters. With the option fastScan the nuiscance parameters will be fixed to the best fit value. You can use this option to speed up the maximum likelihood scan. [Default: \"False\"]")
hgroup.add_option("--points", dest="gridPoints", type="string", default="100",
                  help="Number of grid points for the grid scan of the likelihood function in case of option --algo=grid. [Default: \"100\"]")
hgroup.add_option("--firstPoint", dest="firstPoint", type="string", default="",
                  help="Potential options for splitting the grid points in different jobs. Only to be used with tools that split the maximum likelihood scan in several batch jobs. [Default: \"\"]")
hgroup.add_option("--lastPoint", dest="lastPoint", type="string", default="",
                  help="Potential options for splitting the grid points in different jobs. Only to be used with tools that split the maximum likelihood scan in several batch jobs. [Default: \"\"]")
hgroup.add_option("--setupOnly", dest="setupOnly", action="store_true", default=False,
                  help="Only setup the model, do not start the minimization. To be used with job splitting for maximum likelihood scans. If \"False\" the model will be set up and the minimzation will be executed right away. [Default: \"False\"]")
hgroup.add_option("--saveResults", dest="saveResults", action="store_true", default=False,
                  help="Store the fit output that is usually prompted to the screen in a txt file called multi-dim.fitresult. This input file can be used further on to plot the signal strength as function of mH or as function of mA. [Default: \"False\"]")
hgroup.add_option("--collect", dest="collect", action="store_true", default=False,
                  help="Use this option to re-collect the output in the directory/ies corresponding to ARGs in case you have run the multimensional fit using the script submit.py with option --multidim-fit. Note that you have to specify a physics model, when using limit.py with option --multidim-fit. It is enought to give the name of the physics model in this case. The name of the output file will be modified according to the capitalized name of the physcis model to indicate clearly what model has been fit to the data. [Default: \"False\"]")
parser.add_option_group(hgroup)
##
## SIGNIFICANCE OPTIONS
##
igroup = OptionGroup(parser, "SIGNIFICANCE OPTIONS", "these are the command line options for the use of limit.py with the option --significance. Running limit.py --significance ARGs will result in a calculation of the observed and expected significance based on the datacards in the directory/ies corresponding to ARGs. As the median and quantiles of the expected significance are obtained from toys it is recommended to run the expected significance via batch jobs using the script submit.py with option --significance. You can specify the strength of the signal in multiples of the expected SM cross section as iven in the datacards and the number of toys to be run for the expected significance.")
igroup.add_option("--signal-strength", dest="signal_strength", default="1", type="string",
                  help="Set the signal strength for the calculation the expected significance. [Default: \"1\"]")
igroup.add_option("--toys", dest="toys", default="100", type="string",
                  help="Set number of toys of the median and quantiles for expected significance calculation. [Default: \"100\"]")
parser.add_option_group(igroup)
##
## ASYMPTOTIC OPTIONS 
##
egroup = OptionGroup(parser, "ASYMPTOTIC OPTIONS", "These are the command line options for the use of limit.py with the option --asymptotic. Running limit.py --asymptotic ARGs will result in observed and expected asymptotic CLs limits based on the datacards in the directory/ies corresponding to ARGs. Asymptotic limits can be run directly on the specified target directories without any further processing. It is expected that the target directories follow a directory structure as described on the top of this parameter description. Prior to the limit calculation a maximum likelihood fit is performed to the data with a background only model and with a signal plus background model. The parameters of this fit can be changed according to the options described in section MAX-LIKELIHOOD OPTIONS of this parameter description. The pre-fit to the data can also be suppressed. When calculating expected limits in data blinded mode use the options --no-prefit and --expectedOnly.")
egroup.add_option("--no-prefit", dest="noprefit", default=False, action="store_true",
                  help="Skip the fit that is usually performed before the asymptotic limits are calculated. Use this option together with option --expectedOnly to calculated expected limits for data blinding. [Default: False]")
parser.add_option_group(egroup)
##
## CLS COMMAND OPTIONS
##
jgroup = OptionGroup(parser, "CLS OPTIONS", "These are the command line options for the use of limit.py with the option --CLs. Running limit.py --CLs ARGs will result in an expected and observed full CLs limit based on the datacards in the directory/ies corresponding to ARGs. As this is a fully toy based calculation it is required that you have run the full CLs toys on a batch system or via the grid using the script submit.py with option --CLs. The limit.py script can be used to monitor the jobs and to retrieve their output using the options explained in section CRAB OPTIONS of this parameter description. Using limit.py --CLs requires that you have retrieved the outputs of your jobs beforehand using the option limit.py --getoutput AGRs. The script will then complete harvesting of the output and perform the final calculation of the limits. There is no further options that need to be applied. In case you want to change the conficence level of the limit calculation you must have specified this during batch job submission for the calculation of the individual toys.")
parser.add_option_group(jgroup)
##
## BAYESIAN COMMAND LINE OPTIONS
##
kgroup = OptionGroup(parser, "BAYESIAN OPTIONS", "These are the command line options for the use of limit.py with the option --bayesian. Running limit.py --bayesian ARGs will result in an expected and observed bayesian limit based on the datacards in the directory/ies corresponding to ARGs. As the expected limit calculation is based on a toy based integration of the likelihood function (using the Markov Chain MC approach) it is required that you have run the expected limits on a batch system or via the grid using the script submit.py with option --bayesian. As it can be time consuming for complex models also the calculation of the observed limit can be performed via a batch job or via the grid. The limit.py can be used to monitor the jobs and to retrieve their output using the options explained in section CRAB OPTIONS of this parameter description. Using limit.py --bayesian requires that you have retrieved the outputs of your jobs beforehand using the option limit.py --getoutput AGRs. The script will then complete harvesting of the output and perform the final calculation of the limits. In case the observed limits have been calculated in batch mode the script will recognize this. Otherwise the observed limits will be calculated on the fly. For this calculation there is still a bunch of parameters that canbe specified as explained below.")
kgroup.add_option("--hint", dest="hint", default="Asymptotic", type="string",
                  help="Specify the name of the hint method that should be used to guide the Markov Chain MC. [Default: Asymptotic]")
kgroup.add_option("--iterations", dest="iter", default=10000, type="int",
                  help="Specify the number of iterations to integrate out the nuisance parameters. [Default: 10000]")
kgroup.add_option("--tries", dest="tries", default=10, type="int",
                  help="Specify the number of tries to run the Markov Chain MC on the same data. [Default: 10]")
parser.add_option_group(kgroup)
##
## TANB OPTIONS
##
lgroup = OptionGroup(parser, "TANB OPTIONS", "These are the command line options for the use of limits.py with option --tanb. Running limit.py --tanb ARGs will result in the expected and observed direct exclusion contour in the mA-tanb plane based on the full CLs limit calculation method. This calculation requires a special setup of the datacards in each tanb point for fixed mA. In addition, as this is this is a fully toy based calculation it requires that you have run the full CLs toys for each tanb point for given mA on a batch system or via the grid using the script submit.py with option --tanb. The limit.py script can be used to monitor the jobs and to retrieve their output using the options explained in section CRAB OPTIONS of this parameter description. Using limit.py --tanb requires that you have retrieved the outputs of your jobs beforehand using the option limit.py --getoutput AGRs. The script will then complete harvesting of the output and perform the final calculation of the limits. There is no further options that need to be applied. In case you want to change the conficence level of the limit calculation you must have specified this during batch job submission for the calculation of the individual toys.")
parser.add_option_group(lgroup)
##
## TANB+ COMMAND LINE OPTIONS
##
mgroup = OptionGroup(parser, "TANB+ COMMAND OPTIONS", "These are the command line options for the use of limits.py with option --tanb+. Running limit.py --tanb+ ARGs will result in the expected and observed direct exclusion contour in the mA-tanb plane based on the asymptotic CLs limit calculation method. This calculation requires a special setup of the datacards in each tanb point for fixed mA. You can set up this structure using the script submit.py with option --tanb+. The script will do the calculation in each point of tanb for fixed mA and determin the limit in tanb from the crossing point of the derived limit/tanb with 1, using a linear interpolation between the calculated points. The calculation of the limits can be performed on more than one core in parallel (option --multi-core). If the individual limits for each point in tanb for fixed mA have been calculated the final procedure to determine the crossing point with 1 can be rerun standalone (option --refit).")
mgroup.add_option("--multi-core", dest="tanbMultiCore", type="int", default=-1, help="Run combine calls in parallel on several cores when running in more tanb+ (supply nTasks) when scanning in tanBeta")
mgroup.add_option("--refit", dest="refit", default=False, action="store_true", help="Do not run the asymptotic limits again, but only run the last step, the fit for the limit determination. (Only valid for option --tanb+, for all other options will have no effect.)  [Default: False]")
parser.add_option_group(mgroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

## base directory introduced to allow use of absolute file paths
base_directory = os.getcwd()

def get_hash_for_this_call():
    '''
    Create a unique hash corresponding to this call to limit.py
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
    '''
    Determine if the limit.py tool has already been run for this directory
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

def get_mass(directory) :
    '''
    Returns the mass from a directory string. directories are expected to end with a floating
    point number of with an integer number. Trailing slashes are removed. The mass is returned
    as a string.
    '''
    ## determine mass value from directory name
    idx = directory.rfind("/")
    if idx == (len(directory) - 1):
        idx = directory[:idx - 1].rfind("/")
    mass  = directory[idx + 1:]
    return mass.rstrip('/')
    
def create_card_workspace(mass, card_glob='*.txt', output='tmp.root', extra_options=None) :
    '''
    Create a tmp.root combining data cards in the CWD
    '''
    ws_options = [
        ('-m', mass),
        ('--default-morphing', options.shape),
    ]
    if extra_options:
        ws_options.extend(extra_options)
    output = os.path.join(options.workingdir, output)

    if options.externalPulls:
        ## constrain the nuisances using an external ML fit
        with open(
            os.path.join(base_directory, options.externalPulls), 'r') as pullfile:
            ws_options.extend(
                extract_pull_options(pullfile)
            )
    return create_workspace(output, card_glob, ws_options)

def create_card_workspace_with_physics_model(mass) :
    '''
    Create a tmp.root combining data cards in the CWD with a physics model
    '''
    output = ""
    inputs = []
    wsopts = []
    model  = options.fitModel.split('=')
    ## prepare output name
    output = "%s.root" % model[0]
    ## collect cards that should be combined
    for card in os.listdir(".") :
        if not '.txt' in card :
            continue
        if options.fitModelCategories == "" :
            inputs.append(card)
        else :
            allowed_categories = options.fitModelCategories.split(':')
            for allowed in allowed_categories :
                if allowed in card :
                    inputs.append(card)
    ## prepare options for physics model and options
    wsopts.append(('-P', model[1]))
    if not options.fitModelOptions == "" :
        ## break physics model options to list
        if ';' in options.fitModelOptions :
            opts = options.fitModelOptions.split(';')
        else :
            opts = options.fitModelOptions.split(' ')
        for idx in range(len(opts)) : opts[idx] = opts[idx].rstrip(',')
        for opt in opts :
            wsopts.append(('--PO', opt))                                
    return create_card_workspace(mass, inputs, output, wsopts)

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
    os.chdir(subdirectory)
    ##
    ## STATUS
    ##
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
    ##
    ## GETOUTPUT
    ##
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
            os.chdir(subdirectory)
    ##
    ## KILL
    ##
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
    ##
    ## CLEANUP
    ##
    if options.cleanup :
        os.system("rm -r crab*")
        if os.path.exists("observed") :
            os.chdir(os.path.join(subdirectiry, "observed"))
            os.system("rm -r crab*")
            os.chdir(subdirectory)
    ##
    ## MAX-LIKELIHOOD
    ##
    if options.optMLFit :
        ## determine mass value from directory name
        mass  = get_mass(directory)
        ## prepare workspace
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
        ## run maximum likelihood fit
        print "combine -M MaxLikelihoodFit -m {mass} {minuit} {stable} {user} {wdir}/tmp.root --out=out".format(
            mass=mass, minuit=minuitopt, stable=stableopt, user=options.userOpt, wdir=options.workingdir)
        os.system("combine -M MaxLikelihoodFit -m {mass} {minuit} {stable} {user} {wdir}/tmp.root --out=out".format(
            mass=mass, minuit=minuitopt, stable=stableopt, user=options.userOpt, wdir=options.workingdir))
        ## change to sub-directory out and prepare formated output
        os.chdir(os.path.join(subdirectory, "out"))
        print "formating output..."
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A -a -f text mlfit.root > mlfit.txt")
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A -a -f latex mlfit.root > mlfit.tex")
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A -a -f html mlfit.root > mlfit.html")
        ## add a version with only problematic values
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A  -f text mlfit.root > mlfit_largest-pulls.txt")
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A  -f latex mlfit.root > mlfit_largest-pulls.tex")
        os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -A  -f html mlfit.root > mlfit_largest-pulls.html")
        os.chdir(subdirectory)
    ##
    ## LIKELIHOOD-SCAN
    ##
    if options.optNLLScan :
        ## determine mass value from directory name
        mass  = get_mass(directory)
        ## prepare workspace
        model = []
        if "=" in options.fitModel :
            model = options.fitModel.split('=')
            create_card_workspace_with_physics_model(mass)
        elif options.fitModel == "" :
            create_card_workspace(mass)
        else :
            model = [options.fitModel]
        ## ------------------------------------------------------------------------------------------------------------
        ## OLD STYLE
        ### combine datacard from all datacards in this directory if not done so already
        #if "=" in options.fitModel :
        #    ## collect all cards that should be combined into the model. If used with a dedicated fit model
        #    ## like in the MSSM case, only cards that can be identified to belong to an available decay
        #    ## channel can be combined. this is only a practical limitation for now.
        #    inputcards = ""
        #    for card in os.listdir(".") :
        #        if "htt_" in card :
        #            if options.fitModelCategories == "" :
        #                inputcards+=card[:card.find('.')]+'='+card+' '
        #            else :
        #                allowed_categories = options.fitModelCategories.split(':')
        #                for allowed in allowed_categories :
        #                    if allowed in card :
        #                        inputcards+=card[:card.find('.')]+'='+card+' '
        #    print "combineCards.py -S %s > %s/tmp.txt" % (inputcards, options.workingdir)
        #    os.system("combineCards.py -S %s > %s/tmp.txt" % (inputcards, options.workingdir))
        #else:
        #    ## here all kind of datacards are allowed
        #    if not os.path.exists("%s/tmp.txt" % options.workingdir) :
        #        print "combineCards.py -S *.txt > %s/tmp.txt" % options.workingdir
        #        os.system("combineCards.py -S *.txt > %s/tmp.txt" % options.workingdir) 
        ### set up the physics model
        #model = []
        #if "=" in options.fitModel :
        #    model = options.fitModel.split('=')
        #    ## combine datacard from all datacards in this directory. For the multi-dimensional fit
        #    ## it is of importance that the decay channels and run periods are well defined from the
        #    ## channel names. Allow for a restriction of the event categories
        #    if os.path.exists("%s/%s.root" % (options.workingdir, model[0])) :
        #        os.system("rm %s/%s.root" % (options.workingdir, model[0]))
        #    ## create workspace with dedicated physics model
        #    workspaceOptions = "-m %s " % mass
        #    workspaceOptions+= "-o %s/%s.root " % (options.workingdir, model[0])
        #    workspaceOptions+= "-P %s " % model[1]
        #    if not options.fitModelOptions == "" :
        #        ## break physics model options to list
        #        opts = options.fitModelOptions.split(';')
        #        for idx in range(len(opts)) : opts[idx] = opts[idx].rstrip(',')
        #        for opt in opts :
        #            workspaceOptions+="--PO %s " % opt
        #    print "text2workspace.py %s/tmp.txt %s" % (options.workingdir, workspaceOptions)
        #    os.system("text2workspace.py %s/tmp.txt %s" % (options.workingdir, workspaceOptions))
        #else :
        #    ## prepare binary workspace
        #    print "text2workspace.py --default-morphing=%s -m %s -b %s/tmp.txt -o %s/tmp.root"% (options.shape, mass, options.workingdir, options.workingdir)
        #    os.system("text2workspace.py --default-morphing=%s -m %s -b %s/tmp.txt -o %s/tmp.root"% (options.shape, mass, options.workingdir, options.workingdir))
        ## OLD STYLE
        ## ------------------------------------------------------------------------------------------------------------
        ## if it does not exist already, create link to executable
        if not os.path.exists("combine") :
            os.system("cp -s $(which combine) .")
        ## do the likelihhod scan
        wsp = 'tmp' if len(model) == 0 else model[0]
        print "combine -M MultiDimFit -m {mass} --algo=grid --points={points} --rMin {min} --rMax {max} {user} {wdir}/{wsp}.root".format(
            mass=mass, points=options.gridPoints, user=options.userOpt, min=options.rMin, max=options.rMax, wdir=options.workingdir, wsp=wsp)
        os.system("combine -M MultiDimFit -m {mass} --algo=grid --points={points} --rMin {min} --rMax {max} {user} {wdir}/{wsp}.root".format(
            mass=mass, points=options.gridPoints, user=options.userOpt, min=options.rMin, max=options.rMax, wdir=options.workingdir, wsp=wsp))
    ##
    ## MULTIDIM-FIT
    ##
    if options.optMDFit :
        ## determine mass value from directory name
        mass  = get_mass(directory)
        ## prepare workspace
        model = []
        if "=" in options.fitModel :
            model = options.fitModel.split('=')
            create_card_workspace_with_physics_model(mass)
        elif options.fitModel == "" :
            print "You must configrue a physics model to run this option"
            exit(1)
        else :
            model = [options.fitModel]
        ## ------------------------------------------------------------------------------------------------------------
        ## OLD STYLE    
        ## set up the physics model
        #model = []
        #if "=" in options.fitModel :
        #    model = options.fitModel.split('=')
        #    ## combine datacard from all datacards in this directory. For the multi-dimensional fit
        #    ## it is of importance that the decay channels and run periods are well defined from the
        #    ## channel names. Allow for a restriction of the event categories
        #    if os.path.exists("%s/tmp.txt" % options.workingdir) :
        #        os.system("rm %s/tmp.txt" % options.workingdir)
        #        inputcards = ""
        #    if os.path.exists("%s/%s.root" % (options.workingdir, model[0])) :
        #        os.system("rm %s/%s.root" % (options.workingdir, model[0]))
        #    ## collect all cards that should be combined into the model
        #    inputcards = ""
        #    for card in os.listdir(".") :
        #        if "htt_" in card :
        #            if options.fitModelCategories == "" :
        #                inputcards+=card[:card.find('.')]+'='+card+' '
        #            else :
        #                allowed_categories = options.fitModelCategories.split(':')
        #                for allowed in allowed_categories :
        #                    if allowed in card :
        #                        inputcards+=card[:card.find('.')]+'='+card+' '
        #    print "combineCards.py -S %s > %s/tmp.txt" % (inputcards, options.workingdir)
        #    os.system("combineCards.py -S %s > %s/tmp.txt" % (inputcards, options.workingdir))
        #    ## create workspace with dedicated physics model
        #    workspaceOptions = "-m %s " % mass
        #    workspaceOptions+= "-o %s/%s.root " % (options.workingdir, model[0])
        #    workspaceOptions+= "-P %s " % model[1]
        #    if not options.fitModelOptions == "" :
        #        ## break physics model options to list
        #        opts = options.fitModelOptions.split(';')
        #        for idx in range(len(opts)) : opts[idx] = opts[idx].rstrip(',')
        #        for opt in opts :
        #            workspaceOptions+="--PO %s " % opt
        #    print "text2workspace.py %s/tmp.txt %s" % (options.workingdir, workspaceOptions)
        #    os.system("text2workspace.py %s/tmp.txt %s" % (options.workingdir, workspaceOptions))
        #else :
        #    model = [options.fitModel]
        ## OLD STYLE
        ## ------------------------------------------------------------------------------------------------------------
        if options.collect :
            ## combine outputs
            print mass
            os.system("hadd -f higgsCombine{MODEL}.MultiDimFit.mH{MASS}.root higgsCombine*.MultiDimFit.mH{MASS}-[0-9]*-[0-9]*.root".format(
                MASS=mass, MODEL=model[0].upper()))
            ## cleanup
            os.system("rm higgsCombine*.MultiDimFit.mH{MASS}-[0-9]*-[0-9]*.root".format(MASS=mass))
            continue
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
            ## set up grid points and grid options in case of likelihood scan (option --grid)
            gridpoints = ""
            if options.fitAlgo == "grid" :
                if options.firstPoint == "" :
                    gridpoints = "--points %s --firstPoint 1 --lastPoint %s" % (options.gridPoints, options.gridPoints)
                else :
                    gridpoints = "--points %s --firstPoint %s --lastPoint %s" % (options.gridPoints, options.firstPoint, options.lastPoint)
                if options.fastScan :
                    gridpoints+= " --fastScan"
            fitresults=  ""
            if options.saveResults :
                fitresults = " | grep -A 10 -E '\s*--- MultiDimFit ---\s*' > multi-dim.fitresult"
            ## do the fit/scan
            print "combine -M MultiDimFit -m {mass} --algo={algo} -n {name} --cl {CL} {points} {minuit} {stable} {user} {wdir}/{input}.root {result}".format(
                mass=mass, algo=options.fitAlgo, name=options.name, CL=options.confidenceLevel, points=gridpoints, minuit=minuitopt, stable=stableopt, user=options.userOpt,
                wdir=options.workingdir, input=model[0], result=fitresults)
            os.system("combine -M MultiDimFit -m {mass} --algo={algo} -n {name} --cl {CL} {points} {minuit} {stable} {user} {wdir}/{input}.root {result}".format(
                mass=mass, algo=options.fitAlgo, name=options.name, CL=options.confidenceLevel, points=gridpoints, minuit=minuitopt, stable=stableopt, user=options.userOpt,
                wdir=options.workingdir, input=model[0], result=fitresults))
            if not options.firstPoint == "":
                os.system("mv higgsCombine{name}.MultiDimFit.mH{mass}.root higgsCombine{name}.MultiDimFit.mH{mass}-{label}.root".format(
                    name=options.name, mass=mass, label="%s-%s" % (options.firstPoint, options.lastPoint)))
    ##
    ## SIGNIFICANCE
    ##
    if options.optSig :
        ## determine mass value from directory name
        mass  = get_mass(directory)
        ## prepare workspace
        create_card_workspace(mass)
        ## create a hadd'ed file per crab directory if applicable        
        ifile=0
        directoryList = os.listdir(".")
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
            if not ifile == 0 :
                os.system("hadd batch_collected.root batch_collected_*.root")
                os.system("rm batch_collected_*.root")
            else :
                ## calculate expected significance
                print "combine -M ProfileLikelihood -t {toys} --significance --toysFreq --signalForSignificance={sig} -m {mass} {wdir}/tmp.root".format(
                    toys=options.toys, sig=options.signal_strength, mass=mass, wdir=options.workingdir)
                os.system("combine -M ProfileLikelihood -t {toys} --significance --toysFreq --signalForSignificance={sig} -m {mass} {wdir}/tmp.root".format(
                    toys=options.toys, sig=options.signal_strength, mass=mass, wdir=options.workingdir))
                ## mv output to the name as expected from the output of a batch job, as this is what the plotting tools will expect.
                os.system("mv higgsCombineTest.ProfileLikelihood.mH125.123456.root batch_collected.root")
        if not options.expectedOnly :
            ## calculate observed significance
            print "combine -M ProfileLikelihood --significance -m {mass} {wdir}/tmp.root".format(mass=mass, wdir=options.workingdir)
            os.system("combine -M ProfileLikelihood --significance -m {mass} {wdir}/tmp.root".format(mass=mass, wdir=options.workingdir))
    ##
    ## ASYMPTOTIC
    ##
    if options.optAsym :
        ## determine mass value from directory name
        mass  = get_mass(directory)
        ## prepare workspace
        model = []
        if "=" in options.fitModel :
            model = options.fitModel.split('=')
            create_card_workspace_with_physics_model(mass)
        elif options.fitModel == "" :
            create_card_workspace(mass)
        else :
            model = [options.fitModel]
        ## ------------------------------------------------------------------------------------------------------------
        ## OLD STYLE
        ## combine datacard from all datacards in this directory if not done so already
        #if "=" in options.fitModel :
        #    ## collect all cards that should be combined into the model. If used with a dedicated fit model
        #    ## like in the MSSM case, only cards that can be identified to belong to an available decay
        #    ## channel can be combined. this is only a practical limita tion fro now.  
        #    inputcards = ""
        #    for card in os.listdir(".") :
        #        if "htt_" in card or "hbb_" in card or "hmm_" in card :
        #            if options.fitModelCategories == "" :
        #                inputcards+=card[:card.find('.')]+'='+card+' '
        #            else :
        #                allowed_categories = options.fitModelCategories.split(':')
        #                for allowed in allowed_categories :
        #                    if allowed in card :
        #                        inputcards+=card[:card.find('.')]+'='+card+' '
        #    print "combineCards.py -S %s > %s/tmp.txt" % (inputcards, options.workingdir)
        #    os.system("combineCards.py -S %s > %s/tmp.txt" % (inputcards, options.workingdir))
        #else:
        #    ## here all kind of datacards are allowed
        #    if not os.path.exists("%s/tmp.txt" % options.workingdir) :
        #        print "combineCards.py -S *.txt > %s/tmp.txt" % options.workingdir
        #        os.system("combineCards.py -S *.txt > %s/tmp.txt" % options.workingdir)            
        ### set up the physics model
        #model = []
        #if "=" in options.fitModel :
        #    model = options.fitModel.split('=')
        #    ## combine datacard from all datacards in this directory. For the multi-dimensional fit
        #    ## it is of importance that the decay channels and run periods are well defined from the
        #    ## channel names. Allow for a restriction of the event categories
        #    if os.path.exists("%s/%s.root" % (options.workingdir, model[0])) :
        #        os.system("rm %s/%s.root" % (options.workingdir, model[0]))
        #    ## create workspace with dedicated physics model
        #    workspaceOptions = "-m %s " % mass
        #    workspaceOptions+= "-o %s/%s.root " % (options.workingdir, model[0])
        #    workspaceOptions+= "-P %s " % model[1]
        #    if not options.fitModelOptions == "" :
        #        ## break physics model options to list
        #        opts = options.fitModelOptions.split(';')
        #        for idx in range(len(opts)) : opts[idx] = opts[idx].rstrip(',')
        #        for opt in opts :
        #            workspaceOptions+="--PO %s " % opt
        #    print "text2workspace.py %s/tmp.txt %s" % (options.workingdir, workspaceOptions)
        #    os.system("text2workspace.py %s/tmp.txt %s" % (options.workingdir, workspaceOptions))
        #else :
        #    ## prepare binary workspace
        #    print "text2workspace.py --default-morphing=%s -m %s -b %s/tmp.txt -o %s/tmp.root"% (options.shape, mass, options.workingdir, options.workingdir)
        #    os.system("text2workspace.py --default-morphing=%s -m %s -b %s/tmp.txt -o %s/tmp.root"% (options.shape, mass, options.workingdir, options.workingdir))
        ## OLD STYLE
        ## ------------------------------------------------------------------------------------------------------------
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
        massopt = "-m %s " % mass
        ## run expected limits
        wsp = 'tmp' if len(model) == 0 else model[0]
        if not options.observedOnly :
            print "combine -M Asymptotic --run expected -C {cl} {minuit} {prefit} --minimizerStrategy {strategy} -n '-exp' {mass} {user} {wdir}/{wsp}.root".format(
                cl=options.confidenceLevel, minuit=minuitopt, prefit=prefitopt, strategy=options.strategy, mass=massopt, user=options.userOpt, wdir=options.workingdir, wsp=wsp)
            os.system("combine -M Asymptotic --run expected -C {cl} {minuit} {prefit} --minimizerStrategy {strategy} -n '-exp' {mass} {user} {wdir}/{wsp}.root".format(
                cl=options.confidenceLevel, minuit=minuitopt, prefit=prefitopt, strategy=options.strategy, mass=massopt, user=options.userOpt, wdir=options.workingdir, wsp=wsp))
        ## run observed limit
        if not options.expectedOnly :
            print "combine -M Asymptotic --run observed -C {cl} {minuit} --minimizerStrategy {strategy} -n '-obs' {qtilde} {mass} {user} {wdir}/{wsp}.root".format(
                cl=options.confidenceLevel, minuit=minuitopt, qtilde=qtildeopt, strategy=options.strategy, mass=massopt, user=options.userOpt, wdir=options.workingdir, wsp=wsp)
            os.system("combine -M Asymptotic --run observed -C {cl} {minuit} --minimizerStrategy {strategy} -n '-obs' {qtilde} {mass} {user} {wdir}/{wsp}.root".format(
                cl=options.confidenceLevel, minuit=minuitopt, qtilde=qtildeopt, strategy=options.strategy, mass=massopt, user=options.userOpt, wdir=options.workingdir, wsp=wsp))
    ##
    ## CLS
    ##
    if options.optCLs :
        ## determine mass value from directory name
        mass  = get_mass(directory)
        ## create a hadd'ed file per crab directory
        ifile=0
        directoryList = os.listdir(".")
        for name in directoryList :
            if name.find("crab_0")>-1 and not name.find(".")>-1:
                if os.path.exists("batch_collected_%s.root" % ifile) :
                    os.system("rm batch_collected_%s.root" % ifile)
                os.system("hadd batch_collected_%s.root %s/res/*.root" % (ifile, name))
                ifile=ifile+1
        ## and finally hadd all sub files corresponding to each crab directory
        if os.path.exists("batch_collected.root") :
            os.system("rm batch_collected.root")
        if not ifile == 0 :
            os.system("hadd batch_collected.root batch_collected_*.root")
            os.system("rm batch_collected_*.root")
        if not options.expectedOnly :
            ## observed limit
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root" % mass)
        if not options.observedOnly :
            ## expected -2sigma
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root --expectedFromGrid 0.0275" % mass)
            ## expected -1sigma
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root --expectedFromGrid 0.1600" % mass)
            ## expected median
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root --expectedFromGrid 0.5000" % mass)
            ## expected +1sigma
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root --expectedFromGrid 0.8400" % mass)
            ## expected +2sigma
            os.system("combine batch.root -M HybridNew -m %s --freq --grid=batch_collected.root --expectedFromGrid 0.9750" % mass)
    ##
    ## BAYES
    ##
    if options.optBayes :
        ## determine mass value from directory name
        mass  = get_mass(directory)
        ## create a hadd'ed file per crab directory
        ifile=0
        directoryList = os.listdir(".")
        for name in directoryList :
            if name.find("crab_0")>-1 and not name.find(".")>-1:
                if os.path.exists("batch_collected_%s.root" % ifile) :
                    os.system("rm batch_collected_%s.root" % ifile)
                os.system("hadd batch_collected_%s.root %s/res/*.root" % (ifile, name))
                ifile=ifile+1
        ## and finally hadd all sub files corresponding to each crab directory
        if os.path.exists("batch_collected.root") :
            os.system("rm batch_collected.root")
        if not ifile == 0 :
            os.system("hadd batch_collected.root batch_collected_*.root")
            os.system("rm batch_collected_*.root")
        ## clean up from legacy of former trials to get the observed limit
        if os.path.exists("higgsCombineTest.MarkovChainMC.mH%s.root" % mass) :
            os.system("rm higgsCombineTest.MarkovChainMC.mH%s.root" % mass)
        ## in case the observed was calculated via crab just copy it to the head
        ## directory else run it interactively
        if os.path.exists("observed") :
            if not options.expectedOnly :
                os.system("cp observed/crab_0_*/res/higgsCombineTest.MarkovChainMC.mH{mass}*.root ./higgsCombineTest.MarkovChainMC.mH{mass}.root".format(mass=mass))
        else :
            os.system("combine -M MarkovChainMC -H {hint} --rMin {rMin} --rMax {rMax} -i {iter} --tries {tries} --mass {mass} {user} -d batch.root".format(
                hint=options.hint, rMin=options.rMin, rMax=options.rMax, tries=options.tries, mass=mass, user=options.userOpt, iter=options.iter))
    ##
    ## TANB
    ##
    if options.optTanb :
        ## determine mass value from directory name
        mass  = get_mass(directory)
        ## create a hadd'ed file per crab directory
        ifile=0
        directoryList = os.listdir(".")
        for name in directoryList :
            if name.find("crab_0")>-1 and not name.find(".")>-1:
                if os.path.exists("batch_collected_%s.root" % ifile) :
                    os.system("rm batch_collected_%s.root" % ifile)
                os.system("hadd batch_collected_%s.root %s/res/*.root" % (ifile, name))
                ifile=ifile+1
        ## and finally hadd all sub files corresponding to each crab directory
        if os.path.exists("batch_collected.root") :
            os.system("rm batch_collected.root")
        if not ifile == 0 :
            os.system("hadd batch_collected.root batch_collected_*.root")
            os.system("rm batch_collected_*.root")
        ## fetch workspace for the first best tanb point
        for wsp in directoryList :
            if re.match(r"batch_\d+(.\d\d)?.root", wsp) :
                if not options.expectedOnly :
                    ## observed limit
                    os.system("combine %s -M HybridNew -m %s --fullGrid --noUpdateGrid --freq --grid=batch_collected.root" % (wsp, mass))
                if not options.observedOnly :
                    ## expected -2sigma
                    os.system("combine %s -M HybridNew -m %s --freq --fullGrid --grid=batch_collected.root --expectedFromGrid 0.0275" % (wsp, mass))
                    ## expected -1sigma
                    os.system("combine %s -M HybridNew -m %s --freq --fullGrid --grid=batch_collected.root --expectedFromGrid 0.1600" % (wsp, mass))
                    ## expected median
                    os.system("combine %s -M HybridNew -m %s --freq --fullGrid --grid=batch_collected.root --expectedFromGrid 0.5000" % (wsp, mass))
                    ## expected +1sigma
                    os.system("combine %s -M HybridNew -m %s --freq --fullGrid --grid=batch_collected.root --expectedFromGrid 0.8400" % (wsp, mass))
                    ## expected +2sigma
                    os.system("combine %s -M HybridNew -m %s --freq --fullGrid --grid=batch_collected.root --expectedFromGrid 0.9750" % (wsp, mass))
                ## break after first success (assuming that all workspaces are fine to do the interpolation)
                break
    ##
    ## TANB+
    ##
    if options.optTanbPlus :
        ## determine mass value from directory name
        mass  = get_mass(directory)
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
        ## list of all elements in the current directory
        tasks = []
        ## string for tanb inputfiles
        tanb_inputfiles = ""
        ## fetch workspace for each tanb point
        directoryList = os.listdir(".")
        for wsp in directoryList :
            if re.match(r"batch_\d+(.\d\d)?.root", wsp) :
                tanb_inputfiles += wsp.replace("batch", "point")+","
                tanb_string = wsp[wsp.rfind("_")+1:]
                if not options.refit :
                    tasks.append(
                        ["combine -M Asymptotic -n .tanb{tanb} --run both -C {CL} {minuit} {prefit} --minimizerStrategy {strategy} -m {mass} {user} {wsp}".format(
                        CL=options.confidenceLevel, minuit=minuitopt, prefit=prefitopt,strategy=options.strategy,mass=mass, wsp=wsp, user=options.userOpt, tanb=tanb_string),
                         "mv higgsCombine.tanb{tanb}.Asymptotic.mH{mass}.root point_{tanb}".format(mass=mass, tanb=tanb_string)
                         ]
                        )
        if options.tanbMultiCore == -1:
            for task in tasks:
                for subtask in task:
                    os.system(subtask)
        else:
            ## run in parallel using multiple cores
            parallelize(tasks, options.tanbMultiCore)
        tanb_inputfiles = tanb_inputfiles.rstrip(",")
        ## combine limits of individual tanb point to a single file equivalent to the standard output of --optCLs
        ## to be compatible with the output of the option --optTanb for further processing
        cmssw_base = os.environ["CMSSW_BASE"]
        cmd = cmssw_base+"/src/HiggsAnalysis/HiggsToTauTau/macros/asymptoticLimit.C+"
        ## clean up directory from former run
        os.system("rm higgsCombineTest.HybridNew*")
        if not options.expectedOnly :
            os.system(r"root -l -b -q {CMD}\(\"higgsCombineTest.HybridNew.mH{MASS}.root\",\"{FILES}\",2\)".format(CMD=cmd, MASS=mass, FILES=tanb_inputfiles))
        if not options.observedOnly :
            os.system(r"root -l -b -q {CMD}\(\"higgsCombineTest.HybridNew.mH{MASS}.quant0.027.root\",\"{FILES}\",2\)".format(CMD=cmd, MASS=mass, FILES=tanb_inputfiles))
            os.system(r"root -l -b -q {CMD}\(\"higgsCombineTest.HybridNew.mH{MASS}.quant0.160.root\",\"{FILES}\",2\)".format(CMD=cmd, MASS=mass, FILES=tanb_inputfiles))
            os.system(r"root -l -b -q {CMD}\(\"higgsCombineTest.HybridNew.mH{MASS}.quant0.500.root\",\"{FILES}\",2\)".format(CMD=cmd, MASS=mass, FILES=tanb_inputfiles))
            os.system(r"root -l -b -q {CMD}\(\"higgsCombineTest.HybridNew.mH{MASS}.quant0.840.root\",\"{FILES}\",2\)".format(CMD=cmd, MASS=mass, FILES=tanb_inputfiles))
            os.system(r"root -l -b -q {CMD}\(\"higgsCombineTest.HybridNew.mH{MASS}.quant0.975.root\",\"{FILES}\",2\)".format(CMD=cmd, MASS=mass, FILES=tanb_inputfiles))
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
    ## remove any previous hashes
    os.system("rm -f limit_hash_*")
    ## create hash file for this call, so we can use the norepeat feature.
    hash_file = get_hash_for_this_call()
    os.system("touch %s" % hash_file)
    print "done"
