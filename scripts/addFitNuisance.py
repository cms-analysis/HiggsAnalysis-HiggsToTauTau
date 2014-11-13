#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]", description="Script to fit the tails to functions compute shape high and low nuisances and propagate them to the analysis")
parser.add_option("-i"  ,"--input",          dest="input",          default="test.root",  type="string", help="Input file where to find the signal histograms (or workspaces). [Default: test.root]")
parser.add_option("-b"  ,"--background",     dest="background",     default="TT QCD EWK", type="string",   help="Template to change [TT QCD EWK]")
parser.add_option("-n"  ,"--name",           dest="name",           default="shift",      type="string", help="shift")
parser.add_option("-e"  ,"--energy",         dest="energy",         default="8TeV",       type="string", help="Energy [Default: 8 TeV]")
parser.add_option("-c"  ,"--channel",        dest="channel",        default="tt",         type="string", help="channel [Default: tt]")
parser.add_option("-k"  ,"--categories",     dest="categories",     default="8 9",        type="string", help="Categories [Default: 8 9 ]")
parser.add_option("-r"  ,"--range",          dest="first",          default="200",        type="int",    help="Beginning of fit range [Default: 200]")
parser.add_option("-l"  ,"--rangelast",      dest="last",           default="1500",       type="int",    help="End of fit range [Default: 1500]")
parser.add_option(""    ,"--fitoption",      dest="fitoption",      default="0",          type="int",    help="Fit option 0('legacy' analysis) 1(new MSSM analysis) [Default:0]")
parser.add_option("-f"  ,"--fitmodel",       dest="fitmodel",       default="0",          type="int",    help="Fit model 0(exp(m/(a+b*m)) 1(exp(a*m*pow(b)) [Default:0]")
parser.add_option(""    ,"--erroroption",    dest="erroroption",    default="0",          type="int",    help="Error option 0('legacy' analysis) 1(new MSSM analysis) 2(experimental) [Default:0]")
parser.add_option(""    ,"--extrapoloption", dest="extrapoloption", default="0",          type="int",    help="Extrapolation option 0('legacy' analysis) 1(continue as constant function with large errors) 2(keep original bins) [Default:0]")
parser.add_option("-o"  ,"--varbin",         dest="varbin",         default=False, action="store_true",  help="Use variable binned fits    [Default: False]")
parser.add_option("-s"  ,"--setup",          dest="setup",          default="HiggsAnalysis/HiggsToTauTau/setup",    type="string",  help="Setup Directory : HiggsAnalysis/HiggsToTauTau/setup")
parser.add_option("-v"  ,"--verbose",        dest="verbose",        default=False, action="store_true",  help="increase verbosity and make extra plots. [Default: False]")
parser.add_option("-u"  ,"--no-uncerts",     dest="no_uncerts",     default=False, action="store_true",  help="do not write uncertainties on fit parameters to file (used when providing central fits for shape uncertainties to prevent double counting of fit uncertainties). Should be False for the fit of the central value. [Default: False]")
parser.add_option("-t"  ,"--testmode",       dest="testmode",       default=False, action="store_true",  help="run in test mode-performs fit and makes plots but doesn't alter datacard or uncertainty files. [Default: False]")

# check number of arguments; in case print usage
(options, args) = parser.parse_args()
#if len(args) < 1 :
#    parser.print_usage()
#    exit(1)

import os
import re
import sys as system

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs 

## mapping out signals
channelName = {
    "mm" : "mumu",
    "em" : "emu",
    "et" : "eleTau",
    "mt" : "muTau",
    "tt" : "tauTau"
}

categoryName = {
    "8"  : "nobtag",
    "9"  : "btag",
    "10" : "nobtag_low",
    "11" : "nobtag_medium",
    "12" : "nobtag_high",
    "13" : "btag_low",
    "14" : "btag_high"
}


print " You are running with configuration: "
print "-------------------------------------"
print " input        : ", options.input
print " template     : ", options.background
print " energy       : ", options.energy
print " channel      : ", options.channel
print " categories   : ", options.categories
print " drop uncerts : ", options.no_uncerts
print " channel      : ",  channelName[options.channel]

## add shift Nuisance (ignore the VBF Option right now)
os.system(r"root -l -q -b {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/compileAddFitNuisance.C".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))
os.system(r"cp {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rootlogon.C .".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))

os.system("cp %s %s.bak"      %  (options.setup+'/'+options.channel+'/'+options.input,options.setup+'/'+options.channel+'/'+options.input))
for cat in options.categories.split() :
    for bkg in options.background.split() : 
        status = os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/addFitNuisance.C+\(\"{FILENAME}\"\,\"{CHANNEL}\"\,\"{BKG}\"\,\"{ENERGY}\"\,\"{NAME}\"\,\"{CATEGORY}\"\,{FIRST}\,{LAST}\,{FITOPTION}\,{FITMODEL}\,{ERROROPTION}\,{EXTRAPOLOPTION}\,{VERBOSE}\,{VARBIN}\,{UNCERTS}\,{TESTMODE}\)".format(
            CMSSW_BASE=os.environ.get("CMSSW_BASE"), FILENAME=options.setup+'/'+options.channel+'/'+options.input,CHANNEL=channelName[options.channel],BKG=bkg,ENERGY=options.energy,NAME=options.name,CATEGORY=cat,FIRST=options.first,LAST=options.last,FITOPTION=options.fitoption,FITMODEL=options.fitmodel,ERROROPTION=options.erroroption,EXTRAPOLOPTION=options.extrapoloption,VERBOSE=str(options.verbose).lower(),VARBIN=str(options.varbin).lower(),UNCERTS=str(not options.no_uncerts).lower(),TESTMODE=str(options.testmode).lower()))
        if int(status) > 0:
            system.exit(1)
        os.system("rm %s"      %  (options.setup+'/'+options.channel+'/'+options.input))
        os.system("mv Output.root %s" %  (options.setup+'/'+options.channel+'/'+options.input))

for cat in options.categories.split() :
    if cat == ' ' :
        continue
## add Nuisance to the vals
    if not options.no_uncerts : 
        datacard=options.setup+'/'+options.channel+'/unc-mssm-'+options.energy+('-%02i'% int(cat))+'.vals'
        print "datacard: ",datacard
        old = open(datacard, 'r')
        new = open("%s-tmp.txt" % datacard[0:datacard.rfind('.txt')], 'w')
        for line in old :
            words = line.split()
            new.write(line )
            if len(words) < 2 :
                continue
            if '#' in words[0] :
                continue
            #if ('_scale_t_' or '_scale_e_') in words[2] :
            if  words[2].find('_scale_t_')>-1 or words[2].find('_scale_e_')>-1 :
                new_words    = words 
                new_words[1] = options.background.replace(' ',',').replace("_fine_binning", "")
                new_words[2] = 'CMS_'+options.name+'1_' + channelName[options.channel] + '_' + categoryName[cat] + '_' + options.energy + "_" + options.background
                new_line1     = '                      '.join(new_words)
                new_words[2] = 'CMS_'+options.name+'2_' + channelName[options.channel] + '_' + categoryName[cat] + '_' + options.energy + "_" + options.background
                new_line2     = '                      '.join(new_words)
                new.write(new_line1+'\n')
                new.write(new_line2+'\n')
        old.close()
        new.close()
        os.system("mv %s-tmp.txt %s" % (datacard[0:datacard.rfind('.txt')], datacard))           

## add Nuisance to the conf
        datacard=options.setup+'/'+options.channel+'/unc-mssm-'+options.energy+('-%02i'% int(cat))+'.conf'
        print "datacard: ",datacard
        old = open(datacard, 'r')
        new = open("%s-tmp.txt" % datacard[0:datacard.rfind('.txt')], 'w')
        for line in old :
            new.write(line )
            words = line.split()
            if len(words) < 2 :
                continue
            if '#' in words[0] :
                continue
            #if  ('_scale_t_' or '_scale_e_') in words[0] :
            if  words[0].find('_scale_t_')>-1 or words[0].find('_scale_e_')>-1 :
                new_words    = words 
                new_words[0] = 'CMS_'+options.name+'1_' + channelName[options.channel] + '_' + categoryName[cat] + '_' + options.energy + '_' + options.background
                new_line1     = '                      '.join(new_words)
                new_words[0] = 'CMS_'+options.name+'2_' + channelName[options.channel] + '_' + categoryName[cat] + '_' + options.energy + '_' + options.background
                new_line2     = '                      '.join(new_words)
                new.write(new_line1+'\n')
                new.write(new_line2+'\n')
        new.close()
        old.close()
        os.system("mv %s-tmp.txt %s" % (datacard[0:datacard.rfind('.txt')], datacard))           

