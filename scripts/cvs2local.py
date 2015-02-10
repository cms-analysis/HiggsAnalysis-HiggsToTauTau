#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGs",
                      description="This is  a script to copy input files and datacards for limit and significance calculation from cvs to local or to the svn server that is used for the combination of all Higgs decay channels. If the output directory does not already exist a new directory structure will be created (for local copies). ARGs corresponds to a list of integer values resembling the mass points for which you want to copy the datacards. Ranges can be indicated e.g. by: 110-145'. That only any x-th mass point should be taken into account can be indicated e.g. by: 110-145:5. The latter example will pick up the masses 110 115 120 130 135 140 145. Any combination of this syntax is possible.")
parser.add_option("-i", "--in", dest="input", default="auxiliaries/datacards/", type="string",
                  help="Name of the input directory from where to pick up the datacards. [Default: auxiliaries/datacards/]")
parser.add_option("-o", "--out", dest="out", default="ichep2012", type="string",
                  help="Name of the output directory to which the datacards should be copied. [Default: ichep2012]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string",
                  help="List of run periods for which the datacards are to be copied. [Default: \"7TeV 8TeV\"]")
parser.add_option("-a", "--analysis", dest="analysis", default="sm", type="choice",
                  help="Type of analysis (sm or mssm or Hhh or AZh or bbA). Lower case is required. [Default: sm]", choices=["sm", "mssm", "Hhh","AZh", "bbA"])
parser.add_option("-c", "--channels", dest="channels", default="mm em mt et tt", type="string",
                  help="List of channels, for which the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are ee, mm, em, mt, et, tt, vhtt, hmm, hbb. [Default: \"mm em mt et tt\"]")
parser.add_option("-u", "--no-update", dest="no_update", default=False, action="store_true",
                  help="If there are already root files in common, do not recopy them. This should be used by other tools only to speed up copy jobs. [Default: False]")
parser.add_option("--model", dest="model", default="", type="string", help="For some BSM models the dir structure should not be in steps of mass but other parameters. Differences occure for lowmH and 2HDM. [Default: \"\"]")
cats1 = OptionGroup(parser, "SM EVENT CATEGORIES", "Event categories to be picked up for the SM analysis.")
cats1.add_option("--sm-categories-ee", dest="ee_sm_categories", default="0 1 2 3 5", type="string",
                 help="List ee of event categories. [Default: \"0 1 2 3 5\"]")
cats1.add_option("--sm-categories-mm", dest="mm_sm_categories", default="0 1 2 3 4 5", type="string",
                 help="List mm of event categories. [Default: \"0 1 2 3 4 5\"]")
cats1.add_option("--sm-categories-em", dest="em_sm_categories", default="0 1 2 3 4 5", type="string",
                 help="List em of event categories. [Default: \"0 1 2 3 4 5\"]")
cats1.add_option("--sm-categories-mt", dest="mt_sm_categories", default="0 1 2 3 4 5 6 7", type="string",
                 help="List mt of event categories. [Default: \"0 1 2 3 4 5 6 7 \"]")
cats1.add_option("--sm-categories-et", dest="et_sm_categories", default="0 1 2 3 4 5 6 7", type="string",
                 help="List et of event categories. [Default: \"0 1 2 4 3 5 6 7 \"]")
cats1.add_option("--sm-categories-tt", dest="tt_sm_categories", default="0 1 2", type="string",
                 help="List of tt event categories. [Default: \"0 1 2\"]")
cats1.add_option("--sm-categories-th", dest="th_sm_categories", default="0 1", type="string",
                 help="List of th event categories. [Default: \"0 1\"]")
cats1.add_option("--sm-categories-vhtt", dest="vhtt_sm_categories", default="0 1 2", type="string",
                 help="List of vhtt event categories. [Default: \"0 1 2\"]")
cats1.add_option("--sm-categories-vhbb", dest="vhbb_sm_categories", default="0 1 2 3 4 5 6 7 8 9", type="string",
                 help="List of tt event categories. [Default: \"0 1 2 3 4 5 6 7 8 9\"]")
parser.add_option_group(cats1)
cats2 = OptionGroup(parser, "MSSM EVENT CATEGORIES", "Event categories to be used for the MSSM analysis.")
cats2.add_option("--mssm-categories-ee", dest="ee_mssm_categories", default="8 9", type="string",
                 help="List mm of event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-mm", dest="mm_mssm_categories", default="8 9", type="string",
                 help="List mm of event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-em", dest="em_mssm_categories", default="8 9", type="string",
                 help="List em of event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-mt", dest="mt_mssm_categories", default="8 9", type="string",
                 help="List mt of event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-et", dest="et_mssm_categories", default="8 9", type="string",
                 help="List et of event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-tt", dest="tt_mssm_categories", default="8 9", type="string",
                 help="List of tt event categories. [Default: \"8 9\"]")
cats2.add_option("--mssm-categories-hbb", dest="hbb_mssm_categories", default="0 1 2 3 4 5 6", type="string",
                 help="List of hbb event categories. [Default: \"0 1 2 3 4 5 6\"]")
parser.add_option_group(cats2)
cats3 = OptionGroup(parser, "Hhh EVENT CATEGORIES", "Event categories to be used for the Hhh analysis.")
cats3.add_option("--Hhh-categories-ee", dest="ee_Hhh_categories", default="0 1 2", type="string",
                 help="List ee of event categories. [Default: \"0 1 2\"]")
cats3.add_option("--Hhh-categories-mm", dest="mm_Hhh_categories", default="0 1 2", type="string",
                 help="List mm of event categories. [Default: \"0 1 2\"]")
cats3.add_option("--Hhh-categories-em", dest="em_Hhh_categories", default="0 1 2", type="string",
                 help="List em of event categories. [Default: \"0 1 2\"]")
cats3.add_option("--Hhh-categories-mt", dest="mt_Hhh_categories", default="0 1 2", type="string",
                 help="List mt of event categories. [Default: \"0 1 2\"]")
cats3.add_option("--Hhh-categories-et", dest="et_Hhh_categories", default="0 1 2", type="string",
                 help="List et of event categories. [Default: \"0 1 2\"]")
cats3.add_option("--Hhh-categories-tt", dest="tt_Hhh_categories", default="0 1 2", type="string",
                 help="List of tt event categories. [Default: \"0 1 2\"]")
parser.add_option_group(cats3)
cats4 = OptionGroup(parser, "AZh EVENT CATEGORIES", "Event categories to be used for the AZh analysis.")
cats4.add_option("--AZh-categories-AZh", dest="AZh_AZh_categories", default="0 1 2 3", type="string",
                 help="List AZh of event categories. [Default: \"0 1 2 3\"]")
parser.add_option_group(cats4)
cats5 = OptionGroup(parser, "bbA EVENT CATEGORIES", "Event categories to be used for the bbA analysis.")
cats5.add_option("--bbA-categories-mt", dest="mt_bbA_categories", default="0", type="string",
                 help="List mt of bbA event categories. [Default: \"0\"]")
cats5.add_option("--bbA-categories-et", dest="et_bbA_categories", default="0", type="string",
                 help="List mt of bbA event categories. [Default: \"0\"]")
cats5.add_option("--bbA-categories-em", dest="em_bbA_categories", default="0", type="string",
                 help="List mt of bbA event categories. [Default: \"0\"]")
parser.add_option_group(cats5)
parser.add_option("-4", "--SM4", dest="sm4", default=False, action="store_true",
                  help="Copy SM4 datacards (will add a prefix SM4_ to each file). [Default: False]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="Run in verbose mode. [Default: False]")
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs
from HiggsAnalysis.HiggsToTauTau.utils import is_integer
from HiggsAnalysis.HiggsToTauTau.utils import mass_category

## prepare input
input = options.input + "/" + options.analysis
## run periods
periods = options.periods.split()
for idx in range(len(periods)) : periods[idx] = periods[idx].rstrip(',')
## channels
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')
## define prefix for SM4
prefix = "SM4_" if options.sm4 else ""

def massdir(mass):
    massdir = str(mass)
    if '.0' in massdir :
        return massdir.rstrip('0').rstrip('.')
    return massdir

## switch to sm event categories
if options.analysis == "sm" :
    categories = {
        "ee"   : options.ee_sm_categories.split(),
        "mm"   : options.mm_sm_categories.split(),
        "em"   : options.em_sm_categories.split(),
        "mt"   : options.mt_sm_categories.split(),
        "et"   : options.et_sm_categories.split(),
        "tt"   : options.tt_sm_categories.split(),
        "th"   : options.tt_sm_categories.split(),
        "vhtt" : options.vhtt_sm_categories.split(),
        "vhbb" : options.vhbb_sm_categories.split(),
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
        #"hmm"  : options.hmm_mssm_categories.split(),
        "hbb"  : options.hbb_mssm_categories.split(),
        }
if options.analysis == "Hhh" :
    categories = {
        "ee"   : options.ee_Hhh_categories.split(),
        "mm"   : options.mm_Hhh_categories.split(),
        "em"   : options.em_Hhh_categories.split(),
        "mt"   : options.mt_Hhh_categories.split(),
        "et"   : options.et_Hhh_categories.split(),
        "tt"   : options.tt_Hhh_categories.split(),
        }
if options.analysis == "AZh" :
    categories = {
        "AZh"   : options.AZh_AZh_categories.split(),
        }
if options.analysis == "bbA" :
    categories = {
        "mt"   : options.mt_bbA_categories.split(),
        "et"   : options.et_bbA_categories.split(),
        "em"   : options.em_bbA_categories.split(),
        }

## valid mass range per category
if options.analysis == "sm" :
    valid_masses = {
        "ee"   : ( 90, 145),
        "mm"   : ( 90, 145),
        "em"   : ( 90, 145),
        "mt"   : ( 90, 145),
        "et"   : ( 90, 145),
        "tt"   : ( 90, 145),
        "th"   : (125, 125),
        "vhtt" : ( 90, 145),
        "vhbb" : (110, 145),
    }
if options.analysis == "mssm" :
    if options.model=="lowmH" :
        valid_masses = {
            "ee"   : ( 300, 3100),
            "mm"   : ( 300, 3100),
            "em"   : ( 300, 3100),
            "mt"   : ( 300, 3100),
            "et"   : ( 300, 3100),
            "tt"   : ( 300, 3100),
            }
    elif options.model=="2HDM" :
        valid_masses = {
            "ee"   : ( -1, 1),
            "mm"   : ( -1, 1),
            "em"   : ( -1, 1),
            "mt"   : ( -1, 1),
            "et"   : ( -1, 1),
            "tt"   : ( -1, 1),
            }
    else :
        valid_masses = {
            "ee"   : ( 90, 1000),
            "mm"   : ( 90, 1000),
            "em"   : ( 90, 1000),
            "mt"   : ( 90, 1000),
            "et"   : ( 90, 1000),
            "tt"   : ( 90, 1000),
            #"hmm"  : (120,  300),
            "hbb"  : ( 90,  350),
            }
if options.analysis == "AZh" :
    if options.model=="2HDM" :
        valid_masses = {
            "AZh" : (-1,1),
            }
    else :
        valid_masses = {
            "AZh"   : ( 220, 350),
            }
if options.analysis == "bbA" :
       valid_masses = {
            "mt"   : ( 25, 80),
            "et"   : ( 25, 80),
            "em"   : ( 25, 80),
            }
if options.analysis == "Hhh" :
    if options.model=="lowmH" :
        valid_masses = {
            "ee"   : ( 300, 3100),
            "mm"   : ( 300, 3100),
            "em"   : ( 300, 3100),
            "mt"   : ( 300, 3100),
            "et"   : ( 300, 3100),
            "tt"   : ( 300, 3100),
            }
    elif options.model=="2HDM" :
        valid_masses = {
            "ee"   : ( -1, 1),
            "mm"   : ( -1, 1),
            "em"   : ( -1, 1),
            "mt"   : ( -1, 1),
            "et"   : ( -1, 1),
            "tt"   : ( -1, 1),
            }
    else :
        valid_masses = {
            "ee"   : (250, 350),
            "mm"   : (250, 350),
            "em"   : (250, 350),
            "mt"   : (250, 350),
            "et"   : (250, 350),
            "tt"   : (250, 350),
           }

if options.verbose :
    print "------------------------------------------------------"
    print " Valid mass ranges per channel:"
    print "------------------------------------------------------"
    for chn in channels :
        print "chn: ", chn, "valid mass range:", valid_masses[chn]
    print

## valid run periods
if options.analysis == "sm" :
    valid_periods = {
        "ee"   : "7TeV 8TeV 13TeV 14TeV",
        "mm"   : "7TeV 8TeV 13TeV 14TeV",
        "em"   : "7TeV 8TeV 13TeV 14TeV",
        "mt"   : "7TeV 8TeV 13TeV 14TeV",
        "et"   : "7TeV 8TeV 13TeV 14TeV",
        "tt"   :      "8TeV 13TeV 14TeV",
        "th"   :      "8TeV 13TeV 14TeV",
        "vhtt" : "7TeV 8TeV 13TeV 14TeV",
        "vhbb" : "7TeV 8TeV 13TeV 14TeV",
        }
if options.analysis == "mssm" :
    valid_periods = {
        "ee"   : "7TeV 8TeV 13TeV 14TeV",
        "mm"   : "7TeV 8TeV 13TeV 14TeV",
        "em"   : "7TeV 8TeV 13TeV 14TeV",
        "mt"   : "7TeV 8TeV 13TeV 14TeV",
        "et"   : "7TeV 8TeV 13TeV 14TeV",
        "tt"   :      "8TeV 13TeV 14TeV",
        #"hmm"  : "7TeV"     ,
        "hbb"  : "7TeV"     ,
        }
if options.analysis == "Hhh" :
    valid_periods = {
        "ee"   : "7TeV 8TeV",
        "mm"   : "7TeV 8TeV",
        "em"   : "7TeV 8TeV",
        "mt"   : "7TeV 8TeV",
        "et"   : "7TeV 8TeV",
        "tt"   :      "8TeV",
        }
if options.analysis == "AZh" :
    valid_periods = {
        "AZh"   : "8TeV",
    }
if options.analysis == "bbA" :
    valid_periods = {
        "mt"   : "8TeV",
        "et"   : "8TeV",
        "em"   : "8TeV",
    }

if options.verbose :
    print "------------------------------------------------------"
    print " Valid mass run periods per channel:"
    print "------------------------------------------------------"
    for chn in channels :
        print "chn: ", chn, "valid run periods:", valid_periods[chn]
    print
    print "copy datacards for:", options.analysis, options.channels, options.periods

## setup directory structure in case it does not exist, yet
if not os.path.exists(options.out) :
    os.system("mkdir {OUTPUT}".format(OUTPUT=options.out))
if not os.path.exists("{OUTPUT}/common".format(OUTPUT=options.out)) :
    os.system("mkdir {OUTPUT}/common".format(OUTPUT=options.out))
for mass in parseArgs(args) :
    if not os.path.exists("{OUTPUT}/{MASSDIR}".format(OUTPUT=options.out, MASSDIR=massdir(mass))) :
        os.system("mkdir {OUTPUT}/{MASSDIR}".format(OUTPUT=options.out, MASSDIR=massdir(mass)))

for period in periods :
    for channel in channels :
        for mass in parseArgs(args) :
            ## check validity of run period
            if not period in valid_periods[channel] :
                #print "drop due to failing period: ", channel, valid_periods[channel], period
                continue
            ## check validity of mass
            if (float(mass)< valid_masses[channel][0] or float(mass)> valid_masses[channel][1]) :
                #print "drop due to failing mass:" , channel, valid_masses[channel][0], valid_masses[channel][1], ":", mass
                continue
            if channel == "vhbb" or channel == "hmm" or channel == "hbb" :
                for category in categories[channel] :
                    if options.verbose :
                        print "copying datacards for:", period, channel, category, mass
                    if options.analysis == "mssm" :
                        os.system("cp {INPUT}/{CHN}/{PRE}{CHN}.inputs-{ANA}-{PERIOD}-{MASSCAT}.root* {OUTPUT}/common".format(
                            INPUT=input, ANA=options.analysis, CHN=channel, OUTPUT=options.out, PRE=prefix, PERIOD=period, MASSCAT=mass_category(mass,category, channel)))
                        os.system("cp {INPUT}/{CHN}/{CHN}_{CAT}_{PERIOD}-{MASS}.txt {OUTPUT}/{MASSDIR}/{PRE}{CHN}_{CAT}_{PERIOD}.txt".format(
                            INPUT=input, CHN=channel, CAT=category, PERIOD=period, MASS='100' if options.model=='lowmH' or options.model=='2HDM' else mass, MASSDIR=massdir(mass), OUTPUT=options.out, PRE=prefix))
                        os.system("perl -pi -e 's/{CHN}.inputs/..\/common\/{PRE}{CHN}.inputs/g' {OUTPUT}/{MASSDIR}/{PRE}{CHN}_{CAT}_{PERIOD}.txt".format(
                            CHN=channel, ANA=options.analysis, PRE=prefix, OUTPUT=options.out, MASS=mass, MASSDIR=massdir(mass), CAT=category, PERIOD=period, MASSCAT=mass_category(mass,category,channel)))
                    else :
                        os.system("cp {INPUT}/{CHN}/{CHN}.inputs-{ANA}-{PERIOD}.root {OUTPUT}/common/{PRE}{CHN}.input_{PERIOD}.root".format(
                            INPUT=input, ANA=options.analysis, CHN=channel, OUTPUT=options.out, PRE=prefix, PERIOD=period))
                        os.system("cp {INPUT}/{CHN}/{CHN}_{CAT}_{PERIOD}-{MASS}.txt {OUTPUT}/{MASSDIR}/{PRE}{CHN}_{CAT}_{PERIOD}.txt".format(
                            INPUT=input, CHN=channel, CAT=category, PERIOD=period, MASS='300' if options.model=='lowmH' or options.model=='2HDM' else mass, MASSDIR=massdir(mass), OUTPUT=options.out, PRE=prefix))
                        os.system("perl -pi -e 's/{CHN}.inputs-{ANA}-{PERIOD}.root/..\/common\/{PRE}{CHN}.input_{PERIOD}.root/g' {OUTPUT}/{MASSDIR}/{PRE}{CHN}_{CAT}_{PERIOD}.txt".format(
                            CHN=channel, ANA=options.analysis, PRE=prefix, OUTPUT=options.out, MASS=mass, MASSDIR=massdir(mass), CAT=category, PERIOD=period))
            elif channel == "vhtt":
                for category in categories[channel] :
                    if options.verbose :
                        print "copying datacards for:", period, channel, category, mass
                    os.system("cp {INPUT}/{CHN}/{CHN}.inputs-{ANA}-{PERIOD}.root {OUTPUT}/common/{PRE}{CHN}.input_{PERIOD}.root".format(
                        INPUT=input, ANA=options.analysis, CHN=channel, OUTPUT=options.out, PRE=prefix, PERIOD=period, MASSCAT=mass_category(mass,category, channel)))
                    os.system("cp {INPUT}/{CHN}/{CHN}_{CAT}_{PERIOD}-{MASS}.txt {OUTPUT}/{MASSDIR}/{PRE}{CHN}_{CAT}_{PERIOD}.txt".format(
                        INPUT=input, CHN=channel, CAT=category, PERIOD=period, MASS=mass, MASSDIR=massdir(mass), OUTPUT=options.out, PRE=prefix))
                    os.system("perl -pi -e 's/{CHN}.inputs-{ANA}-{PERIOD}.root/..\/common\/{PRE}{CHN}.input_{PERIOD}.root/g' {OUTPUT}/{MASSDIR}/{PRE}{CHN}_{CAT}_{PERIOD}.txt".format(
                        CHN=channel, ANA=options.analysis, PRE=prefix, OUTPUT=options.out, MASS=mass, MASSDIR=massdir(mass), CAT=category, PERIOD=period, MASSCAT=mass_category(mass,category,channel)))
            else :
                for category in categories[channel] :
                    if options.verbose :
                        print "copying datacards for:", period, channel, category, mass
                    ## check validity of run period
                    if not period in valid_periods[channel] :
                        #print "drop due to failing period: ", channel, valid_periods[channel], period
                        continue
                    ## check validity of mass
                    if (float(mass)< valid_masses[channel][0] or float(mass)> valid_masses[channel][1]) :
                        #print "drop due to failing mass:" , channel, valid_masses[channel][0], valid_masses[channel][1], ":", mass
                        continue
                    if options.analysis == "mssm" :
                        if options.no_update:
                            files = ' '.join(os.listdir("{OUTPUT}/common/".format(OUTPUT=options.out)))
                            if not "htt_"+channel+'.inputs-mssm-'+period in files :
                                os.system("cp {INPUT}/htt_{CHN}/{PRE}htt_{CHN}.inputs-{ANA}-{PERIOD}-{MASSCAT}.root* {OUTPUT}/common/".format(
                                    INPUT=input, CHN=channel, ANA=options.analysis, PERIOD=period, OUTPUT=options.out, PRE=prefix, MASSCAT=mass_category(mass,category, channel)))
                            else :
                                pass
                                #print "no update of files needed."
                        else :
                            os.system("cp {INPUT}/htt_{CHN}/{PRE}htt_{CHN}.inputs-{ANA}-{PERIOD}-{MASSCAT}.root* {OUTPUT}/common/".format(
                                INPUT=input, CHN=channel, ANA=options.analysis, PERIOD=period, OUTPUT=options.out, PRE=prefix, MASSCAT=mass_category(mass,category, channel)))
                        os.system("cp {INPUT}/htt_{CHN}/htt_{CHN}_{CAT}_{PERIOD}-{MASS}.txt {OUTPUT}/{MASSDIR}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            INPUT=input, CHN=channel, CAT=category, PERIOD=period, MASS='100' if options.model=='lowmH' or options.model=='2HDM' else mass, MASSDIR=massdir(mass), OUTPUT=options.out, PRE=prefix))
                        os.system("perl -pi -e 's/htt_{CHN}.inputs/..\/common\/{PRE}htt_{CHN}.inputs/g' {OUTPUT}/{MASSDIR}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            CHN=channel, PRE=prefix, OUTPUT=options.out, MASS=mass, MASSDIR=massdir(mass), CAT=category, PERIOD=period))
                    else :
                        if options.no_update:
                            files = ' '.join(os.listdir("{OUTPUT}/common/".format(OUTPUT=options.out)))
                            if not "htt_"+channel+'.input_'+period in files :
                                os.system("cp {INPUT}/htt_{CHN}/htt_{CHN}.inputs-{ANA}-{PERIOD}.root {OUTPUT}/common/{PRE}htt_{CHN}.input_{PERIOD}.root".format(
                                    INPUT=input, CHN=channel, ANA=options.analysis, OUTPUT=options.out, PRE=prefix, PERIOD=period))
                            else :
                                if not period in files:
                                    os.system("cp {INPUT}/htt_{CHN}/htt_{CHN}.inputs-{ANA}-{PERIOD}.root {OUTPUT}/common/{PRE}htt_{CHN}.input_{PERIOD}.root".format(
                                        INPUT=input, CHN=channel, ANA=options.analysis, OUTPUT=options.out, PRE=prefix, PERIOD=period))
                                else :
                                    pass
                                    #print "no update of files needed."
                        else :
                            os.system("cp {INPUT}/htt_{CHN}/htt_{CHN}.inputs-{ANA}-{PERIOD}.root {OUTPUT}/common/{PRE}htt_{CHN}.input_{PERIOD}.root".format(
                                INPUT=input, CHN=channel, ANA=options.analysis, OUTPUT=options.out, PRE=prefix, PERIOD=period))
                        os.system("cp {INPUT}/htt_{CHN}/htt_{CHN}_{CAT}_{PERIOD}-{MASS}.txt {OUTPUT}/{MASSDIR}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            INPUT=input, CHN=channel, CAT=category, PERIOD=period, MASS='300' if options.model=='lowmH' or options.model=='2HDM' else mass, MASSDIR=massdir(mass), OUTPUT=options.out, PRE=prefix))
                        os.system("perl -pi -e 's/htt_{CHN}.inputs-{ANA}-{PERIOD}.root/..\/common\/{PRE}htt_{CHN}.input_{PERIOD}.root/g' {OUTPUT}/{MASSDIR}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            CHN=channel, ANA=options.analysis, PRE=prefix, OUTPUT=options.out, MASS=mass, MASSDIR=massdir(mass), CAT=category, PERIOD=period))

