#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to scale signal in inputs files by the cross section for SM Higgs boson. This will transform expectations normalized to 1/pb to yield predictions. The signal samples have to be given as options. ARGS corresponds to the given masses, for which the scaling should be performed.")
parser.add_option("-i", "--input", dest="input", default="test.root", type="string", help="Input file where to find the signal histograms (or workspaces). [Default: test.root]")
parser.add_option("-s", "--samples", dest="samples", default="ggH, qqH, VH, WH, ZH, ttH, bbH", type="string", help="Signal samples that should be scaled. This should be a list of strings in \"...\", seperated by comma or by whitespace. Sample which are not present in the file will be ignored. When running in verbose mode a warning will be issued. [Default: \"ggH, qqH, VH, WH, ZH, ttH, bbH\"]")
parser.add_option("-e", "--ecms", dest="ecms", default="7", type="string", help="Center of mass energy in TeV. [Default: 7]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="increase verbosity. [Default: False]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re

## determine the center of mass energy from the name of the input file
matcher = re.compile('v?htt_\w*.inputs-\w*-(?P<PERIOD>[0-9]*\w*)-?_?\w*.root')
ecms_str = matcher.match(options.input).group('PERIOD')
ecms_str = ecms_str[:ecms_str.find('TeV')]
ecms = float(ecms_str)

print " You are running with configuration: "
print "-------------------------------------"
print " input   : ", options.input
print " samples : ", options.samples
print " ecms    : ", ecms

class RescaleSamples:
    def __init__(self, input_file, production_channels, masspoints) :
        ## name of the input file
        self.input_file = input_file
        ## list of mass points to be scaled
        self.masses = masspoints
        ## list of signal channels to be scaled
        self.production_channels = production_channels
        
    def xsec(self, production_channel, mass) :
        """
        Loads SM cross sections needed to rescale the input histograms. Returns
        the cross section in pb
        """
        xs = 0
        if production_channel == "VH" :
            production_channel = "WH+ZH"
        if production_channel == "VH+" :
            production_channel = "WH+ZH_ttH"
        if production_channel == "SM" :
            production_channel = "ggH"
        if production_channel == "VBF" :
            production_channel = "qqH"
        if production_channel == 'bbH' :
            ## not yet available
            return xs            
        if production_channel.find('+')>-1 :
            sub_channels = production_channel.split('+')
            for sub_channel in sub_channels :
                xs += float(os.popen("xsec-sm {CHANNEL} {MA} {ECMS} | grep value".format(
                    CHANNEL=sub_channel, MA=mass, ECMS=ecms)).read().split()[2])
        else :
            print "xsec-sm {CHANNEL} {MA} {ECMS} | grep value".format(
                CHANNEL=production_channel, MA=mass, ECMS=ecms)
            xs += float(os.popen("xsec-sm {CHANNEL} {MA} {ECMS} | grep value".format(
                CHANNEL=production_channel, MA=mass, ECMS=ecms)).read().split()[2])
        return xs

    def BR(self, mass) :
        """
        Loads SM branching ratios needed to rescale the input histograms. 
        """
        return float(os.popen("xsec-sm BR {MA} | grep value".format(MA=mass)).read().split()[2])

    def rescale(self) :
        """
        Rescales histograms according to productiohn channel, decay channel and mass. The rescaling
        is done using the macro rescalSignal.C in the macros directory of the package. This does take
        automatic care of scaling histograms for signal (central value) and shape uncertainties.
        """
        for production_channel in self.production_channels :
            for mass in self.masses :
                ## determine cross section
                xs = self.xsec(production_channel, mass)
                ## determine BR
                br = self.BR(mass)
                ## determine search pattern for mass re-scaling
                pattern = production_channel+mass
                ## run the rescaling
                os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C+\(true,{SCALE},\"{INPUTFILE}\",\"{PROCESS}\",0\)".format(
                    CMSSW_BASE=os.environ.get("CMSSW_BASE"), SCALE=xs*br, INPUTFILE=self.input_file, PROCESS=pattern))


from HiggsAnalysis.HiggsToTauTau.utils import parseArgs 

## turn production_channels into a list of strings
samples = options.samples.split()
for idx in range(len(samples)) :
    samples[idx] = samples[idx].rstrip(',')

## turn masses to list of strings
masspoints = []
for mass in parseArgs(args) :
    masspoints.append("%s" % mass)

## do the rescaling
process = RescaleSamples(options.input, samples, masspoints)
process.rescale()
