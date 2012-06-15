#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to setup the limit calculation for htt. The script relies on the machienery of automatic datacard creation detailed in the setup directory of this package. Apart from options there is no further argument for this script.")
parser.add_option("-n", "--name", dest="name", default="xxxx-test", type="string", help="Name of the working directory. The tool will create two subdirectories mssm and sm, in which it will create subdirectories for all masspoints available for the analysis [Default: xxxx-test]")
parser.add_option("--sm-masses", dest="sm_masses", default="110 115 120 125 130 135 140 145", type="string", help="Available SM mass points [Default: 110 115 120 125 130 135 140 145]")
parser.add_option("--mssm-masses", dest="mssm_masses", default="90 100 120 130 140 160 180 200 250 300 350 400 450 500", type="string", help="Available MSSM mass points [Default: 90 100 120 130 140 160 180 200 250 300 350 400 450 500]")
parser.add_option("--analysis", dest="analysis", default="all", type="choice", help="Choose between sm or mssm analysis [Default: all]", choices=["sm", "mssm", "all"])
parser.add_option("--category", dest="category", default="all", type="choice", help="Choose between event categories (depending on analysis) [Default: all]", choices=["cmb", "0jet", "btag", "boost", "2jet", "vbf", "all"])
parser.add_option("--channel", dest="channel", default="all", type="choice", help="Choose between ditau decay channels [Default: all]", choices=["all", "cmb", "mm", "em", "et", "mt", "tt", "hmm", "vhtt_had"])
parser.add_option("--period", dest="period", default="all", type="choice", help="Choose between run periods [Default: all]", choices=["7TeV", "8TeV", "all"])
parser.add_option("--drop-channels", dest="drop",default="", type="string", help="Scale the given channels to 0. in the datacards. (This action will be applied to all channels that match the given string patterns, which may be on as a whitespace or ',' separated list). [Default: \"\"]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os

## create main directory
if not os.path.exists(options.name) :
    os.system("mkdir %s" % options.name)
os.chdir("%s/%s" % (os.getcwd(), options.name))

## fill optionals
optionals = ""
if options.drop != "":
    optionals+=" --drop-channels '%s'" % options.drop 

## define htt event categories
htt_mm_categories = {
    "0jet"  : ["00", "01"],
    "boost" : ["02", "03"],
    "2jet"  : ["04"],
    "vbf"   : ["05"],
    #"btag"  : ["06", "07"],
    }

htt_em_categories = {
    "0jet"  : ["00", "01"],
    "boost" : ["02", "03"],
    "2jet"  : ["04"],
    "vbf"   : ["05"],
    #"btag"  : ["06", "07"],
    }

htt_mt_categories = {
    "0jet"  : ["00", "01"],
    "boost" : ["02", "03"],
    "2jet"  : ["04"],
    "vbf"   : ["05"],
    #"btag"  : ["06", "07"],
    }

htt_et_categories = {
    "0jet"  : ["00", "01"],
    "boost" : ["02", "03"],
    "2jet"  : ["04"],
    "vbf"   : ["05"],
    #"btag"  : ["06", "07"],
    }

htt_tt_categories = {
    "boost" : ["00"],
    "vbf"   : ["01"]
    }

## define hmm event categories
hmm_categories = {
    "noTag" : ["00"],
    "bTag"  : ["01"]
    }

## define hmm event categories
vhtt_had_categories = {
    "vhtt_had" : ["00"]
    }

## define categories for setup
categories = {
    "mm"  :  htt_mm_categories,
    "em"  :  htt_em_categories,
    "mt"  :  htt_mt_categories,
    "et"  :  htt_et_categories,
    #"tt"  :  htt_et_categories,
    #"vhtt":  htt_et_categories,
    }

## define run periods
periods = []
if options.period == "7TeV" or options.period == "all" :
    periods.append("7TeV-")
if options.period == "8TeV" or options.period == "all" :
    periods.append("8TeV-")

## define masses
masses = {}
if options.analysis == "sm" or options.analysis == "all" :
    masses["sm"] = options.sm_masses
if options.analysis == "mssm" or options.analysis == "all" :
    masses["mssm"] = options.mssm_masses    

## define sub-channels
sub_channels = ["em", "mt", "et", "mm", "tt", "vhtt_had"] ##, "hmm"]

## setup sm/mssm directories
for analysis in masses :
    if not os.path.exists(analysis) :
        os.system("mkdir %s" % analysis)
    os.chdir("%s/%s" % (os.getcwd(), analysis))
    ## individual event categories for all channels
    for period in periods :
        for sub in sub_channels :
            card_idx = 0
            if period == "8TeV" and (sub == "vhtt_had" or sub == "tt") :
                continue
            if sub == "hmm" :
                ## special treatment for hmm
                for label in hmm_categories :
                    for cat in hmm_categories[label] :
                        if options.category == "cmb" or options.category == "all" :
                            if options.channel == "cmb" or options.channel == "all" or options.channel == "hmm" :
                                #print sub, period, label, "1"
                                os.system("setup-batch.py -n cmb -c hmm -o hmm_{PERIOD}{IDX}.txt -e {PERIOD}{CAT} {OPTIONALS} {MASSES}".format(
                                    IDX=card_idx, PERIOD=period, CAT=cat, OPTIONALS=optionals, MASSES=masses[analysis]))
                        if options.category == "all" or options.category == cat :
                            #print sub, period, label, "2"
                            os.system("setup-batch.py -n {LABEL} -c hmm -o hmm_{PERIOD}{IDX}.txt -e {PERIOD}{CAT} {OPTIONALS} {MASSES}".format(
                                LABEL=label, IDX=card_idx, PERIOD=period, CAT=cat, OPTIONALS=optionals, MASSES=masses[analysis]))
                        card_idx = card_idx+1
            elif sub == "vhtt_had" :
                ## special treatment for vhtt_had
                for label in vhtt_had_categories :
                    for cat in vhtt_had_categories[label] :
                        if options.category == "cmb" or options.category == "all" :
                            if options.channel == "cmb" or options.channel == "all" or options.channel == "vhtt_had" :
                                #print sub, period, label, "1"
                                os.system("setup-batch.py -n cmb -c vhtt_had -o vhtt_had_{PERIOD}{IDX}.txt -e {PERIOD}{CAT} {OPTIONALS} {MASSES}".format(
                                    IDX=card_idx, PERIOD=period, CAT=cat, OPTIONALS=optionals, MASSES=masses[analysis]))
                        if options.category == "all" or options.category == cat :
                            if options.channel == "cmb" or options.channel == "all" or options.channel == "vhtt_had" :
                                #print sub, period, label, "2"
                                os.system("setup-batch.py -n {LABEL} -c vhtt_had -o vhtt_had_{PERIOD}{IDX}.txt -e {PERIOD}{CAT} {OPTIONALS} {MASSES}".format(
                                    LABEL=label, IDX=card_idx, PERIOD=period, CAT=cat, OPTIONALS=optionals, MASSES=masses[analysis]))
                        card_idx = card_idx+1
            elif sub == "tt" :
                ## special treatment for htt_tt
                for label in htt_tt_categories :
                    for cat in htt_tt_categories[label] :
                        if options.category == "cmb" or options.category == "all" :
                            if options.channel == "cmb" or options.channel == "all" :
                                #print sub, period, label, "3"
                                os.system("setup-batch.py -n cmb -c {SUBCHN} -o htt_{SUBCHN}_{PERIOD}{IDX}.txt -e {PERIOD}{CAT} {OPTIONALS} {MASSES}".format(
                                    SUBCHN=sub, IDX=card_idx, PERIOD=period, CAT=cat, OPTIONALS=optionals, MASSES=masses[analysis]))
                            if options.channel == sub or options.channel == "all" :
                                #print sub, period, label, "4"
                                os.system("setup-batch.py -n {SUBCHN} -c {SUBCHN} -o htt_{SUBCHN}_{PERIOD}{IDX}.txt -e {PERIOD}{CAT} {OPTIONALS} {MASSES}".format(
                                    SUBCHN=sub, IDX=card_idx, PERIOD=period, CAT=cat, OPTIONALS=optionals, MASSES=masses[analysis]))
                        if options.category == "all" or options.category == label :
                            if options.channel == sub or options.channel == "all" :
                                #print sub, period, label, "4a"
                                os.system("setup-batch.py -n {LABEL} -c {SUBCHN} -o htt_{SUBCHN}_{PERIOD}{IDX}.txt -e {PERIOD}{CAT} {OPTIONALS} {MASSES}".format(
                                    LABEL=label, SUBCHN=sub, IDX=card_idx, PERIOD=period, CAT=cat, OPTIONALS=optionals, MASSES=masses[analysis]))
                        card_idx = card_idx+1
            else :
                ## common treatment for htt_xx
                for label in categories[sub] :
                    for cat in categories[sub][label] :
                        if options.category == "cmb" or options.category == "all" :
                            if options.channel == "cmb" or options.channel == "all" :
                                #print label, cat, card_idx
                                os.system("setup-batch.py -n cmb -c {SUBCHN} -o htt_{SUBCHN}_{PERIOD}{IDX}.txt -e {PERIOD}{CAT} {OPTIONALS} {MASSES}".format(
                                    SUBCHN=sub, IDX=card_idx, PERIOD=period, CAT=cat, OPTIONALS=optionals, MASSES=masses[analysis]))
                            if options.channel == sub or options.channel == "all" :
                                #print label, cat, card_idx
                                os.system("setup-batch.py -n {SUBCHN} -c {SUBCHN} -o htt_{SUBCHN}_{PERIOD}{IDX}.txt -e {PERIOD}{CAT} {OPTIONALS} {MASSES}".format(
                                    SUBCHN=sub, IDX=card_idx, PERIOD=period, CAT=cat, OPTIONALS=optionals, MASSES=masses[analysis]))
                        if options.category == "all" or options.category == label :
                            if options.channel == sub or options.channel == "all" :
                                #print label, cat, card_idx
                                os.system("setup-batch.py -n {LABEL} -c {SUBCHN} -o htt_{SUBCHN}_{PERIOD}{IDX}.txt -e {PERIOD}{CAT} {OPTIONALS} {MASSES}".format(
                                    LABEL=label, SUBCHN=sub, IDX=card_idx, PERIOD=period, CAT=cat, OPTIONALS=optionals, MASSES=masses[analysis]))
                        card_idx = card_idx+1                        
    os.chdir("%s/.." % os.getcwd())
