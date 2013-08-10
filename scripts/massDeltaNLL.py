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

def minimalNLL(main, histname, verbose) :
    """
    Determine the minimal NLL across all masses in main. 
    """
    jobs = []; refs = []
    dirs = glob.glob(main+'/[0-9]*/')
    ## filter out the jobID from a general root output file name of combine
    matcher = re.compile('\w*\.?mH\d+\.?\d*-(?P<JOBID>[0-9]+)-\d+\.?\d*\.?\w*')
    ## create list of file references from the directory with the largest number of apropriate files
    print "# Number of toys per directory:"
    for dir in sorted(dirs) :
        print "# ", dir, "\t:", len(glob.glob(dir+'/'+histname))
        for x in glob.glob(dir+'/'+histname) :
            jobId = matcher.match(x[x.rfind('/')+1:]).group('JOBID')
            jobs.append(jobId)
    print "# --------------------------------------------------------------------------------------"            
    for job in list(set(jobs)) :
        if jobs.count(job) == len(dirs) :
            refs.append(job)
    refs = sorted(refs)
    print "# Number of toys to process:", len(refs), "(this can take a few minutes...)"
    print "# --------------------------------------------------------------------------------------"
    ## for each file go through all directories in dirs, read the nll value from the output files into a buffer, from the
    ## buffer determine the global minimum as function of the mass. Then go through all directories in dirs again, create
    ## a new output file with the original nll value minus the global minimum as function of the mass.
    corrupt = []
    dropped = dict((k, []) for k in dirs)
    globnll = dict((l, dict((k, -1) for k in dirs)) for l in refs)
    ## loop all trees in all output files and determine nll for each given mass value 
    for dir in dirs :
        for file in glob.glob(dir+'/'+histname) :
            jobId = matcher.match(file[file.rfind('/')+1:]).group('JOBID')
            if jobId in refs :
                succeed = False
                root = TFile(file)
                if root :
                    tree = root.FindObjectAny('limit')
                    if tree :
                        for event in tree :
                            globnll[jobId][dir] = event.limit
                            succeed = True
                    root.Close()
                if not succeed :
                    ## spotted corrupted root output file -> remove from list of valid jobs
                    if verbose :
                        print "Warning: output file corrupted - toy", jobId, " will be removed from list of toys."
                    refs = filter(lambda x: x != jobId, refs)
                    dropped[dir].append(jobId)
                    if jobId not in corrupt :
                        corrupt.append(jobId)
    ## remove jobs which included corrupted files
    for jobId in corrupt :
        del  globnll[jobId]
    ## and subtract it from all values, make sure that this happens by reference and not by value
    for job in globnll.keys() :
        globmin = min(globnll[job].values())
        for dir in globnll[job].keys() :
            globnll[job][dir]-= globmin    
    ## write modified nlls back to file
    gROOT.ProcessLine(
        "struct buffer_t {\
        Double_t limit;\
        };"
        );
    for dir in dirs :
        for file in glob.glob(dir+'/'+histname) :
            jobId = matcher.match(file[file.rfind('/')+1:]).group('JOBID')
            if jobId in globnll.keys() :    
                buffer = buffer_t()
                root = TFile(file+'_modified', 'RECREATE')
                tree = TTree('limit', 'limit')
                tree.Branch('limit', buffer, 'limit/D')
                buffer.limit = float(globnll[jobId][dir])
                tree.Fill()
                tree.Write()
                root.Close()                
    ## remove original files and replace by modified files. Make sure that any original files were not contained in the mass
    ## directory that served as reference for files are also removed, as they will destroy the band otherwise. (In principle
    ## this is not needed any more after the dir with the largest number of files gives the reference for files).
    for dir in dirs :
        for file in glob.glob(dir+'/'+histname) :
            if os.path.exists(file) :
                os.system('rm {FILE}'.format(FILE=file))
            if os.path.exists(file+'_modified') :
                os.system('mv {FILE}_modified {FILE}'.format(FILE=file))
    return (len(refs), dropped)

print "# --------------------------------------------------------------------------------------"
print "# Subtracting global minimum from NLL. "
print "# --------------------------------------------------------------------------------------"
print "# You are using the following configuration: "
print "# --histname          :", options.histname
print "# Check option --help in case of doubt about the meaning of one or more of these confi-"
print "# guration parameters.                           "
print "# --------------------------------------------------------------------------------------"
processed_jobs = minimalNLL(args[0], options.histname, options.verbose)
print "# Number of processed toys :", processed_jobs[0]
print "# --------------------------------------------------------------------------------------"
print "# Number of corrupted toys :"
for dir in sorted(processed_jobs[1]) :
    print "# ", dir, "\t:", len(processed_jobs[1][dir])
print "# --------------------------------------------------------------------------------------"
