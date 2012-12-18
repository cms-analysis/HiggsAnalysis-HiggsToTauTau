#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="Script to do quick blinding of datacards inputs. ARG correspond to the file of interest.\n")
parser.add_option("-s", "--signal", dest="signal", default="ggH{MASS},qqH{MASS},VH{MASS}", type="string", help="The signal sample to be injected. Should include a variable string for the mass, e.g. ggH{MASS}. If empty only no signal will be injected. The default corresponds to a SM signal. [Default: \"ggH{MASS},qqH{MASS},VH{MASS}\"]")
parser.add_option("-m", "--mass", dest="mass", default="125", type="string", help="The mass of the signal that should be injected. the default corresponds to 125GeV. Default: \"125\"]")
parser.add_option("-d", "--dir", dest="dir", default="\\*", type="string", help="The directories to which to apply the blinding. [Default: \"\\*\"]")
pgroup = OptionGroup(parser, "BACKGROUNDS", "Command options to customize the backgrounds per channel.")
parser.add_option("--backgrounds-em", dest="bg_em", default="Ztt,ttbar,EWK,Fakes", type="string", help="Backgrounds for blinding for em channel. [Default: 'Ztt,ttbar,EWK,Fakes']")
parser.add_option("--backgrounds-et", dest="bg_et", default="ZTT,QCD,W,ZJ,ZL,TT,VV", type="string", help="Backgrounds for blinding for et channel. [Default: 'ZTT,QCD,W,ZJ,ZL,TT,VV']")
parser.add_option("--backgrounds-mt", dest="bg_mt", default="ZTT,QCD,W,ZJ,ZL,TT,VV", type="string", help="Backgrounds for blinding for mt channel. [Default: 'ZTT,QCD,W,ZJ,ZL,TT,VV']")
parser.add_option("--backgrounds-mm", dest="bg_mm", default="ZTT,ZMM,QCD,TTJ,WJets,Dibosons", type="string", help="Backgrounds for blinding for mm channel. [Default: 'ZTT,ZMM,QCD,TTJ,WJets,Dibosons']")
parser.add_option("--backgrounds-tt", dest="bg_tt", default="ZTT,ZJ,ZL,QCD,TT,W,VV", type="string", help="Backgrounds for blinding for tt channel. [Default: 'ZTT,ZJ,ZL,QCD,TT,W,VV']")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os

input_file = args[0]
backgrounds = ""
if "htt_em" in input_file :
    backgrounds = options.bg_em
if "htt_et" in input_file :
    backgrounds = options.bg_et
if "htt_mt" in input_file :
    backgrounds = options.bg_mt
if "htt_mm" in input_file :
    backgrounds = options.bg_mm
if "htt_tt" in input_file :
    backgrounds = options.bg_tt

os.system("root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/blindData.C+\\(\\\"{INPUT}\\\",\\\"{BG}\\\",\\\"{SIG}\\\",\\\"{DIR}\\\",true\\)".format(
    CMSSW_BASE = os.environ['CMSSW_BASE'],
    INPUT = input_file,
    BG = backgrounds,
    SIG = options.signal.format(MASS=options.mass),
    DIR = options.dir
    ))
