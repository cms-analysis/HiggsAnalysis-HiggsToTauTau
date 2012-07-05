#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to inject signal with fixed mH into a BG only hypothesis from simulation. The mass of the signal to be injected can be passed on by option --mass-injected (-m). The data_obs histograms of each event category found in the input root file is rescaled and the datacard is ajusted accordingly. The injected signal can be chosen to correspond to the expectation from BG and signal. In addition it can be randomized. The signal can be scaled before injection.")
parser.add_option("-i", "--in", dest="input", default="test", type="string", help="Name of the input directory, where to find all inputfiles and datacards in the usual structure for limits calculation. [Default: test]")
parser.add_option("-m", "--mass-injected", dest="mass_injected", default="125", type="string", help="Masspoint to be injected into the background only hypothesis from simulation. [Default: 125]")
parser.add_option("-s", "--signal-strength", dest="signal_strength", default="1", type="string", help="Signal strength to inject into the BG only expecation (in multiples of SM cross section). [Default: \"1\"]")
parser.add_option("-r", "--random", dest="rnd", default="-1", type="int", help="Randomize data yield, enter random seed, -1 will switch randomization off. [Default: \"-1\"]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string", help="List of run periods for which the datacards are to be copied. [Default: \"7TeV 8TeV\"]")
parser.add_option("-c", "--channels", dest="channels", default="mm em mt et", type="string", help="List of channels, for whch the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt. [Default: \"mm em mt et\"]")
parser.add_option("--categories", dest="categories", default="0 1 2 3 5", type="string", help="List of all principally available event categories. The script will internally pick all event categories, which are present in the corresponding mass directory, but this string indicated what event categories will be checked for.. [Default: \"0 1 2 3 5\"]")
sub1 = OptionGroup(parser, "BACKGROUNDS", "Backgrounds to be considered to replace data_obs.")
sub1.add_option("--backgrounds-mm", dest="backgrounds_mm", default="ZTT,ZMM,QCD,TTJ,WJets,Dibosons", type="string", help="List of backgrounds for mm channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"ZTT,ZMM,QCD,TTJ,WJets,Dibosons\"]")
sub1.add_option("--backgrounds-em", dest="backgrounds_em", default="Fakes,EWK,ttbar,Ztt", type="string", help="List of backgrounds for em channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"Fakes,EWK,ttbar,Ztt\"]")
sub1.add_option("--backgrounds-et", dest="backgrounds_et", default="ZTT,QCD,W,ZJ,ZL,ZLL,TT,VV", type="string", help="List of backgrounds for et channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"ZTT,QCD,W,ZJ,ZL,ZLL,TT,VV\"]")
sub1.add_option("--backgrounds-mt", dest="backgrounds_mt", default="ZTT,QCD,W,ZJ,ZL,ZLL,TT,VV", type="string", help="List of backgrounds for mt channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"ZTT,QCD,W,ZJ,ZL,ZLL,TT,VV\"]")
parser.add_option_group(sub1)
sub1 = OptionGroup(parser, "SIGNALS", "Signals to be considered to replace data_obs.")
sub1.add_option("--signals-mm", dest="signals_mm", default="ggH{MASS},qqH{MASS},VH{MASS}", type="string", help="List of signal for em channel. NOTE: should be comma separated, NO spaces allowed. The keyword {MASS} will be replaced by the mass to be injected (--mass-injected). It has to be present in the signal sample string. [Default: \"ggH{MASS},qqH{MASS},VH{MASS}\"]")
sub1.add_option("--signals-em", dest="signals_em", default="ggH{MASS},qqH{MASS},VH{MASS}", type="string", help="List of signal for em channel. NOTE: should be comma separated, NO spaces allowed. The keyword {MASS} will be replaced by the mass to be injected (--mass-injected). It has to be present in the signal sample string. [Default: \"ggH{MASS},qqH{MASS},VH{MASS}\"]")
sub1.add_option("--signals-et", dest="signals_et", default="ggH{MASS},qqH{MASS},VH{MASS}", type="string", help="List of signal for em channel. NOTE: should be comma separated, NO spaces allowed. The keyword {MASS} will be replaced by the mass to be injected (--mass-injected). It has to be present in the signal sample string. [Default: \"ggH{MASS},qqH{MASS},VH{MASS}\"]")
sub1.add_option("--signals-mt", dest="signals_mt", default="ggH{MASS},qqH{MASS},VH{MASS}", type="string", help="List of signal for em channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"ggH{MASS},qqH{MASS},VH{MASS}\"]")
parser.add_option_group(sub1)
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Run in verbose mode. [Default: False]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs


def output_to_list(basket) :
    line=""
    for elem in basket :
        line+=elem
    return line.split('\n') 

def search_list(list, value) :
    for idx in range(len(list)) :
        #print list[idx], value
        if list[idx] == value :
            return (list[idx], list[idx+1])
    return ("NONE", -999.)

def adjust_datacard(datacard, value) :
    old = open(datacard, 'r')
    new = open("tmp.txt", 'w')
    for line in old :
        words = line.split()
        if len(words) < 1: continue
        ## determine a list of unique decay channels
        if words[0] == "observation" :
            line = line.replace(words[1], str(value))
        new.write(line)
    old.close()
    new.close()
    os.system("mv tmp.txt %s" % datacard)

## mapping out the channel and event category to directories in the root files
directories = {
    ("mm", "0") : "mumu_0jet_low",
    ("mm", "1") : "mumu_0jet_high",
    ("mm", "2") : "mumu_boost_low",
    ("mm", "3") : "mumu_boost_high",
    ("mm", "5") : "mumu_vbf",
    ("em", "0") : "emu_0jet_low",
    ("em", "1") : "emu_0jet_high",
    ("em", "2") : "emu_boost_low",
    ("em", "3") : "emu_boost_high",
    ("em", "5") : "emu_vbf",
    ("et", "0") : "eTau_0jet_low",
    ("et", "1") : "eTau_0jet_high",
    ("et", "2") : "eTau_boost_low",
    ("et", "3") : "eTau_boost_high",
    ("et", "5") : "eTau_vbf",
    ("mt", "0") : "muTau_0jet_low",
    ("mt", "1") : "muTau_0jet_high",
    ("mt", "2") : "muTau_boost_low",
    ("mt", "3") : "muTau_boost_high",
    ("mt", "5") : "muTau_vbf",
    }
## mapping out backgrounds
backgrounds = {
    "mm" : options.backgrounds_mm,
    "em" : options.backgrounds_em,
    "et" : options.backgrounds_et,
    "mt" : options.backgrounds_mt,
    }
## mapping out signals
signals = {
    "mm" : options.signals_mm,
    "em" : options.signals_em,
    "et" : options.signals_et,
    "mt" : options.signals_mt,
    }
## run periods
periods = options.periods.split()
for idx in range(len(periods)) : periods[idx] = periods[idx].rstrip(',')
## channels 
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')
## categories 
categories = options.categories.split()
for idx in range(len(categories)) : categories[idx] = categories[idx].rstrip(',')
## mapping out the yields
yields_map = {}

## randomize observation for all potential hist input files
for chn in channels :
    for per in periods :
        re.sub(r'\s', '', signals[chn])
        signals[chn] = signals[chn].format(MASS=options.mass_injected)
        re.sub(r'\s', '', backgrounds[chn])
        histfile = options.input+"/common/htt_"+chn+".input_"+per+".root"
        if os.path.exists(histfile) :
            if options.verbose :
                print "randomizing all data_obs in histogram input file:", histfile
            yields = os.popen(
                "root -l -q -b {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/blindData.C+\\(\\\"{FILE}\\\",\\\"{BACKGROUNDS}\\\",\\\"{SIGNALS}\\\",true,{RND},{SCALE},0\) | grep data_obs".format(
                CMSSW_BASE=os.environ["CMSSW_BASE"],
                FILE=histfile,
                BACKGROUNDS=backgrounds[chn],
                SIGNALS=signals[chn],
                RND=options.rnd,
                SCALE=options.signal_strength,
                )).read()
            yields_map[(chn,per)] = yields
            
## put output, which is in bits and pieces into a list of relevant lines
## that is used for further processing
for mass in parseArgs(args) :
    for chn in channels :
        for per in periods :
            for cat in categories: 
                datacard = options.input+"/"+str(mass)+"/htt_"+chn+"_"+cat+"_"+per+".txt"
                if os.path.exists(datacard) :
                    if options.verbose :
                        print "adapting observation yield in datacard:", datacard
                    ## PATCH until Josh fixes his input fies to contain the proper
                    ## directory names in et
                    directory = directories[(chn,cat)]
                    if per == "8TeV" and chn == "et" :
                        #print "changing directory name"
                        directory = directory.replace("eTau", "eleTau")
                    #print directory, chn, per
                    #print yields_map[(chn,per)]
                    new_yield = search_list(yields_map[(chn,per)].split(), directory)[1]
                    #print search_list(yields_map[(chn,per)].split(), directory)
                    adjust_datacard(datacard, new_yield)
        
