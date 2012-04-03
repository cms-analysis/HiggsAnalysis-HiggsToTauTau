#!/usr/bin/env python

import os

print " -------------------------------------------------------------------------------------------- "
print " Completing package HiggsAnalysis/HiggsToTauTau with all input files, which are necessary to  "
print " make maximal use of it. These input files are expected to be present in an input directory   "
print " datacard. You can check this directory out from the UserCode cvs using the following command "
print
print " cvs co -r V00-01-01 -d datacards UserCode/RWolf/MitLimits/Higgs2Tau/data"
print " -------------------------------------------------------------------------------------------- "

os.chdir("{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/data".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))
os.system("python init-data.py" )
os.chdir("{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))
os.system("python init-setup.py")
