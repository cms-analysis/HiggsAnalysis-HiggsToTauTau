#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to scale signal in inputs files by the cross section for SM Higgs boson. This will transform expectations normalized to 1/pb to yield predictions. The signal samples have to be given as options. ARGS corresponds to the given masses, for which the scaling should be performed.")
parser.add_option("-i", "--input", dest="input", default="test.root", type="string", help="Input file where to find the signal histograms (or workspaces). [Default: test.root]")
parser.add_option("-o", "--old", dest="old", default="scale_t", type="string",         help="Old Histogram string to replace [Default:scale_t] ")
parser.add_option("-n", "--new", dest="new", default="scale_t_et_7TeV", type="string", help="New Histogram string to replace [Default:scale_t_et_7TeV]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="increase verbosity. [Default: False]")

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
print " old     : ", options.old
print " new     : ", options.new

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs 

## do the rescaling
os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/decoupleShapes.C+\(true,\"{OLD}\",\"{NEW}\",\"{INPUTFILE}\",\"\",0\)".format(
    CMSSW_BASE=os.environ.get("CMSSW_BASE"), OLD=options.old,NEW=options.new, INPUTFILE=options.input))

