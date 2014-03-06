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
import re

for mass in ['90', '100', '120', '130', '140', '160', '180', '200', '250', '300', '350', '400', '450', '500', '600', '700', '800', '900', '1000'] :   
    directoryList = os.listdir("{DIR}/{MASS}".format(DIR=args[0], MASS=mass))
    checked = False
    for file in directoryList :
        if re.match(r"numberToys_{MASS}_\d+(.\d\d)?.out".format(MASS=mass), file) :
            checked = True
            Ntoys = open("{DIR}/{MASS}/numberToys_{MASS}_{TANB}.out".format(DIR=args[0], MASS=mass, TANB=file[file.rfind("_")+1:].rstrip(".out")), 'r')
            lines = Ntoys.readlines()
            Ntoys.close()
            for line in lines :
                words = line.split(" ")
                print "mass", words[0], "tanb", words[1], "ntoys", words[2]
    if not checked :
        print "No toy file for mass", mass
