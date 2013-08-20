#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGs",
                      description="This is a script to scale MSSM input histograms by the acceptance corrections that have been derived for the restriction of the signal event in pre-defined mass windows on generator level. The acceptance corrections are obtained from HiggsAnalysis/HiggsToTauTau/python/acceptance_correction.py. ATTENTION: the output will override the input histogram files with the original normalization. ARGs corresponds to the mass points for which the signal histograms should be scaled.")
parser.add_option("-i", "--input", dest="input", default="HiggsAnalysis/HiggsToTauTau/setup", type="string",
                  help="Input directory where to find the input files to be scaled [Default: HiggsAnalysis/HiggsToTauTau/setup]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string",
                  help="Choose between run periods [Default: \"7TeV 8TeV\"]")
parser.add_option("-c", "--channels", dest="channels", default="mm em mt et", type="string",
                  help="List of channels, for which inputs should be scaled. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt, hmm, hbb. [Default: \"mm em mt et\"]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs
from HiggsAnalysis.HiggsToTauTau.utils import mass_category
from HiggsAnalysis.HiggsToTauTau.acceptance_correction import acceptance_correction

source_path = ""
if not os.path.exists(options.input) :
    if os.path.exists(os.environ['CMSSW_BASE']+'/src/'+options.input) :
        source_path = "%s/src/%s" % (os.environ['CMSSW_BASE'], options.input)
    else :
        print "ERROR: path", options.input, "does not exist."
        exit(1)
else:
    source_path = options.input

## periods
periods = options.periods.split()
for idx in range(len(periods)) : periods[idx] = periods[idx].rstrip(',')
## channels
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')

for channel in channels :
    for period in periods :
        for cat in ['0'] :
            for mass in parseArgs(args) :
                for process in ['ggH', 'bbH'] :
                    exe = "{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C+".format(CMSSW_BASE=os.environ.get("CMSSW_BASE"))
                    os.system(r"root -l -b -q {EXE}\(true,{SCALE},\"{PATH}/{CHN}/htt_{CHN}.inputs-mssm-{PER}-{MASSCAT}.root\",\"{PROCESS}\",0\)".format(
                        EXE=exe,
                        PATH=source_path,
                        SCALE=acceptance_correction(process, mass, period),
                        CHN=channel,
                        PER=period,
                        MASSCAT=mass_category(mass,cat,'htt_'+channel),
                        PROCESS=process+str(mass)
                        ))
                    if channel=="mm" :
                        os.system(r"root -l -b -q {EXE}\(true,{SCALE},\"{PATH}/{CHN}/htt_{CHN}.inputs-mssm-{PER}-{MASSCAT}-msv.root\",\"{PROCESS}\",0\)".format(
                            EXE=exe,
                            PATH=source_path,
                            SCALE=acceptance_correction(process, mass, period),
                            CHN=channel,
                            PER=period,
                            MASSCAT=mass_category(mass,cat,'htt_'+channel),
                            PROCESS=process+str(mass)
                            ))
                    
