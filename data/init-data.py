#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Simple script to link root input files which cannot be stored in the official cvs repository due to their size to the setup directory of this package. Apart from options no further ARGs are needed")
parser.add_option("-i", "--input-card", dest="input", default="input-card.txt", type="string", help="Inputcard to be used for the copy process. [Default: input-card.txt]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os

f = open(options.input, 'r')
for line in f:
    line = line.strip().split("\n")[0].strip()   
    if line == "" or line.startswith("#") or line.startswith("%"):
        continue
    else:
        words = line.strip().split()
        #print "cp {CMSSW_BASE}/src/{source} {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/data/{target}".format(
        #    CMSSW_BASE=os.environ['CMSSW_BASE'], source=words[1], target=words[0])
        os.system("cp -s {CMSSW_BASE}/src/{source} ./{target}".format(
            CMSSW_BASE=os.environ['CMSSW_BASE'], source=words[1], target=words[0]))
f.close()




