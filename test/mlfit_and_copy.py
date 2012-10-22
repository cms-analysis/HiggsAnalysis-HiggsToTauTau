#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

# ML-fit a directory of datcards and copy here for making plots
# Usage: ./mlfit_and_copy.py <path>MY-LIMITS/125

parser = OptionParser(usage="usage: %prog [options] datacatd.txt",
                      description="Script to build up the necessart enviroment for postfit plots - including maxlikelihood calculation.")
(options, args) = parser.parse_args()

import os
import sys

analysis = args[0]
dir = args[1]

print "Fitting %s : %s" % (analysis, dir)

os.system("mkdir -p datacards")
os.system("mkdir -p root")
os.system("mkdir -p fitresults")
os.system("limit.py --max-likelihood --stable --rMin -10 --rMax 10 %s" % dir)

if analysis == "SM" :
    os.system("cp -v %s/out/mlfit.txt ./fitresults/mlfit_sm.txt" % dir)
    os.system("cp -v %s/*.txt ./datacards" % dir)
    os.system("cp -v %s/../common/*.root ./root" % dir)

if analysis == "MSSM" :
    os.system("cp -v %s/out/mlfit.txt ./fitresults/mlfit_mssm.txt" % dir)
    os.system("cp -v %s/*.txt ./datacards" % dir)
    os.system("cp -v %s/../common/*TeV.root ./root" % dir)
