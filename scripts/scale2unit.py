#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to scale SM datacards from other channels by one over the SM cross section times BR. SM xsec and BR are taken from FeynHiggs. The output will override the input datacards and corresponding input histogram files. The output is meant to be used for the calculation of MSSM limits in the tanb mA plane making use of the submit.py/submit-slave.py tools with option -m tanb[+]. For this kind of submits the signal yields will be multiplied by the MSSM cross section and devided by the value of tanb. A list of arguments can be given. These arguments (ARGS) should be integers corresponding to the mass points for which you want to rescale the datacards.")
parser.add_option("-i", "--input", dest="input", default="test", type="string", help="Input directory where to find the datacards to be rescaled [Default: test]")
parser.add_option("-c", "--channel", dest="channel", default="all", type="choice", help="Channel to be rescaled [Default: all]", choices=["all", "htt", "hgg", "hbb", "hww", "hzz4l", "hzz2l2q", "hzz2l2nu", "hzz2l2t"])
parser.add_option("--no-rescale", dest="no_rescale", default=False, action="store_true", help="Do not re-scale production channels, which are available in FeynHiggs. Only set those channels to 0 which do not exist in FeynHiggs [Default: False]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)


import os
import re


class RescaleDatacards:
    def __init__(self, masspoint, datacard, channel) :
        ## masspoint in question
        self.mass = masspoint
        ## name of datacard
        self.datacard = datacard
        ## dictionary for production processes to FeynHiggs convention 
        self.production_processes_to_feynHiggs = {
            "ggH" : "ggA",
            "qqH" : "qqA",
            "ZH"  : "ZA" ,
            "WH"  : "WA" ,
            "VH"  : "WA" ,
            "ttH" : "ttA"
            }
        ## dictionary for decay channels to FeynHiggs convention
        self.decay_channels_to_feynHiggs = {
            "hww"      : "AWW",
            "hzz4l"    : "AZZ",
            "hzz2l2q"  : "AZZ",
            "hzz2l2nu" : "AZZ",
            "hzz2l2t"  : "AZZ",
            "hgg"      : "Agg",
            "hbb"      : "Abb",
            "htt"      : "Att"
            }
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

    def xsec(self, production_channel, mass) :
        """
        Loads SM cross sections needed to rescale the input yields. NOTE that the SM cross section
        is obtained from A in FeynHiggs and NOT from H or h. 
        """
        return float(os.popen("feyn-higgs-sm xs {channel} {mA} | grep value".format(channel=self.production_processes_to_feynHiggs[production_channel], mA=mass)).read().split()[2])/1000.

    def BR(self, decay_channel, mass) :
        """
        Loads SM branching ratios needed to rescale the input yields. NOTE that the SM branching
        ratio is obtained from A in FeynHiggs and NOT from H or h.
        """
        return float(os.popen("feyn-higgs-sm br {channel} {mA} | grep value".format(channel=self.decay_channels_to_feynHiggs[decay_channel], mA=mass)).read().split()[2])
    
    def rescale(self, no_rescale=False) :
        """
        Rescales a SM datacard by 1/xsec(SM) for each signal sample. For shape analyses all related histograms
        including shapes are rescaled accordingly. The latter is done by calling the rescaleSignal.C macro in
        the HiggsAnalysis/HiggstoTauTau package. A list of rates is returned in which the old signal rates have
        been replaced by new ones if appropriate. The function acts on the following class members:
        
        mass      : the actual mass point (needed for the look up of the SM xsec and BR for the correction)
        histfiles : list of full paths of the root files that contain the shape histograms
        old_rates : the list of rates (signal rates are picked and rescaled)
        processes : the list of processes (signal processes are picked and the histograms scaled)
        indexes   : the list of indexes of the signal processes in processes and rates

        NOTE:
        When no_rescale is set to False only those production channels, which are not available in FeynHiggs
        are set to 0. The rates, which are available in FeynHiggs are not changed. This is used for debugging.
        """
        ## copy of list of old rates
        new_rates = list(self.old_rates)
        for idx in self.indexes :
            old_rate = float(self.old_rates[idx])
            new_rate = old_rate/(float(self.xsec(self.processes[idx], self.mass))*float(self.BR(self.decay_channel, self.mass)))
            if new_rate<=0 :
                ## those processes for which the SM cross section or BR is not given are explicitely switched off here
                new_rate = 0
            else :
                if no_rescale :
                    new_rate = old_rate
            if old_rate>0 :
                ## zero entries do not need to be scaled
                scale = new_rate/old_rate
                #print "old rate: ", self.old_rates[idx], " new rate: ", new_rate, " scale: ", scale
                for histfile in self.histfiles :
                    ## do the scale replacement in all histfile accordingly
                    os.system(r"root -l -b -q {env}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C+\(true,{scale},\"{inputfile}\",\"{process}\",0\)".format(
                        env=os.environ.get("CMSSW_BASE"), scale=scale, inputfile=histfile, process=self.processes[idx]))
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

    def run(self, no_rescale=False) :
        old_rates_line = ""
        histpath =self.datacard[:self.datacard.rfind("/")+1]
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
        ## do the rescaling
        new_rates = self.rescale(no_rescale)
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

## parse a list of arguments which can be intergers or of type intA-intB
## where intA<=intB and fill this list of arguments into a list if ints
def parseArgs(args) :
    list = []
    for elem in args :
        if elem.find("-") > -1 :
            if elem.find(":") > -1 :
                step = int(elem[elem.find(":")+1:])
                min = int(elem[:elem.find("-")  ])
                max = int(elem[elem.find("-")+1:elem.find(":")])
            else :
                step = 1
                min = int(elem[:elem.find("-")  ])
                max = int(elem[elem.find("-")+1:])
            while min <= max :
                list.append(min)
                min=min+step
        else :
            list.append(elem)
    return list

for mass in parseArgs(args) :
    datacards = []
    path = "%s/%s/%s" % (os.getcwd(), options.input, mass)
    ## collect what is there
    basket = os.listdir(path)
    ## skip empty directories
    if len(basket)<1 :
        continue
    for piece in basket :
        if options.channel == "hww" :
            datacard_regex = r"hww_?\w*.txt"
        if options.channel == "hgg" :
            datacard_regex = r"test.txt"
        datacard_match = re.compile(datacard_regex)
        if datacard_match.search(piece) :
            datacards.append(piece)
    for datacard in datacards :
        rescaleDatacard = RescaleDatacards("%.1f" % float(mass), "%s/%s" % (path, datacard), options.channel)
        rescaleDatacard.run(options.no_rescale)

#print "return value? -- ", os.popen("feyn-higgs-mssm xs sm ggH 110 15 | grep value").read()
