#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to setup the limit calculation for htt from a prepared reservoir of datacards. The output directory to copy the datacards to is expected to have a dedicated structure. Directories that do not exist are created on the fly. ARGS corresponds to a list of integer values resembling the mass points for which you want to create the datacards. Ranges can be indicated e.g. by: 110-145'. That only any x-th mass point should be taken into account can be indicated e.g. by: 110-145:5. The latter example will pick up the masses 110 115 120 130 135 140 145. Any combination of this syntax is possible.")
parser.add_option("-i", "--in", dest="input", default="auxiliaries/datacards", type="string", help="Name of the input directory from which to copy the prepared datacards. [Default: auxiliaries/datacards]")
parser.add_option("-o", "--out", dest="out", default="htt-limits", type="string", help="Name of the output directory to which the datacards should be copied. [Default: htt-limits]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string", help="Choose between run periods [Default: \"7TeV 8TeV\"]")
parser.add_option("-a", "--analysis", dest="analysis", default="sm", type="choice", help="Type of analysis (sm or mssm). Lower case is required. [Default: sm]", choices=["sm", "mssm"])
parser.add_option("-c", "--channels", dest="channels", default="mm em mt et", type="string", help="List of channels, for which datacards should be created. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt, hmm, hbb. [Default: \"mm em mt et\"]")
parser.add_option("-l", "--label", dest="label", default="", type="string", help="Add a label to the subdirectories that belong to each corresponding sub-channel. [Default: \"\"]")
parser.add_option("-s", "--setup", dest="setup", default="all", type="choice", help="Setup in which to run. Choises are between cmb only (cmb), split by channels (chn), split by event category (cat), all (all). The combiend limit will always be calculated. [Default: all]", choices=["cmb", "chn", "cat", "all"])
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Run in verbose mode. [Default: False]")
parser.add_option("--SM4", dest="SM4", default=False, action="store_true", help="Copy datacards for SM4 (for SM only). [Default: False]")
cats1 = OptionGroup(parser, "SM EVENT CATEGORIES", "Event categories to be picked up for the SM analysis.")
cats1.add_option("--sm-categories-ee", dest="ee_sm_categories", default="0 1 2 3 4", type="string", help="List of ee event categories. [Default: \"0 1 2 3 4\"]")
cats1.add_option("--sm-categories-mm", dest="mm_sm_categories", default="0 1 2 3 4", type="string", help="List of mm event categories. [Default: \"0 1 2 3 4\"]")
cats1.add_option("--sm-categories-em", dest="em_sm_categories", default="0 1 2 3 4", type="string", help="List of em event categories. [Default: \"0 1 2 3 4\"]")
cats1.add_option("--sm-categories-mt", dest="mt_sm_categories", default="0 1 2 3 4 5 6 7", type="string", help="List of mt event categories. [Default: \"0 1 2 3 4 5 6 7 \"]")
cats1.add_option("--sm-categories-et", dest="et_sm_categories", default="0 1 2 3 4 5 6 7", type="string", help="List of et event categories. [Default: \"0 1 2 3 4 5 6 7 \"]")
cats1.add_option("--sm-categories-tt", dest="tt_sm_categories", default="0 1 2", type="string", help="List of tt event categories. [Default: \"0 1 2\"]")
cats1.add_option("--sm-categories-vhtt", dest="vhtt_sm_categories", default="0 1 2", type="string", help="List of vhtt event categories. [Default: \"0 1 2\"]")
parser.add_option_group(cats1)
cats2 = OptionGroup(parser, "MSSM EVENT CATEGORIES", "Event categories to be used for the MSSM analysis.")
cats2.add_option("--mssm-categories-ee", dest="ee_mssm_categories", default="8 9", type="string", help="List of ee event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-mm", dest="mm_mssm_categories", default="8 9", type="string", help="List of mm event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-em", dest="em_mssm_categories", default="8 9", type="string", help="List of em event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-mt", dest="mt_mssm_categories", default="8 9", type="string", help="List of mt event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-et", dest="et_mssm_categories", default="8 9", type="string", help="List of et event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-tt", dest="tt_mssm_categories", default="8 9", type="string", help="List of tt event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-hbb", dest="hbb_mssm_categories", default="0 1 2 3 4 5 6", type="string", help="List of hbb event categories. [Default: \"0 1 2 3 4 5\"]")
parser.add_option_group(cats2)

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

## switch to sm event categories
if options.analysis == "sm" :
    categories = {
        "ee"   : options.ee_sm_categories.split(),
        "mm"   : options.mm_sm_categories.split(),
        "em"   : options.em_sm_categories.split(),
        "mt"   : options.mt_sm_categories.split(),
        "et"   : options.et_sm_categories.split(),
        "tt"   : options.tt_sm_categories.split(),
        "vhtt" : options.vhtt_sm_categories.split(),
        }

## switch to mssm event categories
if options.analysis == "mssm" :
    categories = {
        "ee"   : options.ee_mssm_categories.split(),
        "mm"   : options.mm_mssm_categories.split(),
        "em"   : options.em_mssm_categories.split(),
        "mt"   : options.mt_mssm_categories.split(),
        "et"   : options.et_mssm_categories.split(),
        "tt"   : options.tt_mssm_categories.split(),
        "hbb"  : options.hbb_mssm_categories.split(),
        }

## configuration for summer13
directories_sm = {
    'em' : {
    '0' : ['0jet', 'dilepton', 'htt', 'cmb'],
    '1' : ['0jet', 'dilepton', 'htt', 'cmb'],
    '2' : ['1jet', 'dilepton', 'htt', 'cmb'],
    '3' : ['1jet', 'dilepton', 'htt', 'cmb'],
    '4' : ['vbf' , 'dilepton', 'htt', 'cmb'],
    '5' : ['vbf' , 'dilepton', 'htt', 'cmb'],
    },
    'et' : {
    '0' : ['0jet', 'htt', 'cmb'],
    '1' : ['0jet', 'htt', 'cmb'],
    '2' : ['0jet', 'htt', 'cmb'],
    '3' : ['1jet', 'htt', 'cmb'],
    '4' : ['1jet', 'htt', 'cmb'],
    '5' : ['1jet', 'htt', 'cmb'],
    '6' : ['vbf' , 'htt', 'cmb'],
    '7' : ['vbf' , 'htt', 'cmb'],
    },
    'mm' : {
    '0' : ['0jet', 'dilepton', 'htt', 'cmb'],
    '1' : ['0jet', 'dilepton', 'htt', 'cmb'],
    '2' : ['1jet', 'dilepton', 'htt', 'cmb'],
    '3' : ['1jet', 'dilepton', 'htt', 'cmb'],
    '4' : ['vbf' , 'dilepton' , 'htt', 'cmb'],
    },
    'ee' : {
    '0' : ['0jet', 'dilepton', 'htt', 'cmb'],
    '1' : ['0jet', 'dilepton', 'htt', 'cmb'],
    '2' : ['1jet', 'dilepton', 'htt', 'cmb'],
    '3' : ['1jet', 'dilepton', 'htt', 'cmb'],
    '4' : ['vbf' , 'dilepton', 'htt', 'cmb'],
    },
    'mt' : {
    '0' : ['0jet', 'htt', 'cmb'],
    '1' : ['0jet', 'htt', 'cmb'],
    '2' : ['0jet', 'htt', 'cmb'],
    '3' : ['1jet', 'htt', 'cmb'],
    '4' : ['1jet', 'htt', 'cmb'],
    '5' : ['1jet', 'htt', 'cmb'],
    '6' : ['vbf' , 'htt', 'cmb'],
    '7' : ['vbf' , 'htt', 'cmb'],
    '10': ['0jet', 'htt', 'cmb', 'mt_soft'],
    '11': ['0jet', 'htt', 'cmb', 'mt_soft'],
    '12': ['0jet', 'htt', 'cmb', 'mt_soft'],
    '13': ['1jet', 'htt', 'cmb', 'mt_soft'],
    '15': ['1jet', 'htt', 'cmb', 'mt_soft'],
    '16': ['vbf' , 'htt', 'cmb', 'mt_soft'],
    },
    'tt' : {
    '0' : ['1jet', 'htt', 'cmb'],
    '1' : ['1jet', 'htt', 'cmb'],
    '2' : ['vbf' , 'htt', 'cmb'],
    },
    'vhtt' :{
    '0' : ['vhtt_wh', 'vhtt', 'cmb'],
    '1' : ['vhtt_wh', 'vhtt', 'cmb'],
    '2' : ['vhtt_wh', 'vhtt', 'cmb'],
    '3' : ['vhtt_zh', 'vhtt', 'cmb'],
    '4' : ['vhtt_zh', 'vhtt', 'cmb'],
    '5' : ['vhtt_zh', 'vhtt', 'cmb'],
    '6' : ['vhtt_zh', 'vhtt', 'cmb'],
    '7' : ['vhtt_wh_had', 'vhtt', 'cmb'],
    '8' : ['vhtt_wh_had', 'vhtt', 'cmb'],
    },
}

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

## determine directories
def directories(channel) :
    if options.analysis == "sm" :
        category_names = directories_sm
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

