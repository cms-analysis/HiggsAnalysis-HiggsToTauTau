#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGs",
                      description="Script to scale MSSM datacards by the acceptance corrections that have been derived for the restrictioin of the mass window on generator level. The acceptance corrections are obtained from HiggsAnalysis/HiggsToTauTau/python/acceptance_correction.py. The output will override the input datacards and corresponding input histogram files. ARGs corresponds to the mass points for which the datacards should be scaled.")
parser.add_option("-i", "--input", dest="input", default="LIMITS", type="string", help="Input directory where to find the datacards to be scaled [Default: LIMITS]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs
from HiggsAnalysis.HiggsToTauTau.acceptance_correction import acceptance_correction

class RescaleDatacards:
    def __init__(self, masspoint, datacard, channel="htt") :
        ## masspoint in question
        self.mass = masspoint
        ## name of datacard
        self.datacard = datacard
        ## dictionary for correction for sm branching ratio
        self.decay_channel = channel
        ## list of rates in datacard
        self.old_rates = []
        ## list of indexes where to find the actual signal
        self.indexes = []
        ## list of process names for signal processes (used for shape analyses)
        self.processes = []
        ## list of histfiles for shape analyses (determined form datacard)
        self.histfiles = []

    def scale(self, values) :
        """
        Rescales a MSSM datacard by acceptance_correction according to the restriction of the mass window on
        generator level. this correction is obtained from accdeptance_correction. For shape analyses all related
        histograms including shapes are rescaled accordingly. The latter is done by calling the rescaleSignal.C
        macro in the HiggsAnalysis/HiggstoTauTau package. A list of rates is returned in which the old signal
        rates have been replaced by new ones if appropriate. The function acts on the following class members:
        
        mass      : the actual mass point (needed for the look up of the SM xsec and BR for the correction)
        histfiles : list of full paths of the root files that contain the shape histograms
        old_rates : the list of rates (signal rates are picked and rescaled)
        processes : the list of processes (signal processes are picked and the histograms scaled)
        indexes   : the list of indexes of the signal processes in processes and rates
        """
        ## copy of list of old rates
        new_rates = list(self.old_rates)
        for idx in self.indexes :
            old_rate = float(self.old_rates[idx])
            new_rate = old_rate*values[self.processes[idx]]
            for histfile in self.histfiles :
                ## do the scale replacement in all histfile accordingly
                os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C+\(true,{SCALE},\"{INPUT}\",\"{PROCESS}\",0\)".format(
                    CMSSW_BASE=os.environ.get("CMSSW_BASE"), SCALE=values[self.processes[idx]], INPUT=histfile, PROCESS=self.processes[idx]))
            new_rates[idx] = "%f" % new_rate
        return new_rates

    def update_line(self, old_line, new_rates) :
        """
        Replaces the old_rates by the new_rates in the line string
        """
        new_list = old_line.split()
        for idx in self.indexes :
            new_list[idx+1] = str(new_rates[idx])
        new_line = '\t   '.join(new_list)+'\n'
        return new_line

    def run(self) :
        old_rates_line = ""
        histpath =self.datacard[:self.datacard.rstrip('/').rfind('/')+1]
        ## loop datacard in first go and collect information needed for rescaling
        old_datacard = open(self.datacard,'r')
        for line in old_datacard:
            wordarr = line.lstrip().split();
            ## collect histfiles for shape analyses
            if wordarr[0] == "shapes" :
                #print "found shape line: ", wordarr[0]
                for (i,element) in enumerate(wordarr) :
                    if element.find(".root") !=-1 :
                        if not self.histfiles.count(histpath+element)>0 :
                            self.histfiles.append(histpath+element)
            ## find process lines to mark signal processes
            if wordarr[0] == "process":
                #print "found process line: ", wordarr[0]
                for (i,element) in enumerate(wordarr) :
                    if i==0 :
                        continue
                    if element.isdigit() or element.lstrip("-").isdigit() :
                        if int(element) <=0:
                            self.indexes.append(i-1)
                    else :
                        self.processes.append(element)
            ## find actual rates for rescaling
            if wordarr[0].lower() == "rate":
                #print "found rate line: ", wordarr[0]
                old_rates_line = line
                for (i,element) in enumerate(wordarr) :
                    if i==0 :
                        continue
                    self.old_rates.append(element)
        ## determine scale factors for acceptance correction
        scales = {}
        for proc in self.processes :
            scales[proc] = acceptance_correction(proc, self.mass)
        ## do the rescaling
        new_rates = self.scale(scales)
        new_rates_line = self.update_line(old_rates_line, new_rates)
        ## create the new datacard
        old_datacard = open(self.datacard, "r" )
        new_datacard = open("tmp.txt"    , "w" )
        for line in old_datacard :
            new_datacard.write( line.replace(old_rates_line, new_rates_line) )
        old_datacard.close()
        new_datacard.close()
        ## final copying and cleanup
        #print "cp tmp.txt %s" % self.datacard 
        os.system("cp tmp.txt %s" % self.datacard)
        os.system("rm tmp.txt")

for mass in parseArgs(args) :
    datacards = []
    path = "%s/%s/%s" % (os.getcwd(), options.input, mass)
    ## collect what is there
    basket = os.listdir(path)
    ## skip empty directories
    if len(basket)<1 :
        continue
    for piece in basket :
        datacard_regex = r"htt_?\w*.txt"
        datacard_match = re.compile(datacard_regex)
        if datacard_match.search(piece) :
            datacards.append(piece)
    for datacard in datacards :
        rescaleDatacard = RescaleDatacards(mass, "%s/%s" % (path, datacard))
        rescaleDatacard.run()
