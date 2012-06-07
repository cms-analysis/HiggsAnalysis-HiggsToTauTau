#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to copy input files and datacards for limit and significance calculation from cvs to local or to the svn server that is used for the combination of all Higgs decay channels. If the output directory is does not already exist a new directory structure will be created (for local copies). ARGS corresponds to a list of integer values resembling the mass points for which you want to copy the datacards. Ranges can be indicated e.g. by: 110-145'. That only any x-th mass point should be taken into account can be indicated e.g. by: 110-145:5. The latter example will pick up the masses 110 115 120 130 135 140 145. Any combination of this syntax is possible.")
parser.add_option("-i", "--in", dest="input", default="UserCode/HiggsAnalysis/HiggsToTauTau/datacards/sm", type="string", help="Name of the input directory from where to pick up the datacards. [Default: UserCode/HiggsAnalysis/HiggsToTauTau/datacards/sm]")
parser.add_option("-o", "--out", dest="out", default="ichep2012", type="string", help="Name of the output directory to which the datacards should be copied. [Default: ichep2012]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string", help="List of run periods for which the datacards are to be copied. [Default: \"7TeV 8TeV\"]")
parser.add_option("-a", "--analysis", dest="analysis", default="sm", type="choice", help="Type of analysis (sm or mssm). Lower case is required. [Default: sm]", choices=["sm", "mssm"])
parser.add_option("-c", "--channels", dest="channels", default="mm em mt et", type="string", help="List of channels, for whch the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt. [Default: \"mm em mt et\"]")
cats1 = OptionGroup(parser, "SM EVENT CATEGORIES", "Event categories to be picked up for the SM analysis.")
cats1.add_option("--sm-categories-mm", dest="mm_sm_categories", default="0 1 2 3 4 5", type="string", help="List mm of event categories. [Default: \"0 1 2 3 4 5\"]")
cats1.add_option("--sm-categories-em", dest="em_sm_categories", default="0 1 2 3 4 5", type="string", help="List em of event categories. [Default: \"0 1 2 3 4 5\"]")
cats1.add_option("--sm-categories-mt", dest="mt_sm_categories", default="0 1 2 3 4 5", type="string", help="List mt of event categories. [Default: \"0 1 2 3 4 5\"]")
cats1.add_option("--sm-categories-et", dest="et_sm_categories", default="0 1 2 3 4 5", type="string", help="List et of event categories. [Default: \"0 1 2 3 4 5\"]")
cats1.add_option("--sm-categories-tt", dest="tt_sm_categories", default="0 1", type="string", help="List of tt event categories. [Default: \"0 1\"]")
cats1.add_option("--sm-categories-vhtt", dest="vhtt_sm_categories", default="0 1 2", type="string", help="List of tt event categories. [Default: \"0 1 2\"]")
parser.add_option_group(cats1)
cats2 = OptionGroup(parser, "MSSM EVENT CATEGORIES", "Event categories to be used for the MSSM analysis.")
cats2.add_option("--mssm-categories-mm", dest="mm_mssm_categories", default="0 1 2 3 6 7", type="string", help="List mm of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-em", dest="em_mssm_categories", default="0 1 2 3 6 7", type="string", help="List em of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-mt", dest="mt_mssm_categories", default="0 1 2 3 6 7", type="string", help="List mt of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-et", dest="et_mssm_categories", default="0 1 2 3 6 7", type="string", help="List et of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-tt", dest="tt_mssm_categories", default="0 1", type="string", help="List of tt event categories. [Default: \"0 1\"]")
cats2.add_option("--mssm-categories-hmm", dest="hmm_mssm_categories", default="0 1", type="string", help="List of hmm event categories. [Default: \"0 1\"]")
parser.add_option_group(cats2)
parser.add_option("-4", "--SM4", dest="sm4", default=False, action="store_true", help="Copy SM4 datacards (will add a prefix SM4_ to each file). [Default: False]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Run in verbose mode. [Default: False]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

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

## switch to sm event categories
if options.analysis == "sm" :
    categories = {
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
        "mm"   : options.mm_mssm_categories.split(),
        "em"   : options.em_mssm_categories.split(),
        "mt"   : options.mt_mssm_categories.split(),
        "et"   : options.et_mssm_categories.split(),
        "tt"   : options.tt_mssm_categories.split(),
        "hmm"  : options.hmm_mssm_categories.split(),
        }
    
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
            if channel == "vhtt" :
                for category in categories[channel] :
                    if options.verbose :
                        print "copying datacards for:", period, channel, category, mass
                    if period == "8TeV" :
                        continue
                    os.system("cp {INPUT}/{CHN}/vhtt_{CAT}.input_{PERIOD}.root {OUTPUT}/common/{PRE}vhtt_{CAT}.input_{PERIOD}.root".format(
                        INPUT=input, CAT=category, CHN=channel, OUTPUT=options.out, PRE=prefix, PERIOD=period))                        
                    os.system("cp {INPUT}/{CHN}/vhtt_{CAT}_{PERIOD}-{MASS}.txt {OUTPUT}/{MASS}/{PRE}vhtt_{CAT}_{PERIOD}.txt".format(
                        INPUT=input, CHN=channel, CAT=category, PERIOD=period, MASS=mass, OUTPUT=options.out, PRE=prefix))
                    os.system("perl -pi -e 's/cards\/vhtt_{CAT}.input_{PERIOD}.root/..\/common\/{PRE}vhtt_{CAT}.input_{PERIOD}.root/g' {OUTPUT}/{MASS}/{PRE}vhtt_{CAT}_{PERIOD}.txt".format(
                        CAT=category, PRE=prefix, OUTPUT=options.out, MASS=mass, PERIOD=period))
            else :
                for category in categories[channel] :
                    ## special treatment for incomplete 8TeV samples:
                    ## here only mH=115 is considered for mm/em/mt/et
                    ## and mH=125 for tt, vhtt misses completely.
                    single_mass = "125" if channel == "tt" else "115"
                    if channel == "vhtt" and period == "8TeV" :
                        continue
                    if options.verbose :
                        print "copying datacards for:", period, channel, category, mass
                    if period == "8TeV" :
                        os.system("cp {INPUT}/htt_{CHN}/htt_{CHN}.inputs-{period}.root {OUTPUT}/common/{PRE}htt_{CHN}.input_{PERIOD}.root".format(
                            INPUT=input, CHN=channel, period=period.lower(), OUTPUT=options.out, PRE=prefix, PERIOD=period))                        
                        os.system("cp {INPUT}/htt_{CHN}/htt_{CHN}_{CAT}_{PERIOD}-{BYPASS}.txt {OUTPUT}/{MASS}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            INPUT=input, CHN=channel, CAT=category, PERIOD=period, BYPASS=single_mass, MASS=mass, OUTPUT=options.out, PRE=prefix))
                        os.system("perl -pi -e 's/htt_{CHN}.inputs-{period}.root/..\/common\/{PRE}htt_{CHN}.input_{PERIOD}.root/g' {OUTPUT}/{MASS}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            CHN=channel, period=period.lower(), PRE=prefix, OUTPUT=options.out, MASS=mass, CAT=category, PERIOD=period))
                    else :
                        os.system("cp {INPUT}/htt_{CHN}/htt_{CHN}.inputs-{period}.root {OUTPUT}/common/{PRE}htt_{CHN}.input_{PERIOD}.root".format(
                            INPUT=input, CHN=channel, period=period.lower(), OUTPUT=options.out, PRE=prefix, PERIOD=period))                        
                        os.system("cp {INPUT}/htt_{CHN}/htt_{CHN}_{CAT}_{PERIOD}-{MASS}.txt {OUTPUT}/{MASS}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            INPUT=input, CHN=channel, CAT=category, PERIOD=period, MASS=mass, OUTPUT=options.out, PRE=prefix))
                        os.system("perl -pi -e 's/htt_{CHN}.inputs-{period}.root/..\/common\/{PRE}htt_{CHN}.input_{PERIOD}.root/g' {OUTPUT}/{MASS}/{PRE}htt_{CHN}_{CAT}_{PERIOD}.txt".format(
                            CHN=channel, period=period.lower(), PRE=prefix, OUTPUT=options.out, MASS=mass, CAT=category, PERIOD=period))


## for later use for mssm data cards

## add mass point to the list of available masses per channel
#def add_mass(channel, mass) :
#    if not channel in channel_to_mass :
#        channel_to_mass[channel] = "%s :  " % channel
#    channel_to_mass[channel]+= "  %s  " % mass

#if options.channel.find("mssm")>-1 :
#    ## open masses.vals. Append if it exists already, create otherwise
#    if os.path.exists("{pwd}/{output}/common/masses.vals".format(pwd=os.getcwd(), output=options.out)) :
#        masses = open("{pwd}/{output}/common/masses.vals".format(pwd=os.getcwd(), output=options.out), 'a')
#    else :
#        masses = open("{pwd}/{output}/common/masses.vals".format(pwd=os.getcwd(), output=options.out), 'w')

#    ## write channel-mass strings to masses.vals
#    for channel in channel_to_mass :
#        masses.write(channel_to_mass[channel]+"\n")
#    masses.close()
#    ## distribute file across all mass points
#    #for mass in args : 
#    #    os.system("cp {output}/common/masses.vals {output}/{mass}/".format(output=options.out, mass=mass))
