#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG", description="This is a script to transform the NLL for the calculation of the signal strength modified mu into a delta NLL for the estimate of the mass of the new particle. This has to be done across all available masses in the directory pointed to by ARG. As function of the mass the minimal absolute NLL is determined and substracted from the other minimal NLLs.")
parser.add_option("--histname", dest="histname", default="higgsCombineMLFIT*.root", type="string",
                  help="You can configure the name of the histogram files that you are looking for via this option. [Default: \"higgsCombineMLFIT*.root\"]")
parser.add_option("--verbose", dest="verbose", default=False, action="store_true",
                  help="Run in verbose mode. [Default: False]")
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import re
import os
import sys
import glob
from ROOT import *

def trunc(front, list) :
    """
    Remove the front part from each object in list 
    """
    newlist = []
    for elem in list :
        ## this interesting construction should work even for double slashes
        newlist.append(elem[len(front):].replace('/', ' ').strip().rstrip())
    return newlist

def minimalNLL(main, histname, verbose) :
    """
    Determine the minimal NLL across all masses in main. 
    """
    dirs = glob.glob(main+'/[0-9]*/')
    ## create list of file references from the directory with the largest number of apropriate files
    max=0; files=[]
    for dir in dirs :
        if len(glob.glob(dir+'/'+histname))>max :
            files = trunc(dir, glob.glob(dir+'/'+histname))
    print "# Files to process:", len(files), "(this can take a few minutes...)"
    print "# --------------------------------------------------------------------------------------"
    ## for each file go through all directories in dirs, read the nll value from the output files into a buffer, from the
    ## buffer determine the global minimum as function of the mass. Then go through all directories in dirs again, create
    ## a new output file with the original nll value minus the global minimum as function of the mass.  
    for file in files :
        nlls = {}
        ## determine mHXXX label
        matcher = re.compile('\w*\.?(?P<MASS_LABEL>mH\d+\.?\d*)\w*')
        refmass = matcher.match(file).group('MASS_LABEL')
        ## loop all trees in all output files and determine nll for each given mass value 
        for dir in dirs :
            mass = 'mH'+dir[len(main):].replace('/', ' ').strip().rstrip()
            root = TFile(dir+file.replace(refmass, mass))
            if root :
                tree = root.FindObjectAny('limit')
                if tree :
                    for event in tree :
                        nlls[dir] = event.limit
                root.Close()
        ## issue a warning if one directory is missing in the dictionary.
        for dir in dirs :
            if not dir in nlls.keys() :
                print "Warning: file:", file, "was not found in directory:", dir
        ## determine minimal value and subtract it from all values, make sure that this happens by reference and not by value
        globnll = min(nlls.values())
        for idx in range(len(nlls)) :
            nlls[nlls.keys()[idx]]-= globnll
        ## write modified nlls back to file
        gROOT.ProcessLine(
            "struct buffer_t {\
            Float_t limit;\
            };"
            );
        for (dir,nll) in nlls.iteritems() :
            buffer = buffer_t()
            mass = 'mH'+dir[len(main):].replace('/', ' ').strip().rstrip()
            root = TFile(dir+file.replace(refmass, mass)+'_modified', 'RECREATE')
            tree = TTree('limit', 'limit')
            tree.Branch('limit', buffer, 'limit/F')
            buffer.limit = float(nll)
            tree.Fill()
            tree.Write()
            root.Close()
    ## remove original files and replace by modified files. Make sure that any original files were not contained in the mass
    ## directory that served as reference for files are also removed, as they will destroy the band otherwise. (In principle
    ## this is not needed any more after the dir with the largest number of files gives the reference for files).
    for dir in dirs :
        mass = 'mH'+dir[len(main):].replace('/', ' ').strip().rstrip()
        for file in files :
            os.system('rm {DIR}/{FILE}'.format(DIR=dir, FILE=file.replace(refmass, mass)))
            os.system('mv {DIR}/{FILE}_modified {DIR}/{FILE}'.format(DIR=dir, FILE=file.replace(refmass, mass)))
            
print "# --------------------------------------------------------------------------------------"
print "# Subtracting global minimum from NLL. "
print "# --------------------------------------------------------------------------------------"
print "# You are using the following configuration: "
print "# --histname          :", options.histname
print "# Check option --help in case of doubt about the meaning of one or more of these confi-"
print "# guration parameters.                           "
print "# --------------------------------------------------------------------------------------"
minimalNLL(args[0], options.histname, options.verbose)
