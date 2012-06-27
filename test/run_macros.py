from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to run all macros to create postfit plots. Macros have to be prodiced before hand and are expected to be located in the test directory.")
## direct options
parser.add_option("-a", "--analysis", dest="analysis", default="sm", type="choice", help="Type of analysis (sm or mssm). Lower case is required. [Default: sm]", choices=["sm", "mssm"])
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string", help="List of run periods for which the datacards are to be copied. [Default: \"7TeV 8TeV\"]")
parser.add_option("-c", "--channels", dest="channels", default="em, et, mt", type="string", help="Channels, for which to make the postfit plots. [Default: 'em, et, mt']")
parser.add_option("--sm-categories", dest="sm_categories", default="0 1 2 3 5", type="string", help="List sm of event categories. [Default: \"0 1 2 3 5\"]")
parser.add_option("--mssm-categories", dest="mssm_categories", default="0 1 2 3 6 7", type="string", help="List mssm of event categories. [Default: \"0 1 2 3 6 7\"]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) > 0 :
    parser.print_usage()
    exit(1)

import os

## run periods
periods = options.periods.split()
for idx in range(len(periods)) : periods[idx] = periods[idx].rstrip(',')
## channels 
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')
## categories
categories = options.sm_categories.split() if options.analysis == "sm" else options.mssm_categories.split()
for idx in range(len(categories)) : categories[idx] = categories[idx].rstrip(',')

log = {
    ("em", "0") : "true",  #    if options.analysis == "sm" else  "true" ,
    ("em", "1") : "false", #    if options.analysis == "sm" else  "false",
    ("em", "2") : "false", #   if options.analysis == "sm" else  "true" ,
    ("em", "3") : "false", #   if options.analysis == "sm" else  "false",
    ("em", "5") : "false",
    ("em", "6") : "false",
    ("em", "7") : "false", 
    ("mt", "0") : "true", 
    ("mt", "1") : "false", 
    ("mt", "2") : "false",
    ("mt", "3") : "false",
    ("mt", "5") : "false",
    ("mt", "6") : "false",
    ("mt", "7") : "false",
    ("et", "0") : "false"   if options.analysis == "sm" else  "false",
    ("et", "1") : "false"   if options.analysis == "sm" else  "false", 
    ("et", "2") : "false"   if options.analysis == "sm" else  "false", 
    ("et", "3") : "false"   if options.analysis == "sm" else  "false", 
    ("et", "5") : "false",
    ("et", "6") : "false",
    ("et", "7") : "false",
    }

max = {
    ("em", "0") :  "500", #    if options.analysis == "sm" else "300",  
    ("em", "1") :   "30", #    if options.analysis == "sm" else  "40",  
    ("em", "2") :   "50", #    if options.analysis == "sm" else  "10",  
    ("em", "3") :   "15", #    if options.analysis == "sm" else   "2",  
    ("em", "5") :  "1.4",
    ("em", "6") :    "8",
    ("em", "7") :    "3",
    ("mt", "0") : "2000",
    ("mt", "1") :  "110", 
    ("mt", "2") :  "160",
    ("mt", "3") :   "60",
    ("mt", "5") :    "3",
    ("mt", "6") :   "20",
    ("mt", "7") :    "5",
    ("et", "0") :   "40"    if options.analysis == "sm" else  "40", 
    ("et", "1") :   "16"    if options.analysis == "sm" else  "10", 
    ("et", "2") :   "30"    if options.analysis == "sm" else  "40", 
    ("et", "3") :   "10"    if options.analysis == "sm" else  "10", 
    ("et", "5") :  "1.5",
    ("et", "6") :   "10",
    ("et", "7") :  "2.4",
    }

min = {
    ("em", "0") : "0.1", #   if options.analysis == "sm" else  "0.1", 
    ("em", "1") : "0.",  #   if options.analysis == "sm" else   "0.", 
    ("em", "2") : "0.",  #     if options.analysis == "sm" else  "0.1", 
    ("em", "3") : "0.",  #     if options.analysis == "sm" else   "0.", 
    ("em", "5") : "0.",
    ("em", "6") : "0.",
    ("em", "7") : "0.",
    ("mt", "0") : "0.1",
    ("mt", "1") : "0.", 
    ("mt", "2") : "0.",
    ("mt", "3") : "0.",
    ("mt", "5") : "0.",
    ("mt", "6") : "0.",
    ("mt", "7") : "0.",
    ("et", "0") : "0."     if options.analysis == "sm" else  "0.",
    ("et", "1") : "0."     if options.analysis == "sm" else  "0.",
    ("et", "2") : "0."     if options.analysis == "sm" else  "0.",
    ("et", "3") : "0."     if options.analysis == "sm" else  "0.",
    ("et", "5") : "0.",
    ("et", "6") : "0.",
    ("et", "7") : "0.",
    }

for chn in channels :
    for per in periods :
        for cat in categories :
            for sca in ["true", "false"] :
                bash_script = "root -l -b -q htt_{CHN}_{CAT}_{PER}.C+\(\"{SCA}\",\"{LOG}\",{MIN},{MAX}\)".format(
                    SCA=sca, LOG=log[(chn,cat)],  MIN=min[(chn,cat)], MAX=max[(chn,cat)], CHN=chn, CAT=cat, PER=per)
                os.system(bash_script)
