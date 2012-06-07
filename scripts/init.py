#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to copy all root input files to obtain the full functionality of the package. These files are used for datacard creation and cross section estimates in different MSSM models and in the SM. They are to large to be kept in the official CMSSW package and therefore have to be copied into the local copy of the package.\n")
parser.add_option("--tag", dest="version", default="V00-01-xx", type="string", help="The cvs tag of the UserCode package to administrate the input files. [Default: \"V00-01-xx\"]")
parser.add_option("--cvs-path", dest="path", default="UserCode/HiggsAnalysis/HiggsToTauTau", type="string", help="The cvs path of the UserCode package to administrate the input files. [Default: UserCode/HiggsAnalysis/HiggsToTauTau]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os

print " -------------------------------------------------------------------------------------------- "
print " Completing package HiggsAnalysis/HiggsToTauTau with all input files, which are necessary to  "
print " make maximal use of it. These input files are expected to be present in an input directory   "
print " auxiliaries. trying to check this directory out from the for following UserCode directory:   "
print " PATH = {PATH}".format(PATH=options.path)
print " TAG  = {TAG}".format(TAG=options.version)
print " -------------------------------------------------------------------------------------------- "

## setup CMSSW to be able to co the auxiliray package
os.chdir("{CMSSW_BASE}/src".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))
os.system("cmsenv")
os.system("cvs co -d auxiliaries -r {TAG} {PATH}".format(TAG=options.version, PATH=options.path))

## copy all inputs into the corresponding directories in the HiggsToTauTau package
os.chdir("{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/data".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))
os.system("python init-data.py" )
os.chdir("{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))
os.system("python init-setup.py")
