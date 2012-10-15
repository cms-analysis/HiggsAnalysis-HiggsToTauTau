#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to collect and hadd the rootfiles of the output of lxq/b_gridScan.py. Also the temp files are deleted!")
parser.add_option("-d", "--directory", dest="directory", default="test", type="string", help="Name of the directory where the gridScan points are . [Default: test-injected]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os
import sys

mass = options.directory[options.directory.rfind("/")+1:]
os.system("hadd {DIRECTORY}/higgsCombineScan.MultiDimFit.mH{MASS}.root {DIRECTORY}/higgsCombine_*.MultiDimFit.mH{MASS}-*.root".format(
    DIRECTORY=options.directory,
    MASS=mass
    ))
os.system("rm {DIRECTORY}/tmp*".format(
    DIRECTORY=options.directory
    ))
os.system("rm {DIRECTORY}/higgsCombine_*.MultiDimFit.mH{MASS}-*.root".format(
    DIRECTORY=options.directory,
    MASS=mass
    ))
        
            
