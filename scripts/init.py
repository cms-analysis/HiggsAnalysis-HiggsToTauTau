#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="This is a script to copy all root input files to obtain the full functionality of the package. These files are used for datacard creation and cross section estimates in different MSSM models and in the SM. They are to large to be kept in the official CMSSW package and therefore have to be copied into the local clopy of the packae by hand. \n")
## direct options
parser.add_option("--version", dest="version", default="V00-01-xx", type="string", help="CMSSW version of the UserCode package to administrate the input files. [Default: \"V00-01-xx\"]")
parser.add_option("--path", dest="path", default="UserCode/RWolf/MitLimits/Higgs2Tau/data", type="string", help="Path of the UserCode package to administrate the input files. [Default: \"UserCode/RWolf/MitLimits/Higgs2Tau/data\"]")

import os

print " -------------------------------------------------------------------------------------------- "
print " Completing package HiggsAnalysis/HiggsToTauTau with all input files, which are necessary to  "
print " make maximal use of it. These input files are expected to be present in an input directory   "
print " datacard. trying to check this directory out from the for following UserCode directory:      "
print " PATH    = {path}".format(options.path)
print " VERSION = {version}".format(options.version)
print " -------------------------------------------------------------------------------------------- "

## setup CMSSW to be able to co the auxiliray package
os.chdir("{CMSSW_BASE}/src".format(CMSSW_BASE.os.environ.get("CMSSW_BASE")))
os.chdir("cmsenv")
os.chdir("cvs co -d datacards -r {version} {path}".format(version=options.version, options.path))

## copy all inputs into the corresponding directories in the HiggsToTauTau package
os.chdir("{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/data".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))
os.system("python init-data.py" )
os.chdir("{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))
os.system("python init-setup.py")
