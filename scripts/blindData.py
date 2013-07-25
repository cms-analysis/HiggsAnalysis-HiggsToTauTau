#!/usr/bin/env python

from optparse import OptionParser, OptionGroup
from HiggsAnalysis.CombinedLimit.DatacardParser import *

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to apply blinding to a set of datacards located in the directory given by ARG. Depending on the configuration of the script signal can be added or not. In case it is added it can be scaled by factor, which is common to all signal processes indicated in the datacards. If necessary the mass of the signal to be injected can be given. If a random seed larger equal 0 is chosen the created asimov dataset is being randomized after creation. The script can work with binned shape analyses, based on root histograms or counting experiments.\n")
parser_opts = OptionGroup(parser, "DATACARD PARSER OPTIONS", "These are the options that can be passed on to configure the datacard parsing.")
addDatacardParserOptions(parser_opts)
parser.add_option_group(parser_opts)
asimov_opts = OptionGroup(parser, "ASIMOV DATACARD OPTIONS", "These are the options that can be passed on to configure the creation of the asomiv dataset used fro blinding.")
asimov_opts.add_option("--update-file", dest="update_file", default=False, action="store_true",
                  help="Use this option if you want to update the same file instead of writing a new file. In the case of --update_file=True a new temaplte histogram will be written to file with the name data_obs_asimov for each template histogram with name data_obs that is found. In case of --update-file=False the new data_obs template histograms will be written into a new file with additional label _asimov at the same location as the original file and with the same file structure. [Default: False]")
asimov_opts.add_option("--seed", dest="seed", default="-1", type="string",
                       help="Random seed. If you want the asimov dataset to be randomized after being created use a random seed, which is larger equal to 0. Default: \"-1\"]")
asimov_opts.add_option("--inject-signal", dest="inject_signal", default=False, action="store_true",
                  help="Use this option if you want signal to be added to the asimov dataset. In case all signal contribution, as indicated in the datacards will be chosen. [Default: False]")
asimov_opts.add_option("--injected-scale", dest="injected_scale", default="1", type="string",
                       help="Scale for signal. This is only of relevance if signal should be added to the asimov dataset. The scale factor will than be applied equally to each signal contribution. Default: \"1\"]")
asimov_opts.add_option("--injected-mass", dest="injected_mass", default="125", type="string",
                       help="The mass of the signal that should be injected. Default: \"125\"]")
asimov_opts.add_option("--extra-templates", dest="extra_templates", default="", type="string",
                       help="List of extra background or signal templates which should be injected to the asimov dataset. Needs to be comma seperated list. For example to inject SM signal into MSSM datacards. [Default: \"\"]")
asimov_opts.add_option("--blacklist", dest="blacklist", default="", type="string",
                       help="List of signal or background templates that should be ignored when creating the asimov dataset. Needs to be comma seperated list. Use cases are a central template that should be replaced by a template to which a shift has been applied (added to --extra-templates) or to add a set of signal processes that should be ignored when creating the asimov dataset with signal injected. [Default: \"\"]")
parser.add_option_group(asimov_opts)
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import glob
from HiggsAnalysis.HiggsToTauTau.AsimovDatacard import *

## blacklist
blacklist = options.blacklist.split()
for idx in range(len(blacklist)) : blacklist[idx] = blacklist[idx].rstrip(',')

def main() :
    print "# --------------------------------------------------------------------------------------"
    print "# Blinding datacards. "
    print "# --------------------------------------------------------------------------------------"
    print "# You are using the following configuration: "
    print "# --update-file    :", options.update_file
    print "# --seed           :", options.seed
    print "# --inject-signal  :", options.inject_signal
    print "# --injected-scale :", options.injected_scale
    print "# --injected-mass  :", options.injected_mass
    print "# --extra-templates:", options.extra_templates
    print "# --blacklist      :", blacklist
    print "# Check option --help in case of doubt about the meaning of one or more of these confi-"
    print "# guration parameters.                           "
    print "# --------------------------------------------------------------------------------------"
    cardMaker = AsimovDatacard(options, options.update_file, options.seed, options.inject_signal, options.injected_mass, options.injected_scale, options.extra_templates, blacklist)
    ## clean up directory from former trials
    cardMaker.cleanup(args[0], '_asimov')
    cardMaker.make_asimov_datacards(args[0])

main()
exit(0)
