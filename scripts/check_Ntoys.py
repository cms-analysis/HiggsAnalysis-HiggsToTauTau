#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a tool to print out the number toys for each gridpoint. ARG corresponds to the path to the directory containing the toy files.")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="increase verbosity. [Default: False]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os
from operator import itemgetter, attrgetter

for mass in ['90', '100', '120', '130', '140', '160', '180', '200', '250', '300', '350', '400', '450', '500', '600', '700', '800', '900', '1000'] :
    
    directoryList = os.listdir("{DIR}".format(DIR=args[0]))
    for file in directoryList :
        if re.match(r"numberToys_{MASS}_\d+(.\d\d)?.out".format(MASS=mass), file) :            
            Ntoys = open("numberToys_{MASS}_{TANB}.out".format(MASS=mass, TANB=file[file.rfind("_")+1:].rstrip(".out")), 'r')
            lines = Ntoys.readlines()
            Ntoys.close()
            for line in lines :
                words = line.split(" ")
                print "mass", words[0], "tanb", words[1], "ntoys", words[2]
