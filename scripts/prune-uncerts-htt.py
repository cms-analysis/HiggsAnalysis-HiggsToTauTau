#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to prune uncertainties of an existing set of datacards. The script needs as inputs the directory that contains all datacards, which are supposed to be processed and the output of the maximum likelihood fit and the script diffNuisances.py in text format. The latter should be passed on by option --fit-results. Note that option --fit-results can also take a list of these files produced on subsets of the datacards in question. In this case for correlated uncertainties the pruning decision will be based on the maximal shift in the individual fits. The script optionally takes a list of regular expressions for uncertainties that should not be considered for pruning using the option --blacklist. The pruning takes place based on the relative shift of the nuisance parameter in the maximum likelihood fit(s). The metric can be switched between the result of the background-only fit ('b'), the signal-plus-background fit ('s+b') or the maximum of the two ('max'). A threshold on the shift can be given via option --threshold. Each nuisance parameter, for which the relative shift in the according metric falls below this threshold will be be added to a list of uncertainties to be pruned. You can optionally choose to have these uncertainties already commented in the tested datacards at the same time. The output of the script is the list of pruned and a list of kept nuisance parameters in text format (uncertainty-pruning-[drop/keep].txt). In the current implementation the script is meant to be used for datacards for counting experiments or for shape analyses based on histograms. ARG corresponds to the input directory where to find the datacards.")
parser.add_option("--fit-results", dest="fit_results", default="", type="string",
                  help="The absolute path to the output file(s) of the maximum likelihood fit and the script diffNuisances.py, which returns the output of the maximum likelihood fit in txt format. For this purpose the script diffNuisances.py should be run with options -A, -f text and -a. Note that you can also pass a list of maximum likelihood fit outputs based on a subsets of datacards. In this case the absolute paths to all maximum likelihood fit output files should be passed on embraced by quotation marks and separated by whitespace. [Default: \"\"]")
parser.add_option("--metric", dest="metric", default="max",  type="choice", choices=['b', 's+b', 'max'],
                  help="The metric to be used for the pruning decision. Choices are: b (pull for background-only fit), s+b (pull for signal-plus-background fit), the maximum of 'b' and 's+b'. [Default: 'max']")
parser.add_option("-m", "--mass", dest="mass", default="125", type="string",
                  help="The mass value to be chosen, when considering the signal-plus-background fit in the metric. If the metric of the background-only fit is chosen this option has no effect. [Default: \"125\"]")
parser.add_option("--threshold", dest="threshold", default="0.05", type="string",
                  help="The threshold to determine the nuisance parameters to be pruned. The value corresponds to the relative shift of the parameter in the maximum likelihood fit(s). If the shift of the nuisance parameter falls below this threshold the nuisance parameter will be added to the list of nuisance parameters to be pruned. [Default: 0.05]")
parser.add_option("--blacklist", dest="blacklist", default="", type="string",
                  help="A list of regular python style expressions for nuisance parameters that should not be considered during the pruning decision. (You can add holy cows here.) The regular expressions should be embraced by quotation marks and separated by whitespace. [Default: \"\"]")
parser.add_option("--whitelist", dest="whitelist", default="", type="string",
                  help="A list of regular python style expressions that can be used to restrict the pruning to only those nuisance parameters that match these expressions. (You can e.g. restrict yourself only to bin-by-bin uncertainties.) The regular expressions should be embraced by quotation marks and separated by whitespace. [Default: \"\"]")
parser.add_option("--comment-nuisances", dest="comment_nuisances", default=False, action="store_true",
                  help="Use this option if you want to comment the uncertainties added to the list of pruned nuisance parameters from the tested datacards at the same time. [Default: False]")
parser.add_option("--shielding", dest="shielding", default="", type="string",
                  help="This parameter allows to apply a shielding of bin-by-bin uncertainties in sensitive regions of the input histograms. A shielding window has to be defined by two float values separated by a call-on (i.e. value1:value2). Value1 corresponds to the central value of the sensitive region in the input histogram. Value2 corresponds to a window size given as relative value (e.g. 125:0.3, 0.3 corresponds to 30%). More than one window can be passed via this option. Then the individual value pairs should be embraced by quotation marks and separated by whitespace. [Default: \"\"]")
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import random
import string
from HiggsAnalysis.HiggsToTauTau.HttPruner import HttPruner

def remove_empty_strings(list) :
    """
    Remove emptry strings from list
    """
    indices = []
    for idx in range(len(list)) :
        if list[idx] == '' : indices.append(idx)
    for idx in indices :
        list.pop(idx)
    return list
        
def main() :
    ## turn options.fit_results into a list
    fit_results = options.fit_results.replace('$PWD', os.getcwd()).split(' ')
    for idx in range(len(fit_results)) : fit_results[idx] = fit_results[idx].rstrip(',')
    fit_results = remove_empty_strings(fit_results)
    ## turn options.blacklist into a list
    blacklist = options.blacklist.split(' ')
    for idx in range(len(blacklist)) : blacklist[idx] = blacklist[idx].rstrip(',')
    blacklist = remove_empty_strings(blacklist)
    ## turn options.whitelist into a list
    whitelist = options.whitelist.split(' ')
    for idx in range(len(whitelist)) : whitelist[idx] = whitelist[idx].rstrip(',')
    whitelist = remove_empty_strings(whitelist)
    ## turn options.shielding into a list
    shielding = options.shielding.split(' ')
    for idx in range(len(shielding)) : shielding[idx] = shielding[idx].rstrip(',')
    shielding = remove_empty_strings(shielding)

    print "# --------------------------------------------------------------------------------------"
    print "# Pruning uncertainties. "
    print "# --------------------------------------------------------------------------------------"
    print "# You are using the following configuration: "
    print "# --fit-results       :", fit_results
    print "# --metric            :", options.metric
    print "# --mass              :", options.mass
    print "# --threshold         :", options.threshold
    print "# --blacklist         :", blacklist
    print "# --whitelist         :", whitelist
    print "# --shielding         :", shielding
    print "# --comment-nuisances :", options.comment_nuisances
    print "# Check option --help in case of doubt about the meaning of one or more of these confi-"
    print "# guration parameters.                           "
    print "# --------------------------------------------------------------------------------------"

    ## create a list of windows from the elements in list shielding
    windows = []
    for elem in shielding :
        windows.append((elem[:elem.find(':')], elem[elem.find(':')+1:]))

    ## create a combined datacard from input datacards
    datacard='/tmp/'+''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    os.system("combineCards.py -S {PATH}/*.txt > {DATACARD}".format(PATH=args[0], DATACARD=datacard))

    pruner = HttPruner(fit_results, options.metric, options.mass, options.threshold, blacklist, whitelist, options.comment_nuisances, windows)
    ## determine list of all uncertainties from input datacards 
    uncerts = pruner.determine_uncerts(datacard)
    ## determine list of dropped and kept uncertainties from input datacards
    (dropped, kept, confused) = pruner.prune(uncerts)
    ## apply shielding if configured such
    rescued = 0
    if len(windows)>0 :
        (dropped, rescued) = pruner.shield_bbb_uncertainties(datacard, dropped, kept)
    ## write dropped and kept uncertainties to file
    pruner.list_to_file(kept   , "uncertainty-pruning-keep.txt")
    pruner.list_to_file(dropped, "uncertainty-pruning-drop.txt")
    ## comment dropped uncertainties from datacards if configured such
    if options.comment_nuisances :
        num = 0
        for file in glob.glob(args[0]+'/*.txt') : 
            num = pruner.manipulate_datacard(file, "COMMENT", dropped)

    print "# Excluded", len(dropped), "uncertainties from", len(dropped)+len(kept), ": (", confused, "not pruned due to missmatch of inputs)."
    print "#                                       (", rescued, "rescued by shielding)."
    print "# Check the output files uncertainty-pruning-keep.txt and uncertainty-pruning-drop.txt"
    print "# for the full list of pruned and and kept parameters.                                "
    print "# --------------------------------------------------------------------------------------"
    
main()
exit(0)
