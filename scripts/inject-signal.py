#!/usr/bin/env python

from optparse import OptionParser, OptionGroup
import subprocess
import shlex

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to inject signal with fixed mH into a BG only hypothesis from simulation. The mass of the signal to be injected can be passed on by option --mass-injected (-m). The data_obs histograms of each event category found in the input root file is rescaled and the datacard is ajusted accordingly. The injected signal can be chosen to correspond to the expectation from BG and signal. In addition it can be randomized. The signal can be scaled before injection.")
parser.add_option("-i", "--in", dest="input", default="test", type="string", help="Name of the input directory, where to find all inputfiles and datacards in the usual structure for limits calculation. [Default: test]")
parser.add_option("-m", "--mass-injected", dest="mass_injected", default="125", type="string", help="Masspoint to be injected into the background only hypothesis from simulation. [Default: 125]")
parser.add_option("-s", "--signal-strength", dest="signal_strength", default="1", type="string", help="Signal strength to inject into the BG only expecation (in multiples of SM cross section). [Default: \"1\"]")
parser.add_option("-r", "--random", dest="rnd", default="-1", type="int", help="Randomize data yield, enter random seed, -1 will switch randomization off. [Default: \"-1\"]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string", help="List of run periods for which the datacards are to be copied. [Default: \"7TeV 8TeV\"]")
parser.add_option("-c", "--channels", dest="channels", default="tt mm em mt et", type="string", help="List of channels, for whch the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt. [Default: \"mm em mt et\"]")
parser.add_option("--categories", dest="categories", default="0 1 2 3 5", type="string", help="List of all principally available event categories. The script will internally pick all event categories, which are present in the corresponding mass directory, but this string indicated what event categories will be checked for.. [Default: \"0 1 2 3 5\"]")
sub1 = OptionGroup(parser, "BACKGROUNDS", "Backgrounds to be considered to replace data_obs.")
sub1.add_option("--backgrounds-mm", dest="backgrounds_mm", default="ZTT,ZMM,QCD,TTJ,WJets,Dibosons", type="string", help="List of backgrounds for mm channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"ZTT,ZMM,QCD,TTJ,WJets,Dibosons\"]")
sub1.add_option("--backgrounds-em", dest="backgrounds_em", default="Fakes,EWK,ttbar,Ztt", type="string", help="List of backgrounds for em channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"Fakes,EWK,ttbar,Ztt\"]")
sub1.add_option("--backgrounds-et", dest="backgrounds_et", default="ZTT,QCD,W,ZJ,ZL,ZLL,TT,VV", type="string", help="List of backgrounds for et channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"ZTT,QCD,W,ZJ,ZL,ZLL,TT,VV\"]")
sub1.add_option("--backgrounds-mt", dest="backgrounds_mt", default="ZTT,QCD,W,ZJ,ZL,ZLL,TT,VV", type="string", help="List of backgrounds for mt channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"ZTT,QCD,W,ZJ,ZL,ZLL,TT,VV\"]")
sub1.add_option("--backgrounds-tt", dest="backgrounds_tt", default="ZTT,QCD,W,ZJ,ZL,TT,VV", type="string", help="List of backgrounds for tt channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"ZTT,QCD,W,ZJ,ZL,TT,VV\"]")
sub1.add_option("--backgrounds-wh", dest="backgrounds_wh", default="wz,zz,fakes", type="string", help="List of backgrounds for the WH channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"wz,zz,fakes\"]")
sub1.add_option("--backgrounds-zh", dest="backgrounds_zh", default="ZZ,Zjets", type="string", help="List of backgrounds for the WH channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"ZZ,Zjets\"]")
parser.add_option_group(sub1)
sub1 = OptionGroup(parser, "SIGNALS", "Signals to be considered to replace data_obs.")
sub1.add_option("--signals-mm", dest="signals_mm", default="ggH{MASS},qqH{MASS},VH{MASS}", type="string", help="List of signal for em channel. NOTE: should be comma separated, NO spaces allowed. The keyword {MASS} will be replaced by the mass to be injected (--mass-injected). It has to be present in the signal sample string. [Default: \"ggH{MASS},qqH{MASS},VH{MASS}\"]")
sub1.add_option("--signals-em", dest="signals_em", default="ggH{MASS},qqH{MASS},VH{MASS}", type="string", help="List of signal for em channel. NOTE: should be comma separated, NO spaces allowed. The keyword {MASS} will be replaced by the mass to be injected (--mass-injected). It has to be present in the signal sample string. [Default: \"ggH{MASS},qqH{MASS},VH{MASS}\"]")
sub1.add_option("--signals-et", dest="signals_et", default="ggH{MASS},qqH{MASS},VH{MASS}", type="string", help="List of signal for em channel. NOTE: should be comma separated, NO spaces allowed. The keyword {MASS} will be replaced by the mass to be injected (--mass-injected). It has to be present in the signal sample string. [Default: \"ggH{MASS},qqH{MASS},VH{MASS}\"]")
sub1.add_option("--signals-mt", dest="signals_mt", default="ggH{MASS},qqH{MASS},VH{MASS}", type="string", help="List of signal for em channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"ggH{MASS},qqH{MASS},VH{MASS}\"]")
sub1.add_option("--signals-tt", dest="signals_tt", default="ggH{MASS},qqH{MASS},VH{MASS}", type="string", help="List of signal for em channel. NOTE: should be comma separated, NO spaces allowed. [Default: \"ggH{MASS},qqH{MASS},VH{MASS}\"]")
sub1.add_option("--signals-vhtt", dest="signals_vhtt", default="VH{MASS},VH_hww{MASS}", type="string", help="List of signal for the VH (WH & ZH) channels. NOTE: should be comma separated, NO spaces allowed. [Default: \"VH{MASS},VH_hww{MASS}\"]")
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

def adjust_datacard(datacard, new_values) :
    print "doot", datacard, new_values
    old = open(datacard, 'r')
    new = open("tmp.txt", 'w')
    for line in old :
        words = line.split()
        if len(words) < 1: continue
        ## determine a list of unique decay channels
        if words[0] == "observation" :
            line = " ".join(['observation'] + new_values)
        new.write(line + '\n')
    old.close()
    new.close()
    os.system("mv tmp.txt %s" % datacard)

def get_bins(datacard):
    ''' Extract the name of the bins from a data card. Returns a list.

    Example of a bin: mumu_0jet_low

    The order is preserved.
    '''
    dc = open(datacard, 'r')
    for line in dc:
        words = line.split()
        if words and words[0].lower() == 'bin':
            return words[1:]
    return []

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
    ("tt", "0") : "tauTau_boost",
    ("tt", "1") : "tauTau_vbf",
    ("wh", "0") : ["emt", "mmt"], # WH is always category 0, and is 2 channels
    # ZH is always category 1, and is 8 channels
    ("zh", "1") : ["mmmt_zh", "mmet_zh", "mmme_zh", "mmtt_zh", "eemt_zh",
                   "eeet_zh", "eeem_zh", "eett_zh"],
    }

## mapping out backgrounds
backgrounds = {
    "mm" : options.backgrounds_mm,
    "em" : options.backgrounds_em,
    "et" : options.backgrounds_et,
    "mt" : options.backgrounds_mt,
    "tt" : options.backgrounds_tt,
    "wh" : options.backgrounds_wh,
    "zh" : options.backgrounds_zh,
    }
## mapping out signals
signals = {
    "mm" : options.signals_mm,
    "em" : options.signals_em,
    "et" : options.signals_et,
    "mt" : options.signals_mt,
    "tt" : options.signals_tt,
    "wh" : options.signals_vhtt,
    "zh" : options.signals_vhtt,
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

def get_shape_file(channel, period):
    ''' Map a channel + run period to a shape .root file '''
    if channel not in ['wh', 'zh']:
        return options.input+"/common/htt_"+channel+".input_"+period+".root"
    else:
        return options.input+"/common/vhtt.input_"+period+".root"

## randomize observation for all potential hist input files
for chn in channels :
    for per in periods :
        re.sub(r'\s', '', signals[chn])
        signals[chn] = signals[chn].format(MASS=options.mass_injected)
        re.sub(r'\s', '', backgrounds[chn])
        histfile = get_shape_file(chn, per)
        if os.path.exists(histfile) :
            if options.verbose :
                print "randomizing all data_obs in histogram input file:", histfile
            # Which channel directories in the .root file to randomize.
            # For the normal H2Tau case, this doesn't matter - since every
            # channel (directory) has the same backgrounds in it.
            # For WH/ZH, both are in the same file, and the names of the bkgs.
            # depend on which category (i.e. WH or ZH) it is.
            directories_to_randomize = '*'
            if chn == 'zh':
                directories_to_randomize = '*_zh'
            elif chn == 'wh':
                directories_to_randomize = 'emt,mmt'
            command = "root -l -q -b {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/blindData.C+\\(\\\"{FILE}\\\",\\\"{BACKGROUNDS}\\\",\\\"{SIGNALS}\\\",\\\"{DIRS}\\\",true,{RND},{SCALE},1\)"
            yields = subprocess.Popen(
                shlex.split(command.format(
                    CMSSW_BASE=os.environ["CMSSW_BASE"],
                    FILE=histfile,
                    BACKGROUNDS=backgrounds[chn],
                    SIGNALS=signals[chn],
                    DIRS=directories_to_randomize,
                    RND=options.rnd,
                    SCALE=options.signal_strength,
                )), stdout=subprocess.PIPE)

            (stdout, _) = yields.communicate()
            data_obs_lines = []
            for line in stdout.split('\n'):
                if 'data_obs' in line:
                    data_obs_lines.append(line)
            yields_map[(chn,per)] = " ".join(data_obs_lines)
            #print "%s ...done" % yields_map[(chn,per)]
            print "...done"

def get_card_file(channel, category, period, mass):
    ''' Map a channel, category, period, and mass to a datacard .txt file'''
    if channel not in ['wh', 'zh']:
        return os.path.join(options.input, str(mass),
                            "htt_"+channel+"_"+category+"_"+period+".txt")
    else:
        # For WH and ZH, they are differentiated by category number
        if channel == 'wh' and int(category) != 0:
            return "wh is always category 0" # this will fail os.path.exists
        elif channel == 'zh' and int(category) != 1:
            return "zh is always category 1" # this will fail os.path.exists
        return os.path.join(options.input, str(mass),
                            "vhtt_"+category+"_"+period+".txt")

## put output, which is in bits and pieces into a list of relevant lines
## that is used for further processing
for mass in parseArgs(args) :
    for chn in channels :
        for per in periods :
            for cat in categories:
                datacard = get_card_file(chn, cat, per, mass)
                if os.path.exists(datacard) :
                    if options.verbose :
                        print "adapting observation yield in datacard:", datacard
                    # Get name of bins
                    directories = get_bins(datacard)
                    print datacard, directories

                    new_values = []
                    for dir in directories:
                        #print directory, chn, per
                        #print yields_map[(chn,per)]
                        new_yield = search_list(yields_map[(chn,per)].split(), dir)[1]
                        new_values.append(new_yield)
                        #print search_list(yields_map[(chn,per)].split(), directory)
                    adjust_datacard(datacard, new_values)

