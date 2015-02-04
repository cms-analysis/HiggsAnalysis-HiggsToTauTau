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
                      description="This is a script to merge H+->tau nu shape files. ARG corresponds to the *root files which should get merged.")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="Run in verbose mode")
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

hists = []

outputfile = ROOT.TFile("combine_histograms_hplushadronic_light.root", "RECREATE")

for arg in args :
    print arg
    mass=arg.rstrip(".root").split("_")[-1].lstrip("m")
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
        if "CMS_ttHpHp_signal" in name.GetName() :
            newnames=name.GetName().split("signal")
            newname=newnames[0]+"signal"+mass+newnames[-1]
            if "statBin" in name.GetName() :
                newname=newnames[0]+"signal"+mass+"_"+newnames[0]+"signal"+newnames[-1]
            #print newname
            hist.SetTitle(newname)
            hist.SetName(newname)
        if "CMS_ttHpW_signal" in name.GetName() :
            newnames=name.GetName().split("signal")
            newname=newnames[0]+"signal"+mass+newnames[-1]
            if "statBin" in name.GetName() :
                newname=newnames[0]+"signal"+mass+"_"+newnames[0]+"signal"+newnames[-1]
            #print newname
            hist.SetTitle(newname)
            hist.SetName(newname)
        if newname!="":
            hist.Write(newname)
        else :
            hist.Write()
            
        hists.append(hist.GetName())
        
outputfile.Close()
#print hists

#hoirzontal template morphing needed for 130
os.system("horizontal-morphing.py --categories='' --samples='CMS_ttHpHp_signal{MASS},CMS_ttHpW_signal{MASS}' --uncerts='' --masses='120,140' --step-size 10. -v combine_histograms_hplushadronic_light.root".format(MASS="{MASS}"))
