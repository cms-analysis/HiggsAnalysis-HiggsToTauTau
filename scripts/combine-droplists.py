#!/usr/bin/env python
#flake8: noqa
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="This is a script to combine multiple droplists generated from prune-uncerts.py or scripts derived from this script w/o double counting. It prompts the number of nuisance parameters in the combined droplist to the shell.")
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import glob
import os

## list of combined uncerts
combined_uncerts = []
individual_uncerts = {}

## read uncerts from individual files 
for path in args :
    uncerts = []
    file = open(path, 'r')
    for unc in file :
        uncerts.append(unc)
        if not unc in combined_uncerts :
            combined_uncerts.append(unc)
        else :
            print "uncertainty: ", unc, "already in list."
    file.close()
    individual_uncerts[path] = uncerts

## write combined uncertainties back to a new file
file = open('uncertainty-pruning-drop.txt_combined', 'w')
for unc in combined_uncerts :
    file.write(unc)
file.close()

print "# --------------------------------------------------------------------------------------"
print "# Combining Droplists. "
print "# --------------------------------------------------------------------------------------"
print "# Individual files:"
for path,uncerts in individual_uncerts.iteritems() :
    print "# ", path, "\t : ", len(uncerts)
print "#"
print "# Combined", len(combined_uncerts), "uncertainties in file: uncertainty-pruning-drop.txt_combined."
print "# --------------------------------------------------------------------------------------"
