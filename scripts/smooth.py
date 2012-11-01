#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to scale signal in inputs files by the cross section for SM Higgs boson. This will transform expectations normalized to 1/pb to yield predictions. The signal samples have to be given as options. ARGS corresponds to the given masses, for which the scaling should be performed.")
parser.add_option("-i"  ,"--input", dest="input", default="test.root", type="string", help="Input file where to find the signal histograms (or workspaces). [Default: test.root]")
parser.add_option("-k"  ,"--key", dest="key", default="CMS"      , type="string",         help="Key to change range")
parser.add_option("-d"  ,"--dir", dest="dir", default="0jet_high", type="string",         help="Dir to change range")
parser.add_option("-v"  ,"--verbose", dest="verbose", default=False, action="store_true", help="increase verbosity. [Default: False]")

# check number of arguments; in case print usage
(options, args) = parser.parse_args()
#if len(args) < 1 :
#    parser.print_usage()
#    exit(1)

import os
import re

print " You are running with configuration: "
print "-------------------------------------"
print " input   : ", options.input
print " key     : ", options.key
print " dir     : ", options.dir

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs 

## do the rescaling
os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/smooth.C+\(true,\"{OLD}\",\"{NEW}\",\"{INPUTFILE}\",\"\",0\)".format(
    CMSSW_BASE=os.environ.get("CMSSW_BASE"), OLD=options.key,NEW=options.dir, INPUTFILE=options.input))

