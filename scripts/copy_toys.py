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
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os
from operator import itemgetter, attrgetter

for mass in ['90', '100', '120', '130', '140', '160', '180', '200', '250', '300', '350', '400', '450', '500', '600', '700', '800', '900', '1000'] :
    directoryList = os.listdir("{DIR}".format(DIR=args[0]))
    for file in directoryList :    
        print "cp {DIR}/{FILE} {OUTPUT}/{MASS}/{FILE}_{NAME}".format(DIR=args[0], FILE=file, MASS=mass, OUTPUT=options.output, NAME=options.name)   
        os.system("cp {DIR}/{FILE} {OUTPUT}/{MASS}/{FILE}_{NAME}".format(DIR=args[0], FILE=file, MASS=mass, OUTPUT=options.output, NAME=options.name))
