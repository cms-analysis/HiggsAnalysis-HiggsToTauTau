#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to setup the limit calculation for htt from a prepared reservoir of datacards. The output directory to copy the datacards to is expected to have a dedicated structure. Directories that do not exist are created on the fly. ARGS corresponds to a list of integer values resembling the mass points for which you want to create the datacards. Ranges can be indicated e.g. by: 110-145'. That only any x-th mass point should be taken into account can be indicated e.g. by: 110-145:5. The latter example will pick up the masses 110 115 120 130 135 140 145. Any combination of this syntax is possible.")
parser.add_option("-i", "--in", dest="input", default="auxiliaries/datacards", type="string", help="Name of the input directory from which to copy the prepared datacards. [Default: auxiliaries/datacards]")
parser.add_option("-o", "--out", dest="out", default="htt-limits", type="string", help="Name of the output directory to which the datacards should be copied. [Default: htt-limits]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string", help="Choose between run periods [Default: \"7TeV 8TeV\"]")
parser.add_option("-a", "--analysis", dest="analysis", default="Hhh", type="choice", help="Type of analysis (Hhh or mssm). Lower case is required. [Default: Hhh]", choices=["Hhh", "mssm"])
parser.add_option("-c", "--channels", dest="channels", default="mm em mt et", type="string", help="List of channels, for which datacards should be created. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt, hmm, hbb. [Default: \"mm em mt et\"]")
parser.add_option("-l", "--label", dest="label", default="", type="string", help="Add a label to the subdirectories that belong to each corresponding sub-channel. [Default: \"\"]")
parser.add_option("-s", "--setup", dest="setup", default="all", type="choice", help="Setup in which to run. Choises are between cmb only (cmb), split by channels (chn), split by event category (cat), all (all). The combiend limit will always be calculated. [Default: all]", choices=["cmb", "chn", "cat", "all"])
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Run in verbose mode. [Default: False]")
parser.add_option("--lowmH", dest="lowmH", default=False, action="store_true", help="Setup of directory structure for lowmH MSSM scenario. [Default: False]")
parser.add_option("--SM4", dest="SM4", default=False, action="store_true", help="Copy datacards for SM4 (for SM only). [Default: False]")
cats1 = OptionGroup(parser, "Hhh EVENT CATEGORIES", "Event categories to be picked up for the Hhh analysis.")
cats1.add_option("--Hhh-categories-ee", dest="ee_Hhh_categories", default="0 1 2 3 4", type="string", help="List of ee event categories. [Default: \"0 1 2 3 4\"]")
cats1.add_option("--Hhh-categories-mm", dest="mm_Hhh_categories", default="0 1 2 3 4", type="string", help="List of mm event categories. [Default: \"0 1 2 3 4\"]")
cats1.add_option("--Hhh-categories-em", dest="em_Hhh_categories", default="0 1 2 3 4", type="string", help="List of em event categories. [Default: \"0 1 2 3 4\"]")
cats1.add_option("--Hhh-categories-mt", dest="mt_Hhh_categories", default="0 1 2", type="string", help="List of mt event categories. [Default: \"0 1 2 3 4\"]")
cats1.add_option("--Hhh-categories-et", dest="et_Hhh_categories", default="0 1 2", type="string", help="List of et event categories. [Default: \"0 1 2 3 4\"]")
cats1.add_option("--Hhh-categories-tt", dest="tt_Hhh_categories", default="0 1 2", type="string", help="List of tt event categories. [Default: \"0 1 2 3 4\"]")
parser.add_option_group(cats1)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

## label
label = "" if options.label == "" else "-"+options.label
## periods
periods = options.periods.split()
for idx in range(len(periods)) : periods[idx] = periods[idx].rstrip(',')
## channels
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')

## switch to Hhh event categories
if options.analysis == "Hhh" :
    categories = {
        "ee"   : options.ee_Hhh_categories.split(),
        "mm"   : options.mm_Hhh_categories.split(),
        "em"   : options.em_Hhh_categories.split(),
        "mt"   : options.mt_Hhh_categories.split(),
        "et"   : options.et_Hhh_categories.split(),
        "tt"   : options.tt_Hhh_categories.split(),
        }


## configuration for summer13

directories_mssm = {
    'ee' : {
    '8'  : ['nobtag', 'nobtag-ee'],
    '9'  : ['btag'  , 'btag-ee'  ],
    },
    'mm' : {
    '8'  : ['nobtag', 'nobtag-mm'],
    '9'  : ['btag'  , 'btag-mm'  ],
    },
    'em' : {
    '8'  : ['nobtag', 'nobtag-em'],
    '9'  : ['btag'  , 'btag-em'  ],
    },    
    'et' : {
    '8'  : ['nobtag', 'nobtag-et'],
    '9'  : ['btag'  , 'btag-et'  ],
    },
    'mt' : {
    '8'  : ['nobtag', 'nobtag-mt'],
    '9'  : ['btag'  , 'btag-mt'  ],
    },
    'tt' : {
    '8'  : ['nobtag', 'nobtag-tt'],
    '9'  : ['btag'  , 'btag-tt'  ],
    },
}

directories_Hhh = {
    'ee' : {
    '0'  : ['2jet0tag', '2jet0tag-ee'],
    '1'  : ['2jet1tag'  , '2jet1tag-ee'  ],
    '2'  : ['2jet2tag'  , '2jet2tag-ee'  ],
    '3'  : ['1jet0tag'  , '1jet0tag-ee'  ],
    '4'  : ['1jet1tag'  , '1jet1tag-ee'  ],
    },
    'mm' : {
    '0'  : ['2jet0tag', '2jet0tag-mm'],
    '1'  : ['2jet1tag'  , '2jet1tag-mm'  ],
    '2'  : ['2jet2tag'  , '2jet2tag-mm'  ],
    '3'  : ['1jet0tag'  , '1jet0tag-mm'  ],
    '4'  : ['1jet1tag'  , '1jet1tag-mm'  ],
    },
    'em' : {
    '0'  : ['2jet0tag', '2jet0tag-em'],
    '1'  : ['2jet1tag'  , '2jet1tag-em'  ],
    '2'  : ['2jet2tag'  , '2jet2tag-em'  ],
    '3'  : ['1jet0tag'  , '1jet0tag-em'  ],
    '4'  : ['1jet1tag'  , '1jet1tag-em'  ],
    },    
    'et' : {
    '0'  : ['2jet0tag', '2jet0tag-et'],
    '1'  : ['2jet1tag'  , '2jet1tag-et'  ],
    '2'  : ['2jet2tag'  , '2jet2tag-et'  ],
    '3'  : ['1jet0tag'  , '1jet0tag-et'  ],
    '4'  : ['1jet1tag'  , '1jet1tag-et'  ],
    },
    'mt' : {
    '0'  : ['2jet0tag', '2jet0tag-mt'],
    '1'  : ['2jet1tag'  , '2jet1tag-mt'  ],
    '2'  : ['2jet2tag'  , '2jet2tag-mt'  ],
    '3'  : ['1jet0tag'  , '1jet0tag-mt'  ],
    '4'  : ['1jet1tag'  , '1jet1tag-mt'  ],
    },
    'tt' : {
    '0'  : ['2jet0tag', '2jet0tag-tt'],
    '1'  : ['2jet1tag'  , '2jet1tag-tt'  ],
    '2'  : ['2jet2tag'  , '2jet2tag-tt'  ],
    '3'  : ['1jet0tag'  , '1jet0tag-tt'  ],
    '4'  : ['1jet1tag'  , '1jet1tag-tt'  ],
    },
}


## determine directories
def directories(channel) :
    if options.analysis == "Hhh" :
        category_names = directories_Hhh
    else :
        category_names = directories_mssm
    return category_names

## setup directory structure in case it does not exist, yet.
if not os.path.exists(options.out) :
    os.system("mkdir {OUTPUT}/".format(OUTPUT=options.out))
if not os.path.exists("{OUTPUT}/cmb{LABEL}".format(OUTPUT=options.out, ANA=options.analysis, LABEL=label)) :
    os.system("mkdir {OUTPUT}/cmb{LABEL}".format(OUTPUT=options.out, ANA=options.analysis, LABEL=label))
for channel in channels :
    if not os.path.exists("{OUTPUT}/{CHN}{LABEL}".format(OUTPUT=options.out, CHN=channel, LABEL=label)) :
        os.system("mkdir {OUTPUT}/{CHN}{LABEL}".format(OUTPUT=options.out, CHN=channel, LABEL=label))
for channel in channels :
    category_names = directories(channel)
    for cat in categories[channel] :
        for dir in category_names[channel][cat]:
            if not os.path.exists("{OUTPUT}/{DIR}{LABEL}".format(OUTPUT=options.out, DIR=dir, LABEL=label)) :
                os.system("mkdir {OUTPUT}/{DIR}{LABEL}".format(OUTPUT=options.out, DIR=dir, LABEL=label))

verb = "-v" if options.verbose else ""

for channel in channels :
    category_names = directories(channel)
    for period in periods :
        for cat in categories[channel] :
            for mass in parseArgs(args) :
                if options.lowmH :
                    print "setup lowmH-directory structure for", options.analysis, period, channel, cat, mass
                    ## setup combined
                    os.system("cvs2local-lowmH.py -i {INPUT} -o {OUTPUT} -p {PER} -a {ANA} -c {CHN} --no-update --{ANA}-categories-{CHN} {CAT} {VERB} {MASS}".format(
                        INPUT=options.input, OUTPUT=options.out+"/cmb"+label, PER=period, ANA=options.analysis, CHN=channel, CAT=cat, VERB=verb, MASS=mass))
                    if options.setup == "all" or options.setup == "chn" :
                        ## setup channel-wise
                        os.system("cvs2local-lowmH.py -i {INPUT} -o {OUTPUT} -p {PER} -a {ANA} -c {CHN} --no-update --{ANA}-categories-{CHN} {CAT} {VERB} {MASS}".format(
                            INPUT=options.input, OUTPUT=options.out+"/"+channel+label, PER=period, ANA=options.analysis, CHN=channel, CAT=cat, VERB=verb, MASS=mass))
                    if options.setup == "all" or options.setup == "cat" :
                        ## setup category-wise
                        for category in category_names[channel][cat]:
                            os.system("cvs2local-lowmH.py -i {INPUT} -o {OUTPUT} -p {PER} -a {ANA} -c {CHN} --no-update  --{ANA}-categories-{CHN} {CAT} {VERB} {MASS}".format(
                                INPUT=options.input, OUTPUT=options.out+"/"+category+label, PER=period, ANA=options.analysis, CHN=channel, CAT=cat, VERB=verb, MASS=mass))
                else :
                    print "setup directory structure for", options.analysis, period, channel, cat, mass
                    ## setup combined
                    os.system("cvs2local.py -i {INPUT} -o {OUTPUT} -p {PER} -a {ANA} -c {CHN} --no-update --{ANA}-categories-{CHN} {CAT} {VERB} {MASS}".format(
                        INPUT=options.input, OUTPUT=options.out+"/cmb"+label, PER=period, ANA=options.analysis, CHN=channel, CAT=cat, VERB=verb, MASS=mass))
                    if options.setup == "all" or options.setup == "chn" :
                        ## setup channel-wise
                        os.system("cvs2local.py -i {INPUT} -o {OUTPUT} -p {PER} -a {ANA} -c {CHN} --no-update --{ANA}-categories-{CHN} {CAT} {VERB} {MASS}".format(
                            INPUT=options.input, OUTPUT=options.out+"/"+channel+label, PER=period, ANA=options.analysis, CHN=channel, CAT=cat, VERB=verb, MASS=mass))
                    if options.setup == "all" or options.setup == "cat" :
                        ## setup category-wise
                        for category in category_names[channel][cat]:
                            os.system("cvs2local.py -i {INPUT} -o {OUTPUT} -p {PER} -a {ANA} -c {CHN} --no-update  --{ANA}-categories-{CHN} {CAT} {VERB} {MASS}".format(
                                INPUT=options.input, OUTPUT=options.out+"/"+category+label, PER=period, ANA=options.analysis, CHN=channel, CAT=cat, VERB=verb, MASS=mass))
