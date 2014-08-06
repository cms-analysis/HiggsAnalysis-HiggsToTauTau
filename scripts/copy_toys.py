#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a tool to crab toys stored in one direction and copy them to another directory. ARG corresponds to the path to the directory containing the toy files. This tool is needed for MSSMvsSM hypotheses testing, since more than one person will produce toys")
parser.add_option("-o", "--output", dest="output", default="LIMITS-ddmmyy-mssm/bbb-hypo/cmb", type="string",
                  help="Path to the directories in which the mass dirs containing the toy files are. [Default: \"LIMITS-ddmmyy-mssm/bbb-hypo/cmb\"]")
parser.add_option("-n", "--name", dest="name", default="test", type="string",
                  help="some random name to make sure files will not be overwritten. [Default: \"test\"]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="increase verbosity. [Default: False]")
parser.add_option("--lowmH", dest="lowmH", default=False, action="store_true",
                  help="Turn on if lowmH toys shall be copied. [Default: False]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os
import re
from operator import itemgetter, attrgetter

if not options.lowmH :
    for mass in ['90', '100', '120', '130', '140', '160', '180', '200', '250', '300', '350', '400', '450', '500', '600', '700', '800', '900', '1000'] :
        directoryList = os.listdir("{DIR}/{MASS}".format(DIR=args[0], MASS=mass))
        os.system("mkdir {OUTPUT}/{MASS}".format(MASS=mass, OUTPUT=options.output))
        for file in directoryList :
            if re.match(r"point_\d+?_\d+(.\d\d)?.root$", file) : 
                #tanb_string = file[file.rfind("_")+1:]
                print "cp {DIR}/{MASS}/{FILE} {OUTPUT}/{MASS}/{FILECORR}_{NAME}".format(DIR=args[0], FILE=file, FILECORR=file.replace(mass+"_",""), MASS=mass, OUTPUT=options.output, NAME=options.name)
                os.system("cp {DIR}/{MASS}/{FILE} {OUTPUT}/{MASS}/{FILECORR}_{NAME}".format(DIR=args[0], FILE=file, FILECORR=file.replace(mass+"_",""), MASS=mass, OUTPUT=options.output, NAME=options.name))
                
else :
    for mass in ['300', '400', '500', '600', '700', '800', '900', '1000', '1100', '1200', '1300', '1400', '1500', '1600', '1700', '1800', '1900', '2000', '2100', '2200', '2300', '2400', '2500', '2600', '2700', '2800', '2900', '3000', '3100'] :
        directoryList = os.listdir("{DIR}/{MASS}".format(DIR=args[0], MASS=mass))
        os.system("mkdir {OUTPUT}/{MASS}".format(MASS=mass, OUTPUT=options.output))
        for file in directoryList :
            if re.match(r"point_\d+?_\d+(.\d\d)?.root$", file) : 
                #tanb_string = file[file.rfind("_")+1:]
                print "cp {DIR}/{MASS}/{FILE} {OUTPUT}/{MASS}/{FILECORR}_{NAME}".format(DIR=args[0], FILE=file, FILECORR=file.replace(mass+"_",""), MASS=mass, OUTPUT=options.output, NAME=options.name)
                os.system("cp {DIR}/{MASS}/{FILE} {OUTPUT}/{MASS}/{FILECORR}_{NAME}".format(DIR=args[0], FILE=file, FILECORR=file.replace(mass+"_",""), MASS=mass, OUTPUT=options.output, NAME=options.name))

            
