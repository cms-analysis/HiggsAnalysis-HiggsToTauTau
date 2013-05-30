#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to fit the tails to functions compute shape high and low nuisances and propagate them to the analysis")
parser.add_option("-i"  ,"--input", dest="input", default="test.root", type="string", help="Input file where to find the signal histograms (or workspaces). [Default: test.root]")
parser.add_option("-b"  ,"--background", dest="background", default="TT QCD EWK",      type="string",   help="Template to change [TT QCD EWK]")
parser.add_option("-n"  ,"--name",       dest="name",       default="shift",   type="string",   help="shift")
parser.add_option("-e"  ,"--energy",     dest="energy",     default="8TeV",    type="string",   help="Energy [Default: 8 TeV]")
parser.add_option("-c"  ,"--channel",    dest="channel",    default="tt",      type="string",   help="channel [Default: tauTau]")
parser.add_option("-k"  ,"--categories", dest="categories", default="8 9",     type="string",   help="Categories [Default: 8 9 ]")
parser.add_option("-s"  ,"--setup",      dest="setup",      default="HiggsAnalysis/HiggsToTauTau/setup",    type="string",  help="Setup Directory : HiggsAnalysis/HiggsToTauTau/setup")
parser.add_option("-v"  ,"--verbose",    dest="verbose",    default=False, action="store_true", help="increase verbosity. [Default: False]")

# check number of arguments; in case print usage
(options, args) = parser.parse_args()
#if len(args) < 1 :
#    parser.print_usage()
#    exit(1)

import os
import re

print " You are running with configuration: "
print "-------------------------------------"
print " input      : ", options.input
print " Template   : ", options.background
print " energy     : ", options.energy
print " channel    : ", options.channel
print " categories : ", options.categories

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs 

## mapping out signals
channelName = {
    "mm" : "mumu",
    "em" : "emu",
    "et" : "eleTau",
    "mt" : "muTau",
    "tt" : "tauTau"
    }

print " channel : ",  channelName[options.channel]
## add shift Nuisance (ignore the VBF Option right now)
os.system(r"cp {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rootlogon.C .".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))

for bkg in options.background.split() : 
    os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/addFitNuisance.C+\(\"{FILENAME}\"\,\"{CHANNEL}\"\,\"{BKG}\"\,\"{ENERGY}\"\,\"{NAME}\"\)".format(
        CMSSW_BASE=os.environ.get("CMSSW_BASE"), FILENAME=options.input,CHANNEL=channelName[options.channel],BKG=bkg,ENERGY=options.energy,NAME=options.name))

for cat in options.categories :
    if cat == ' ' :
        continue
## add Nuisance to the conf
    datacard=options.setup+'/'+options.channel+'/unc-mssm-'+options.energy+'-0'+cat+'.vals'
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
        if ('_scale_t_' or '_scale_e_') in words[2] :
            new_words    = words 
            new_words[1] = options.background
            new_words[2] = 'CMS_'+options.name+'1_' + channelName[options.channel] + '_' + options.energy
            new_line1     = '                      '.join(new_words)
            new_words[2] = 'CMS_'+options.name+'2_' + channelName[options.channel] + '_' + options.energy
            new_line2     = '                      '.join(new_words)
            new.write(new_line1+'\n')
            new.write(new_line2+'\n')
    old.close()
    new.close()
    os.system("mv %s-tmp.txt %s" % (datacard[0:datacard.rfind('.txt')], datacard))           

## add Nuisance to the vals
    datacard=options.setup+'/'+options.channel+'/unc-mssm-'+options.energy+'-0'+cat+'.conf'
    old = open(datacard, 'r')
    new = open("%s-tmp.txt" % datacard[0:datacard.rfind('.txt')], 'w')
    for line in old :
        new.write(line )
        words = line.split()
        if len(words) < 2 :
            continue
        if '#' in words[0] :
            continue
        if  ('_scale_t_' or '_scale_e_') in words[0] :
            new_words    = words 
            new_words[0] = 'CMS_'+options.name+'1_' + channelName[options.channel] + '_' + options.energy
            new_line1     = '                      '.join(new_words)
            new_words[0] = 'CMS_'+options.name+'2_' + channelName[options.channel] + '_' + options.energy
            new_line2     = '                      '.join(new_words)
            new.write(new_line1+'\n')
            new.write(new_line2+'\n')
    new.close()
    old.close()
    os.system("mv %s-tmp.txt %s" % (datacard[0:datacard.rfind('.txt')], datacard))           

