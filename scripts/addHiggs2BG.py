#!/usr/bin/env python

import os
import re
import ROOT
from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to inject a SM Higgs as background. The mass of the Higgs Boson can be chosen freely, but has to be available in the root input files. ARG corresponds to the full path of the auxiliaries directory to which you want to apply this change. Note that this causes a change of the inputs datacards.")
parser.add_option("--uncert-inputs", dest="cash_uncert", default="{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup".format(CMSSW_BASE=os.environ['CMSSW_BASE']), type="string",
                  help="Add here the path where to find the uncertainty files that these datacards have been produced from. [Default: '{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup']")
parser.add_option("--mass", dest="mass", default="125", type="string",
                  help="Chose which Higgs Mass Hypotheses to add. [Default: '125']")
parser.add_option("--label", dest="label", default="", type="string",
                  help="Add an additional label here that you might want to append to the Higgs as background samples. [Default: '']")
parser.add_option("--scale-rate", dest="scale", default=1.0, type="float",
                  help="Scale the Higgs rate of the injected Higgs. [Default: 1.0]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="Run in verbose mode.")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if not len(args) == 1 :
    parser.print_usage()
    exit(1)    
    
class MakeDatacard :
    def load_hist(self, file, name) :
        """
        Load a histogram with name from input histfile. Issue a warning in case the histogram
        is not available.
        """
        hist = file.Get(name)
        if type(hist) == ROOT.TObject :
            print "hist not found: ", file.GetName(), ":", name           
        return hist

    def rate_from_hist(self, file, directory, hist_name) :
        """
        Return rate from histogram in output histfile.
        """
        file = ROOT.TFile(file,"READ")
        rate=0.
        help = directory +"/"+hist_name
        hist=self.load_hist(file, help)
        rate=hist.Integral()
        return rate

    def scale_histogram(self, file, directory, hist_name, scale, uncertainty="") :
        """
        Rescale and Clone a given Higgs histogram.
        """
        ## open root file and get original histograms
        file = ROOT.TFile(file, "UPDATE")
        help = directory + "/" + hist_name + uncertainty
        ## prepare mA hist
        hist = self.load_hist(file, help)
        new_hist = hist.Clone()
        new_hist_name = hist_name.replace("{MASS}".format(MASS=options.mass), "{MASS}_{SCALE}".format(MASS=options.mass, SCALE=str(scale))) + uncertainty
        new_hist.Scale(scale)
        ## write modified histogram to file
        #help2 = directory + "/" + hist_name.replace("{MASS}".format(MASS=options.mass), "{MASS}_{SCALE}".format(MASS=options.mass, SCALE=str(scale))) + uncertainty
        #test = self.load_hist(file, help2)
        #if not type(test) == ROOT.TObject :
        #    print "Already included a Higgs with exact same configuration"
        #    exit(1)
        file.cd(directory)
        new_hist.Write(new_hist_name, ROOT.TObject.kOverwrite)

## cashed uncertainties for each channel
def cash_uncerts(datacard="htt_em_0_8TeV.txt") :
    """
    open the uncertainty files for a given datacard, extract the uncertainties that
    should be added for ggH, qqH, VH and return these as a dictionary of dictionaries
    """
    uncert_VH  = {}
    uncert_ggH = {}
    uncert_qqH = {}
    ## extract info from datacards name unc-sm-8TeV-00.vals
    matcher = re.compile('\w+_(?P<CHN>\w+)_(?P<CAT>\w+)_(?P<PER>\d\w+)\w*')
    chn = matcher.match(datacard).group('CHN')
    cat = matcher.match(datacard).group('CAT')
    per = matcher.match(datacard).group('PER')
    ## parse uncertainty values file
    input = open(options.cash_uncert+"/{CHN}/unc-sm-{PER}-0{CAT}.vals".format(CHN=chn, PER=per, CAT=cat),'r')
    for index, line in enumerate(input) :
        if "#" in line :
            continue
        words = line.lstrip().strip().split()
        if len(words)<4 :
            continue
        if 'signal' in words[1] or 'ggH' in words[1] :
            uncert_ggH[words[-2]] = words[-1]
        if 'signal' in words[1] or 'qqH' in words[1] :
            uncert_qqH[words[-2]] = words[-1]
        if 'signal' in words[1] or 'VH'  in words[1] :
            uncert_VH [words[-2]] = words[-1]
    input.close()
    cash = {}
    cash['ggH'] = uncert_ggH
    cash['qqH'] = uncert_qqH
    cash['VH' ] = uncert_VH
    return cash

## setup datacard creator
datacard_creator = MakeDatacard()

directoryList = os.listdir(args[0]+"/sm")
#print directoryList
for dir in directoryList :
    datacards = os.listdir(args[0]+"/sm/{DIR}".format(DIR=dir))
    for datacard in datacards :
        ## skip first pass of 'bin'
        first_pass_on_bin = True
        ## does datacard include signal?
        includesSignal = False
        ## add shape only once
        add_shapes = True
        ## other needed stuff
        full_rootfile=""
        rootfile=""
        bin_name=""
        ggH_idx=0
        qqH_idx=0
        VH_idx=0
        input_name=""
        if datacard.find(".txt")>-1 :
            input_name = datacard
        else :
            continue
        ## cash the uncertainties for Higgs as BG. The result is a dictionary of
        ## dictionaries for ggH, qqH, VH relating uncertainty names to values.
        cashed_uncerts = cash_uncerts(input_name)
        ## first file parsing
        input_file = open(args[0]+"/sm/{DIR}/".format(DIR=dir) +input_name,'r')
        output_file = open(args[0]+"/sm/{DIR}/".format(DIR=dir) +input_name.replace(".txt", "_Higgs.txt"), 'w')
        for index, input_line in enumerate(input_file) :
            words = input_line.split()
            output_line = input_line
            if len(words) < 1: continue
            ## need to fix jmax in the head of the file here
            if words[0] == "jmax" :
                output_line = output_line.replace(words[1], " *")
                jmax=words[1]
            ## determine which file and directory structures to take care of for this combination
            if words[0] == "shapes" and add_shapes:
                for (idx, word) in enumerate(words):
                    if word.find(".root")>-1 :
                        full_rootfile=args[0]+"/sm/{DIR}/".format(DIR=dir)+word
                        rootfile=word.replace("../common/", "")
                output_line = output_line +"""shapes ggH_SM{LABEL} * {ROOTFILE} $CHANNEL/ggH{MASS} $CHANNEL/ggH{MASS}_$SYSTEMATIC 
shapes qqH_SM{LABEL} * {ROOTFILE} $CHANNEL/qqH{MASS} $CHANNEL/qqH{MASS}_$SYSTEMATIC 
shapes VH_SM{LABEL} * {ROOTFILE} $CHANNEL/VH{MASS} $CHANNEL/VH{MASS}_$SYSTEMATIC
""".format(LABEL=options.label, ROOTFILE=rootfile, MASS=options.mass)
                add_shapes= False
            ## determine the list of all single channels (in standardized format, multiple occurences possible)
            if words[0] == "bin" :
                if not first_pass_on_bin :
                    bin_name=words[1]
                    output_line = output_line.replace("\n", "")
                    output_line = output_line + '\t' + bin_name + '\t' + bin_name + '\t' + bin_name + '\n'
                first_pass_on_bin = False
            if words[0] == "process" and words[-1].isdigit() :
                if not words[1].isdigit() :
                    includesSignal = True
                final_elem = int(words[-1])
                output_line = output_line.replace("\n", "")
                output_line = output_line + ("\t \t %s" % (final_elem+1)) + ("\t \t %s" % (final_elem+2)) + ("\t \t %s \n" % (final_elem+3))
            if words[0] == "process" and words[-1].isdigit()==False :
                for (idx, word) in enumerate(words) :
                    if word=="ggH" :
                        ggH_idx=idx
                    if word=="qqH" :
                        qqH_idx=idx
                    if word=="VH" :
                        VH_idx=idx
                output_line = output_line.replace("\n", "")
                output_line = output_line + "\t \t ggH_SM{LABEL}".format(LABEL=options.label) + "\t \t qqH_SM{LABEL}".format(LABEL=options.label) + "\t \t VH_SM{LABEL} \n".format(LABEL=options.label)
            if words[0] == "rate" :
                VH_rate=datacard_creator.rate_from_hist(full_rootfile, bin_name, "VH{MASS}".format(MASS=options.mass))*options.scale
                qqH_rate=datacard_creator.rate_from_hist(full_rootfile, bin_name, "qqH{MASS}".format(MASS=options.mass))*options.scale
                ggH_rate=datacard_creator.rate_from_hist(full_rootfile, bin_name, "ggH{MASS}".format(MASS=options.mass))*options.scale
                output_line = output_line.replace("\n", "")
                output_line = output_line + '\t \t' + str(ggH_rate) + "\t \t" + str(qqH_rate) + "\t \t" + str(VH_rate) + "\n"
                ## add new scaled central histograms
                datacard_creator.scale_histogram(full_rootfile, bin_name, "VH{MASS}".format(MASS=options.mass), options.scale, "")
                datacard_creator.scale_histogram(full_rootfile, bin_name, "qqH{MASS}".format(MASS=options.mass), options.scale, "")
                datacard_creator.scale_histogram(full_rootfile, bin_name, "ggH{MASS}".format(MASS=options.mass), options.scale, "")
            if len(words) > 1 :
                if words[1]=="lnN" or words[1]=="shape" or words[1]=="gnN" :
                    if includesSignal :
                        output_line = output_line.replace("\n", "")
                        output_line = output_line + "\t" + words[ggH_idx+1] + "\t" + words[qqH_idx+1] + "\t" + words[VH_idx+1] + "\n"
                    else :
                        output_line = output_line.replace("\n", "")
                        ggH_value = '-'
                        if words[0] in cashed_uncerts['ggH'].keys() :
                            ggH_value = cashed_uncerts['ggH'][words[0]]
                        qqH_value = '-'
                        if words[0] in cashed_uncerts['qqH'].keys() :
                            qqH_value = cashed_uncerts['qqH'][words[0]]
                        VH_value  = '-'
                        if words[0] in cashed_uncerts['VH' ].keys()  :
                            VH_value  = cashed_uncerts['VH' ][words[0]]
                        ## add uncertainties channelwise
                        output_line = output_line + "{GGH} \t {QQH} \t {VH} \n".format(GGH=ggH_value, QQH=qqH_value, VH=VH_value)
                ## add new scaled uncertainty histograms
                if words[1]=="shape" :
                    if words[0] in cashed_uncerts['qqH'].keys() :
                        datacard_creator.scale_histogram(full_rootfile, bin_name, "VH{MASS}_".format(MASS=options.mass) + words[0], options.scale, "Up")
                        datacard_creator.scale_histogram(full_rootfile, bin_name, "qqH{MASS}_".format(MASS=options.mass) + words[0], options.scale, "Up")
                        datacard_creator.scale_histogram(full_rootfile, bin_name, "ggH{MASS}_".format(MASS=options.mass) + words[0], options.scale, "Up")
                        datacard_creator.scale_histogram(full_rootfile, bin_name, "VH{MASS}_".format(MASS=options.mass) + words[0], options.scale, "Down")
                        datacard_creator.scale_histogram(full_rootfile, bin_name, "qqH{MASS}_".format(MASS=options.mass) + words[0], options.scale, "Down")
                        datacard_creator.scale_histogram(full_rootfile, bin_name, "ggH{MASS}_".format(MASS=options.mass) + words[0], options.scale, "Down")  
            if options.verbose :
                print output_line
            output_file.write(output_line)
        ##close files
        input_file.close()
        output_file.close()
        os.system("rm -r {INPUT}".format(INPUT=args[0]+"/sm/{DIR}/".format(DIR=dir) +input_name))
        os.system("mv {OUTPUT} {NEW}".format(OUTPUT=args[0]+"/sm/{DIR}/".format(DIR=dir) +input_name.replace(".txt", "_Higgs.txt"), NEW=args[0]+"/sm/{DIR}/".format(DIR=dir) +input_name))
    print dir, " done"
