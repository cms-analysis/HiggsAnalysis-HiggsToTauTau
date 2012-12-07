#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to copy input files and datacards for limit and significance calculation from cvs to local or to the svn server that is used for the combination of all Higgs decay channels. If the output directory is does not already exist a new directory structure will be created (for local copies). ARGS corresponds to a list of integer values resembling the mass points for which you want to copy the datacards. Ranges can be indicated e.g. by: 110-145'. That only any x-th mass point should be taken into account can be indicated e.g. by: 110-145:5. The latter example will pick up the masses 110 115 120 130 135 140 145. Any combination of this syntax is possible.")
parser.add_option("-i", "--in", dest="input", default="auxiliaries/datacards/", type="string", help="Name of the input directory from where to pick up the datacards. [Default: auxiliaries/datacards/]")
parser.add_option("-o", "--out", dest="out", default="ichep2012", type="string", help="Name of the output directory to which the datacards should be copied. [Default: ichep2012]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string", help="List of run periods for which the datacards are to be copied. [Default: \"7TeV 8TeV\"]")
parser.add_option("-a", "--analysis", dest="analysis", default="sm", type="choice", help="Type of analysis (sm or mssm). Lower case is required. [Default: sm]", choices=["sm", "mssm"])
parser.add_option("-c", "--channels", dest="channels", default="mm em mt et", type="string", help="List of channels, for whch the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt, hmm, bbhad, bblep. [Default: \"mm em mt et\"]")
parser.add_option("-u", "--no-update", dest="no_update", default=False, action="store_true", help="If there are already root file in common, do not recopy them. This should be used by other tools only to speed up copy jobs. [Default: False]")
cats1 = OptionGroup(parser, "SM EVENT CATEGORIES", "Event categories to be picked up for the SM analysis.")
cats1.add_option("--sm-categories-mm", dest="mm_sm_categories", default="0 1 2 3 5", type="string", help="List mm of event categories. [Default: \"0 1 2 3 5\"]")
cats1.add_option("--sm-categories-em", dest="em_sm_categories", default="0 1 2 3 5", type="string", help="List em of event categories. [Default: \"0 1 2 3 5\"]")
cats1.add_option("--sm-categories-mt", dest="mt_sm_categories", default="0 1 2 3 5", type="string", help="List mt of event categories. [Default: \"0 1 2 3 5\"]")
cats1.add_option("--sm-categories-et", dest="et_sm_categories", default="0 1 2 3 5", type="string", help="List et of event categories. [Default: \"0 1 2 3 5\"]")
cats1.add_option("--sm-categories-tt", dest="tt_sm_categories", default="0 1", type="string", help="List of tt event categories. [Default: \"0 1\"]")
cats1.add_option("--sm-categories-vhtt", dest="vhtt_sm_categories", default="0 1", type="string", help="List of vhtt event categories. [Default: \"0 1\"]")
cats1.add_option("--sm-categories-vhbb", dest="vhbb_sm_categories", default="0 1 2 3 4 5 6 7 8 9", type="string", help="List of tt event categories. [Default: \"0 1 2 3 4 5 6 7 8 9\"]")
parser.add_option_group(cats1)
cats2 = OptionGroup(parser, "MSSM EVENT CATEGORIES", "Event categories to be used for the MSSM analysis.")
cats2.add_option("--mssm-categories-mm", dest="mm_mssm_categories", default="8 9", type="string", help="List mm of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-em", dest="em_mssm_categories", default="8 9", type="string", help="List em of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-mt", dest="mt_mssm_categories", default="8 9", type="string", help="List mt of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-et", dest="et_mssm_categories", default="8 9", type="string", help="List et of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-tt", dest="tt_mssm_categories", default="0 1", type="string", help="List of tt event categories. [Default: \"0 1\"]")
cats2.add_option("--mssm-categories-hmm", dest="hmm_mssm_categories", default="0 1", type="string", help="List of hmm event categories. [Default: \"0 1\"]")
parser.add_option_group(cats2)
parser.add_option("-4", "--SM4", dest="sm4", default=False, action="store_true", help="Copy SM4 datacards (will add a prefix SM4_ to each file). [Default: False]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Run in verbose mode. [Default: False]")
cats2.add_option("--mssm-categories-bbhad", dest="bbhad_mssm_categories", default="0 1 2 3 4 5", type="string", help="List of hbb event categories. [Default: \"0 1 2 3 4 5\"]")
cats2.add_option("--mssm-categories-bblep", dest="bblep_mssm_categories", default="0", type="string", help="List of hbb event categories. [Default: \"0\"]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs
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

## add mass point to the list of available masses per channel
def add_mass(channel, mass) :
    """
    add a mass point for a corresponding channel to communicate, which mass points
    do exist for which decay channel.
    """
    ## map of channel to available masses
    channel_to_mass = {}
    ## map out already available channels and masses
    if os.path.exists("{OUTPUT}/common/masses.vals".format(OUTPUT=options.out)) :
        input  = open("{OUTPUT}/common/masses.vals".format(OUTPUT=options.out), 'r')
        for line in input :
            words = line.split()
            channel_to_mass[words[0]] = words
        input.close()
    ## check for the presence of a given channel and mass and depending on that
    ## append to the list or create a new entry
    CHANNEL_EXISTS = False
    for existing_channel, existing_masses in channel_to_mass.iteritems() :
        if existing_channel == channel :
            CHANNEL_EXISTS = True
        MASS_EXISTS = False
        for existing_mass in existing_masses :
            if not existing_mass.isdigit() :
                continue
            if int(existing_mass) == mass :
                MASS_EXISTS = True
        if not MASS_EXISTS :
            channel_to_mass[existing_channel].append(str(mass))
    if not CHANNEL_EXISTS :
        channel_to_mass[channel] = [channel, str(mass)]
    ## putting everything together again and fan out
    update = open("{OUTPUT}/common/masses.vals".format(OUTPUT=options.out), 'w')
    for chn in channel_to_mass :
        line = '\t'.join(channel_to_mass[chn])+'\n'
        update.write(line)
    update.close()

## switch to sm event categories
if options.analysis == "sm" :
    categories = {
        "mm"   : options.mm_sm_categories.split(),
        "em"   : options.em_sm_categories.split(),
        "mt"   : options.mt_sm_categories.split(),
        "et"   : options.et_sm_categories.split(),
        "tt"   : options.tt_sm_categories.split(),
        "vhtt" : options.vhtt_sm_categories.split(),
        "vhbb" : options.vhbb_sm_categories.split(),
        }
## switch to mssm event categories
if options.analysis == "mssm" :
    categories = {
        "mm"   : options.mm_mssm_categories.split(),
        "em"   : options.em_mssm_categories.split(),
        "mt"   : options.mt_mssm_categories.split(),
        "et"   : options.et_mssm_categories.split(),
        "tt"   : options.tt_mssm_categories.split(),
        "hmm"  : options.hmm_mssm_categories.split(),
        "bbhad": options.bbhad_mssm_categories.split(),
        "bblep": options.bblep_mssm_categories.split(),
        }

## valid mass range per category
if options.analysis == "sm" :
    valid_masses = {
        "mm"   : (110, 145),
        "em"   : (110, 145),
        "mt"   : (110, 145),
        "et"   : (110, 145),
        "tt"   : (110, 145),
        "vhtt" : (110, 145),
        "vhbb" : (110, 145),
    }
if options.analysis == "mssm" :
    valid_masses = {
        "mm"   : ( 90, 1000),
        "em"   : ( 90, 1000),
        "mt"   : ( 90, 1000),
        "et"   : ( 90, 1000),
        "tt"   : ( 90,  500),
        "hmm"  : (120,  300),
        "bbhad": ( 90,  350),
        "bblep": ( 90,  350),       
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
        "mm"   : "7TeV 8TeV 14TeV",
        "em"   : "7TeV 8TeV 14TeV",
        "mt"   : "7TeV 8TeV 14TeV",
        "et"   : "7TeV 8TeV 14TeV",
        "tt"   :      "8TeV 14TeV",
        "vhtt" : "7TeV 8TeV 14TeV",
        "vhbb" : "7TeV 8TeV 14TeV",
        }
if options.analysis == "mssm" :
    valid_periods = {
        "mm"   : "7TeV 8TeV",
        "em"   : "7TeV 8TeV",
        "mt"   : "7TeV 8TeV",
        "et"   : "7TeV 8TeV",
        "tt"   :      "8TeV",
        "hmm"  : "7TeV"     ,
        "bbhad": "7TeV"     ,
        "bblep": "7TeV"     ,
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
    if not os.path.exists("{OUTPUT}/{MASS}".format(OUTPUT=options.out, MASS=mass)) :
        os.system("mkdir {OUTPUT}/{MASS}".format(OUTPUT=options.out, MASS=mass))

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
            if channel == "vhtt" or channel == "vhbb" or channel == "hmm" :
                for category in categories[channel] :
                    if options.verbose :
                        print "copying datacards for:", period, channel, category, mass
                    os.system("cp {INPUT}/{CHN}/{CHN}.inputs-{ANA}-{PERIOD}*.root {OUTPUT}/common/{PRE}{CHN}.input_{PERIOD}*.root".format(
                        INPUT=input, ANA=options.analysis, CHN=channel, OUTPUT=options.out, PRE=prefix, PERIOD=period))
                    os.system("cp {INPUT}/{CHN}/{CHN}_{CAT}_{PERIOD}-{MASS}.txt {OUTPUT}/{MASS}/{PRE}{CHN}_{CAT}_{PERIOD}.txt".format(
                        INPUT=input, CHN=channel, CAT=category, PERIOD=period, MASS=mass, OUTPUT=options.out, PRE=prefix))
                    os.system("perl -pi -e 's/{CHN}.inputs-{ANA}-{PERIOD}*.root/..\/common\/{PRE}{CHN}.input_{PERIOD}*.root/g' {OUTPUT}/{MASS}/{PRE}{CHN}_{CAT}_{PERIOD}.txt".format(
                        CHN=channel, ANA=options.analysis, PRE=prefix, OUTPUT=options.out, MASS=mass, CAT=category, PERIOD=period))
                    if options.analysis == "mssm" :
                        add_mass("{CHN}_{CAT}_{PERIOD}".format(CHN=channel, CAT=category, PERIOD=period), mass)
            elif channel == "bbhad" or channel == "bblep":
                for category in categories[channel] :
                    if options.verbose :
                        print "copying datacards for:", period, channel, category, mass
                    os.system("cp {INPUT}/hbb_{CHN}/hbb_{CHN}.inputs-{ANA}-{PERIOD}*root {OUTPUT}/common/{PRE}hbb_{CHN}.input_{PERIOD}*.root".format(
                        INPUT=input, ANA=options.analysis, CHN=channel, OUTPUT=options.out, PRE=prefix, PERIOD=period))
                    os.system("cp {INPUT}/hbb_{CHN}/hbb_{CHN}_{CAT}_{PERIOD}-{MASS}.txt {OUTPUT}/{MASS}/{PRE}hbb_{CHN}_{CAT}_{PERIOD}.txt".format(
                        INPUT=input, CHN=channel, CAT=category, PERIOD=period, MASS=mass, OUTPUT=options.out, PRE=prefix))
                    os.system("perl -pi -e 's/hbb_{CHN}.inputs-{ANA}-{PERIOD}*.root/..\/common\/{PRE}hbb_{CHN}.input_{PERIOD}*.root/g' {OUTPUT}/{MASS}/{PRE}hbb_{CHN}_{CAT}_{PERIOD}.txt".format(
                        CHN=channel, ANA=options.analysis, PRE=prefix, OUTPUT=options.out, MASS=mass, CAT=category, PERIOD=period))
                    if options.analysis == "mssm" :
                        add_mass("hbb_{CHN}_{CAT}_{PERIOD}".format(CHN=channel, CAT=category, PERIOD=period), mass)
            else :
                for category in categories[channel] :
                    if options.verbose :
                        print "copying datacards for:", period, channel, category, mass
                    if options.analysis == "mssm" :
                        add_mass("htt_{CHN}_{CAT}_{PERIOD}".format(CHN=channel, CAT=category, PERIOD=period), mass)
                        if options.no_update:
                            files = ' '.join(os.listdir("{OUTPUT}/common/".format(OUTPUT=options.out)))
                            if not "htt_"+channel+'.inputs-mssm-'+period in files :
                                os.system("cp {INPUT}/htt_{CHN}/{PRE}htt_{CHN}.inputs-{ANA}-{PERIOD}*.root {OUTPUT}/common/".format(
                                    INPUT=input, CHN=channel, ANA=options.analysis, PERIOD=period, OUTPUT=options.out, PRE=prefix))
                            else :
                                pass
                                #print "no update of files needed."
                        else :
                            os.system("cp {INPUT}/htt_{CHN}/{PRE}htt_{CHN}.inputs-{ANA}-{PERIOD}*.root {OUTPUT}/common/".format(
                                INPUT=input, CHN=channel, ANA=options.analysis, PERIOD=period, OUTPUT=options.out, PRE=prefix))
                        os.system("cp {INPUT}/htt_{CHN}/htt_{CHN}_{CAT}_{PERIOD}-{MASS}.txt {OUTPUT}/{MASS}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            INPUT=input, CHN=channel, CAT=category, PERIOD=period, MASS=mass, OUTPUT=options.out, PRE=prefix))
                        os.system("perl -pi -e 's/htt_{CHN}.inputs/..\/common\/{PRE}htt_{CHN}.inputs/g' {OUTPUT}/{MASS}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            CHN=channel, PRE=prefix, OUTPUT=options.out, MASS=mass, CAT=category, PERIOD=period))
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
                        os.system("cp {INPUT}/htt_{CHN}/htt_{CHN}_{CAT}_{PERIOD}-{MASS}.txt {OUTPUT}/{MASS}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            INPUT=input, CHN=channel, CAT=category, PERIOD=period, MASS=mass, OUTPUT=options.out, PRE=prefix))
                        os.system("perl -pi -e 's/htt_{CHN}.inputs-{ANA}-{PERIOD}.root/..\/common\/{PRE}htt_{CHN}.input_{PERIOD}.root/g' {OUTPUT}/{MASS}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            CHN=channel, ANA=options.analysis, PRE=prefix, OUTPUT=options.out, MASS=mass, CAT=category, PERIOD=period))
