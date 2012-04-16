#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...",
                      description="Script for comprehensive crabjob submission for htt MSSM and SM limits and for the combination of all Higgs channels. ARG1, ARG2, ARG3, ... correspond to the job directories for the submission. These directories should contain the all datacards and input files needed for the limit calculation. Dedicated options can be fed through to the submit-slave.py via the option --options, enbraced by '...'.")
parser.add_option("-n", "--cycles", dest="cycles", default=1, type="int", help="Number of submission cycles (one submission cycle consists of 50 crabjobs). [Default: 1]")
parser.add_option("-s", "--setup", dest="setup", default="htt-mssm", type="choice", help="Limit calculation setup [Default: htt-mssm]", choices=["hww-mssm", "htt-mssm", "htt-sm", "cmb"])
parser.add_option("-m", "--method", dest="method", default="CLs", type="choice", help="Limit calculation method [Default: CLs]", choices=["Bayesian", "CLs", "tanb", "tanb+", "single"])
parser.add_option("--options", dest="opt", default="", type="string", help="String for additional options for testing (enclosed by \"...\"). [Default: \"\"]")
mgroup = OptionGroup(parser, "HIGGS COMBINATION COMMAND OPTIONS", "Command options for the use with --setup cmb.")
mgroup.add_option("-b", "--boundaries", dest="bound", default="cmb", type="choice", help="Optimized CLs grid boundaries for a given channel (to be used for submissions together with option --setup \"cmb\") [Default: cmb]", choices=["cmb", "htt", "hgg", "hbb", "hww", "hzz4l", "hzz2l2q", "hzz2l2nu", "hzz2l2t"])
parser.add_option_group(mgroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import re
import os

## create a subvector of a vector of strings that contains
## an integer and a '/' as substring 
def subvec(vec, min, max):
    subvec = []
    for directory in vec :
        if re.search(r"^.*/\d+?$", directory) :
            mass = int(directory[directory.rfind("/")+1:])
            if min <= mass and mass <= max:
                subvec.append(directory)
    return subvec

## return a string concatenated from elements of a vector
## seperate these elements by a deliminator as specified
## by delim; default is " "
def vec2str(vec, delim=" "):
    str = ""
    for i in vec:
        str+=i
        str+=delim
    return str

if options.setup == "hww-mssm" :
    cycle = options.cycles
    while cycle>0 :
        print "***********************************************************"
        print " %s cycle(s) to finish" % cycle
        print "***********************************************************"
        if options.method == "tanb" :
            ## three submits depending on the mass
            if len(subvec(args,  90, 249))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min  1.0  --max  3.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min  3.2  --max  5.4 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
                os.system("submit-slave.py --bin combine --method tanb -n  2 --min  6.0  --max  7.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
            if len(subvec(args, 250, 299))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min 10.0  --max 66.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 250, 299))))
            if len(subvec(args, 300, 550))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min  2.0  --max 22.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 300, 550))))
                os.system("submit-slave.py --bin combine --method tanb -n  5 --min 26.0  --max 66.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 300, 550))))
        if options.method == "tanb+" :
            ## three submits depending on the mass
            if len(subvec(args,  90, 249))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min  1.0  --max  2.8 --interactive %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
                os.system("submit-slave.py --bin combine --method tanb -n 11 --min  3.0  --max  5.0 --interactive %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
                os.system("submit-slave.py --bin combine --method tanb -n  2 --min  6.0  --max  7.0 --interactive %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
            if len(subvec(args, 250, 299))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min 10.0  --max 65.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 250, 299))))
            if len(subvec(args, 300, 550))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 11 --min  2.0  --max 22.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 300, 550))))
                os.system("submit-slave.py --bin combine --method tanb -n  6 --min 26.0  --max 66.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 300, 550))))                
        cycle = cycle-1
        
if options.setup == "htt-mssm" :
    cycle = options.cycles
    while cycle>0 :
        print "***********************************************************"
        print " %s cycle(s) to finish" % cycle
        print "***********************************************************"
        if options.method == "single" :
            ## submit a single job in all directories you can find the signal strength grid has to be
            ## taken into account in structure of the sub-directories already
            if len(subvec(args,  90, 249))>0 :
                os.system("submit-slave.py --bin combine --method single --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
            if len(subvec(args, 250, 399))>0 :
                os.system("submit-slave.py --bin combine --method single --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 250, 399))))
            if len(subvec(args, 400, 500))>0 :
                os.system("submit-slave.py --bin combine --method single --toysH 100 -t 100 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 400, 500))))
        if options.method == "tanb" :
            ## three submits depending on the mass
            if len(subvec(args,  90, 249))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min  5.0  --max 14.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
                os.system("submit-slave.py --bin combine --method tanb -n  6 --min 15.0  --max 30.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
                os.system("submit-slave.py --bin combine --method tanb -n  4 --min 40.0  --max 70.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
            if len(subvec(args, 250, 299))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min  5.0  --max 14.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 250, 299))))
                os.system("submit-slave.py --bin combine --method tanb -n  5 --min 16.0 --max  24.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 250, 299))))
                os.system("submit-slave.py --bin combine --method tanb -n  5 --min 30.0 --max  70.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 250, 299))))
            if len(subvec(args, 300, 399))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n  8 --min  8.0  --max 22.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 300, 399))))
                os.system("submit-slave.py --bin combine --method tanb -n  6 --min 25.0  --max 40.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 300, 399))))
                os.system("submit-slave.py --bin combine --method tanb -n  6 --min 45.0  --max 70.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 300, 399))))
            if len(subvec(args, 400, 499))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min 12.0  --max 39.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 400, 499))))
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min 42.0  --max 69.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 400, 499))))
            if len(subvec(args, 500, 550))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n  9 --min 18.0  --max 42.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 500, 550))))
                os.system("submit-slave.py --bin combine --method tanb -n  9 --min 45.0  --max 69.0 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 500, 550))))
        if options.method == "tanb+" :
            ## three submits depending on the mass
            if len(subvec(args,  90, 249))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min  5.0  --max 14.0 --interactive %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
                os.system("submit-slave.py --bin combine --method tanb -n  6 --min 15.0  --max 30.0 --interactive %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
                os.system("submit-slave.py --bin combine --method tanb -n  4 --min 40.0  --max 70.0 --interactive %s %s" % (options.opt, vec2str(subvec(args,  90, 249))))
            if len(subvec(args, 250, 299))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min  5.0  --max 14.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 250, 299))))
                os.system("submit-slave.py --bin combine --method tanb -n  5 --min 16.0  --max 24.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 250, 299))))
                os.system("submit-slave.py --bin combine --method tanb -n  5 --min 30.0  --max 70.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 250, 299))))
            if len(subvec(args, 300, 399))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n  8 --min  8.0  --max 22.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 300, 399))))
                os.system("submit-slave.py --bin combine --method tanb -n  6 --min 25.0  --max 40.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 300, 399))))
                os.system("submit-slave.py --bin combine --method tanb -n  6 --min 45.0  --max 70.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 300, 399))))
            if len(subvec(args, 400, 499))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min 12.0  --max 39.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 400, 499))))
                os.system("submit-slave.py --bin combine --method tanb -n 10 --min 42.0  --max 69.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 400, 499))))
            if len(subvec(args, 500, 550))>0 :
                os.system("submit-slave.py --bin combine --method tanb -n  9 --min 18.0  --max 42.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 500, 550))))
                os.system("submit-slave.py --bin combine --method tanb -n  9 --min 45.0  --max 69.0 --interactive %s %s" % (options.opt, vec2str(subvec(args, 500, 550))))
        if options.method == "CLs" :
            ## three submits depending on the mass
            if len(subvec(args,  90, 119))>0 :
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min   0.25  --max  20.25 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 119))))
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min  25.25  --max  75.25 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 119))))
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min  95.25  --max 295.25 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 119))))
            if len(subvec(args, 120, 300))>0 :
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min   0.05  --max   2.05 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 120, 500))))
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min   2.25  --max  20.25 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 120, 500))))
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min  23.35  --max  63.25 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 120, 500))))
            if len(subvec(args, 350, 500))>0 :
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min  0.005  --max  0.105 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 120, 500))))
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min  0.130  --max  0.380 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 120, 500))))
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min  0.500  --max  1.700 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args, 120, 500))))                                
        if options.method == "Bayesian" :
            if len(subvec(args,  90, 500))>0 :
                os.system("submit-slave.py --bin combine --method Bayesian -t 1000 -j 100 --server --random --priority %s %s" % (options.opt, vec2str(subvec(args, 90, 500))))
        cycle = cycle-1
        
if options.setup == "htt-sm" :
    cycle = options.cycles
    while cycle>0 :
        print "***********************************************************"
        print " %s cycle(s) to finish" % cycle
        print "***********************************************************"    
        if options.method == "CLs" :
            ## three submits depending on the mass
            if len(subvec(args, 90, 150))>0 :
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min   0.5  --max   5.5 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 150))))
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min   8.5  --max  38.5 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 150))))
                os.system("submit-slave.py --bin combine --method CLs -n 11 --min  68.5  --max 368.5 --toysH 100 -t 200 -j 100 --random --server --priority %s %s" % (options.opt, vec2str(subvec(args,  90, 150))))
        if options.method == "Bayesian" :
            if len(subvec(args, 90, 150))>0 :
                os.system("submit-slave.py --bin combine --method Bayesian -t 1000 -j 100 --server --random --priority %s %s" % (options.opt, vec2str(subvec(args, 90, 150))))
        cycle = cycle-1

if options.setup == "cmb" :
    cycle = options.cycles
    while cycle>0 :
        print "***********************************************************"
        print " %s cycle(s) to finish" % cycle
        print "***********************************************************"            
        for directory in args :
            if directory.find("common")>-1 :
                print "> skipping directory common"
                continue 
            mass = int(directory[directory.rfind("/")+1:])
            ## search for limit boundaries corresponding to mass point and submit
            found = False
            CMSSW_BASE = os.environ["CMSSW_BASE"]                
            f = open("%s/src/datacards/bounds/%s.bnd" % (CMSSW_BASE, options.bound))
            for line in f:
                line = line.strip().split("\n")[0].strip()
                if line == "" or line.startswith("#") or line.startswith("%"):
                    continue
                wordarr = line.strip().split()
                if mass == int(wordarr[0]) :
                    found = True
                    if options.method == "CLs" :
                        ## submit on a grid with three different granularities if configures such
                        if float(wordarr[1])>0 and float(wordarr[2])>0 :
                            os.system("submit-slave.py --bin combine --method CLs -n 11 --min %s --max %s --toysH 50 -t 100 -j 50 --random --server --priority %s %s" %
                                      (wordarr[1], wordarr[2], options.opt, directory))
                        if float(wordarr[3])>0 and float(wordarr[4])>0 :
                            os.system("submit-slave.py --bin combine --method CLs -n 11 --min %s --max %s --toysH 50 -t 100 -j 50 --random --server --priority %s %s" %
                                      (wordarr[3], wordarr[4], options.opt, directory))
                        if float(wordarr[5])>0 and float(wordarr[6])>0 :
                            os.system("submit-slave.py --bin combine --method CLs -n 11 --min %s --max %s --toysH 50 -t 100 -j 50 --random --server --priority %s %s" %
                                      (wordarr[5], wordarr[6], options.opt, directory))
                    if options.method == "Bayesian" :
                        os.system("submit-slave.py --bin combine --method Bayesian -H None --rMin %s --rMax %s -t 250 -j 50 --server --random --priority %s %s %s" %
                                  ((float(wordarr[1])+float(wordarr[2]))/2, (float(wordarr[5])+float(wordarr[6]))/2, ("--observed" if cycle==1 else ""), options.opt, directory))
            if not found :
                print "Did not find mass point for directory %s in file cls-%s.bnd" % (directory, options.bound)
        cycle = cycle-1
