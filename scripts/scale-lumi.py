#!/usr/bin/env python

from optparse import OptionParser, OptionGroup
## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="Script to do final adjustments of vhbb datacards.\n")
parser.add_option("-i", "--input", dest="input", default="", type="string",
                  help="The root input file. [Default: \"\"]")
parser.add_option("-d", "--datacard", dest="datacard", default="", type="string",
                  help="Fullpath to datacard in question. [Default: \"\"]")
parser.add_option("--from", dest="source", default="", type="string",
                  help="The original lumi of the datacards. [Default: \"\"]")
parser.add_option("--to", dest="target", default="", type="string",
                  help="The lumi to scale the datacard to. [Default: \"\"]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os
import ROOT

def adapt_data_obs(path_to_datacard) :
    """

    """
    bins = []
    shapes = {}
    observes = []

    def paths(proc, bin) :
        paths = shapes[('*','*')]
        for (p,b) in shapes.keys() :
            if p == proc and b == bin :
                paths = shapes[(p,b)]
                break
        return paths
    
    old_file = open(path_to_datacard, 'r')
    for line in old_file :
        words = line.lstrip().split()
        if words[0] == 'shapes' :
            shapes[(words[1],words[2])] = words[3:]
        if words[0] == 'bin' :
            if len(bins) == 0 or len(words[1:])<len(bins) :
                bins = words[1:]
    old_file.close()

    old_file = open(path_to_datacard, 'r')
    new_file = open(path_to_datacard+'_tmp', 'w')
    for line in old_file :
        new_line = line
        words = line.lstrip().split()
        if words[0] == 'observation' :
            old_observes = words[1:]
            for idx in range(len(old_observes)) :
                hist_file = ROOT.TFile(path_to_datacard[:path_to_datacard.rfind('/')+1]+paths('data_obs',bins[idx])[0], 'READ')
                hist = hist_file.Get(paths('data_obs',bins[idx])[1].replace('$PROCESS','data_obs').replace('$CHANNEL',bins[idx]))
                value = hist.Integral()
                observes.append('%.0d' % value)
                hist_file.Close()
            new_line = 'observation '+' '.join(observes)+'\n'
        new_file.write(new_line)
    old_file.close()
    new_file.close()
    os.system("mv %s_tmp %s" % (path_to_datacard, path_to_datacard))
    return
    
def adapt_rates(path, scale) :
    """

    """
    rates = []
    old_file = open(path, 'r')
    new_file = open(path+'_tmp', 'w')
    for line in old_file :
        new_line = line
        words = line.lstrip().split()
        if words[0] == 'process' :
            if words[1].lstrip('-').isdigit() :
                pass
            else :
                procs = words[1:]
        if words[0] == 'rate' :
            old_rates = words[1:]
            for idx in range(len(old_rates)) :
                if not old_rates[idx].startswith('-') :
                    rates.append(str(float(old_rates[idx])*scale))
                else :
                    rates.append(old_rates[idx])
            new_line = 'rate '+' '.join(rates)+'\n'            
        new_file.write(new_line)
    old_file.close()
    new_file.close()
    os.system("mv %s_tmp %s" % (path, path))
    return

os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+\(\"{INPUTFILE}\",{OLD_LUMI},{NEW_LUMI},0,1\)".format(
    CMSSW_BASE=os.environ.get("CMSSW_BASE"),
    INPUTFILE=options.input,
    OLD_LUMI=options.source,
    NEW_LUMI=options.target,
    ))
adapt_rates(options.datacard, float(options.target)/float(options.source))
adapt_data_obs(options.datacard)
