#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGs",
                      description="This is a script to scale signal in input files by the cross section for a SM Higgs boson. This will transform expectations normalized to 1/pb to yield predictions. The signal samples have to be given as options. ARGs corresponds to the given masses, for which the scaling should be performed.")
parser.add_option("-i", "--input", dest="input", default="test.root", type="string",
                  help="Input file where to find the signal histograms (or workspaces). [Default: test.root]")
parser.add_option("-s", "--samples", dest="samples", default="ggH, qqH, VH, WH, ZH, ttH, bbH", type="string",
                  help="Signal samples that should be scaled. This should be a list of strings in \"...\", seperated by comma or by whitespace. Sample which are not present in the file will be ignored. When running in verbose mode a warning will be issued. [Default: \"ggH, qqH, VH, WH, ZH, ttH, bbH\"]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="increase verbosity. [Default: False]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re

## determine the center of mass energy from the name of the input file
filename = options.input
if '/' in filename :
    filename = filename[filename.rfind('/')+1:]
matcher = re.compile('v?htt_?\w*.inputs-\w*-(?P<PERIOD>[0-9]*\w*)(-?_?\w*)*.root')
ecms_str = matcher.match(filename).group('PERIOD')
ecms_str = ecms_str[:ecms_str.find('TeV')]
ecms = float(ecms_str)

print " You are running with configuration: "
print "-------------------------------------"
print " input   : ", options.input
print " samples : ", options.samples
print " ecms    : ", ecms

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs 
from HiggsAnalysis.HiggsToTauTau.scale2SM import RescaleSamples

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
