#!/usr/bin/env pythonimport glob

import os
import re
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

#ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so')
#from ROOT import th1fmorph

from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to merge H+ shape files.")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="Run in verbose mode")
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

hists = []

outputfile = ROOT.TFile("combined.root", "RECREATE")

for arg in args :
    print arg
    
    file = ROOT.TFile(arg, "READ")
    if not file :
        print "file not found: ", arg
    file.cd()

    for name in ROOT.gDirectory.GetListOfKeys():
        hist = file.Get(name.GetName())
        
        if hist.GetName() in hists :
            continue

        outputfile.cd()
        newname=""
        if "HH" in name.GetName() :
            newnames=name.GetName().split("_a")
            newname=newnames[0]+newnames[-1]
            if "statBin" in name.GetName() :
                newname=newnames[0]+"_HH"+newnames[-1]
            hist.SetTitle(newname)
            hist.SetName(newname)
        if "HW" in name.GetName() :
            newnames=name.GetName().split("_a")
            newname=newnames[0]+newnames[-1]
            if "statBin" in name.GetName() :
                newname=newnames[0]+"_HW"+newnames[-1]
            hist.SetTitle(newname)
            hist.SetName(newname)
        if newname!="":
            hist.Write(newname)
        else :
            hist.Write()
            
        hists.append(hist.GetName())

#print hists
