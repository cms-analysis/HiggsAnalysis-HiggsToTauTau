#!/usr/bin/env python

import os
import re
import ROOT
from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to inject a SM Higgs as background. The mass of the Higgs Boson can be chosen freely, but has to be available in the root input files. ARG corresponds to the full path of the auxiliaries directory to which you want to apply this change. Note that this causes a change of the inputs datacards.")
parser.add_option("--uncert-inputs", dest="cash_uncert", default="{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup".format(CMSSW_BASE=os.environ['CMSSW_BASE']), type="string",
                  help="Add here the path where to find the uncertainty files that these datacards have been produced from. [Default: '{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup']")
parser.add_option("--label", dest="label", default="", type="string",
                  help="Add an additional label here that you might want to append to the Higgs as background samples. [Default: '']")
parser.add_option("--mass", dest="mass", default="125", type="string",
                  help="Chose which Higgs Mass Hypotheses to add. [Default: '125']")
parser.add_option("--scale-rate", dest="scale", default=1.0, type="float",
                  help="Scale the Higgs rate of the injected Higgs. [Default: 1.0]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="Run in verbose mode.")
parser.add_option("--mssm", dest="mssm", default=False, action="store_true",
                  help="Inject SM higgs as BKG to MSSM datacards.")
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
        new_hist_name = hist_name.replace("{MASS}".format(MASS=options.mass), "{MASS}_SCALE{SCALE}".format(MASS=options.mass, SCALE=str(scale)), 1) + uncertainty
        if options.mssm :
            new_hist_name = hist_name.replace("125".format(MASS=options.mass), "125_MSSM{LABEL}".format(LABEL=options.label), 1) + uncertainty
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
def cash_uncerts(dir, backgrounds, categories, signal_processes, datacard="htt_em_0_8TeV.txt") :
    """
    open the uncertainty files for a given datacard, extract the uncertainties that
    should be added for ggH, qqH, VH and return these as a dictionary of dictionaries
    """
    vhtt = False
    uncert = {}
    #uncert_process  = {}
    ## extract info from datacards name unc-sm-8TeV-00.vals
    matcher = re.compile('\w+_(?P<CHN>\w+)_(?P<CAT>\w+)_(?P<PER>\d\w+)\w*')
    if dir=="vhtt" :
        vhtt = True
        matcher = re.compile('(?P<CHN>\w+)_(?P<CAT>\w+)_(?P<PER>\d\w+)\w*')
    chn = matcher.match(datacard).group('CHN')
    cat = matcher.match(datacard).group('CAT')
    per = matcher.match(datacard).group('PER')
    ## parse uncertainty values file
    cgs_file = open(options.cash_uncert+"/{CHN}/cgs-{ANA}-{PER}-0{CAT}.conf".format(ANA="mssm" if options.mssm else "sm", CHN=chn, PER=per, CAT=cat),'r')
    #signal_processes = []
    for index, line in enumerate(cgs_file) :
        line = line.replace(",", " ")
        words = line.lstrip().strip().split()
        if len(words)<2 :
            continue
        if vhtt :
            if "#" in line:
                continue
        if "$" in words[0] and words[2]=="signal" :
            for idx, word in enumerate(words) :
                if idx > 2:
                    signal_processes.append(word)
        if "categories" in words[0] :
            for idx, word in enumerate(words) :
                if idx > 0:
                    categories.append(word)
        if words[0]=="$" and words[2]=="background" :
            for idx, word in enumerate(words) :
                if idx > 2:
                    backgrounds.append(word)        
    if options.mssm:
        options.mass=""
        signal_processes = ['ggH_SM125','qqH_SM125','VH_SM125']
    ## parse uncertainty values file  
    for category in categories :
        uncert_cat  = {}
        for signal in signal_processes :
            uncert_signal  = {}
            input = open(options.cash_uncert+"/{CHN}/unc-{ANA}-{PER}-0{CAT}.vals".format(ANA="mssm" if options.mssm else "sm", CHN=chn, PER=per, CAT=cat),'r')
            for index, line in enumerate(input) :
                if "#" in line :
                    continue
                words = line.lstrip().strip().split()
                if len(words)<4 :
                    continue
                #for category in categories :
                if category in words[0] :               
                    #for signal in signal_processes :
                    if options.mssm :
                        if 'signal' in words[1] or 'ggH' in words[1] or 'simulated' in words[1] :                      
                            uncert_signal[words[-2]] = words[-1]
                    else :
                        if 'signal' in words[1] or signal in words[1] or 'simulated' in words[1] :                      
                            uncert_signal[words[-2]] = words[-1]
                    
            input.close()
            uncert_cat[signal] = uncert_signal
        uncert[category] = uncert_cat
    #print uncert
    return uncert

## setup datacard creator
datacard_creator = MakeDatacard()

directoryList = os.listdir(args[0]+"/{ANA}".format(ANA="mssm" if options.mssm else "sm"))
for dir in directoryList :
    datacards = os.listdir(args[0]+"/{ANA}/{DIR}".format(ANA="mssm" if options.mssm else "sm", DIR=dir))
    for datacard in datacards :
        ## skip first pass of 'bin'
        first_pass_on_bin = True
        ## add shape only once
        add_shapes = True
        ## other needed stuff
        full_rootfile=""
        rootfile=""
        input_name=""
        signal_processes = []
        categories = []
        backgrounds = []
        if datacard.find(".txt")>-1 :
            input_name = datacard
        else :
            continue
        cashed_uncerts = cash_uncerts(dir, backgrounds, categories, signal_processes, input_name)
        if options.mssm:
            options.mass=""
            signal_processes = ['ggH_SM125','qqH_SM125','VH_SM125']
        if options.verbose :
            print "signal_processes", signal_processes
            print "backgrounds", backgrounds
            print "categories", categories
        ## first file parsing
        input_file = open(args[0]+"/{ANA}/{DIR}/".format(ANA="mssm" if options.mssm else "sm", DIR=dir) +input_name,'r')
        output_file = open(args[0]+"/{ANA}/{DIR}/".format(ANA="mssm" if options.mssm else "sm", DIR=dir) +input_name.replace(".txt", "_Higgs.txt"), 'w')
        for index, input_line in enumerate(input_file) :
            words = input_line.split()
            output_line = input_line
            if len(words) < 2: continue
            ## need to fix jmax in the head of the file here
            if words[0] == "jmax" :
                output_line = output_line.replace(words[1], " *")
                jmax=words[1]
            ## determine which file and directory structures to take care of for this combination
            if words[0] == "shapes" and add_shapes:
                for (idx, word) in enumerate(words):
                    if word.find(".root")>-1 :
                        full_rootfile=args[0]+"/{ANA}/{DIR}/".format(ANA="mssm" if options.mssm else "sm", DIR=dir)+word
                        rootfile=word.replace("../common/", "")
                for signal in signal_processes :
                    if not options.mssm :
                        output_line = output_line +"""shapes {SIGNAL}_SM{LABEL} * {ROOTFILE} $CHANNEL/{SIGNAL}{MASS}_SCALE{SCALE} $CHANNEL/{SIGNAL}{MASS}_SCALE{SCALE}_$SYSTEMATIC 
                        """.format(SIGNAL=signal, LABEL=options.label, ROOTFILE=rootfile, MASS=options.mass, SCALE=options.scale)
                    if options.mssm :
                        output_line = output_line +"""shapes {SIGNAL}_MSSM{LABEL} * {ROOTFILE} $CHANNEL/{SIGNAL}_MSSM{LABEL} $CHANNEL/{SIGNAL}_MSSM{LABEL}_$SYSTEMATIC 
                        """.format(SIGNAL=signal, LABEL=options.label, ROOTFILE=rootfile)
                add_shapes= False               
            ## determine the list of all single channels (in standardized format, multiple occurences possible)
            if words[0] == "bin" :
                if not first_pass_on_bin :
                    output_line = output_line.replace("\n", "")
                    for category in categories :
                        for signal in signal_processes :
                            output_line = output_line + '\t' + category
                    output_line = output_line + '\n'
                first_pass_on_bin = False                
            if words[0] == "process" and words[-1].isdigit() :
                output_line = output_line.replace("\n", "")
                for category in categories :
                    final_elem = int(words[-1])
                    for signal in signal_processes :
                        output_line = output_line + ("\t \t %s" % (final_elem+1))
                        final_elem = final_elem+1
                output_line = output_line + '\n'     
            if words[0] == "process" and words[-1].isdigit()==False :
                 output_line = output_line.replace("\n", "")
                 for category in categories :
                     for signal in signal_processes :
                         output_line = output_line + "\t \t {SIGNAL}_{ANA}{LABEL}".format(SIGNAL=signal, ANA='MSSM' if options.mssm else 'SM', LABEL=options.label)                  
                 output_line = output_line + '\n'               
            if words[0] == "rate" :
                output_line = output_line.replace("\n", "")
                for category in categories :
                    if options.mssm : 
                        for signal in signal_processes :
                            rate=datacard_creator.rate_from_hist(full_rootfile, category, "{SIGNAL}{MASS}".format(SIGNAL=signal, MASS=options.mass))*options.scale
                            datacard_creator.scale_histogram(full_rootfile, category, "{SIGNAL}{MASS}".format(SIGNAL=signal, MASS=options.mass), options.scale, "")
                            output_line = output_line + '\t \t' + str(rate)
                    else :
                        for signal in signal_processes :
                            rate=datacard_creator.rate_from_hist(full_rootfile, category, "{SIGNAL}{MASS}".format(SIGNAL=signal, MASS=options.mass))*options.scale
                            datacard_creator.scale_histogram(full_rootfile, category, "{SIGNAL}{MASS}".format(SIGNAL=signal, MASS=options.mass), options.scale, "")
                            output_line = output_line + '\t \t' + str(rate)
                output_line = output_line.replace("\n", "")
                output_line = output_line + "\n"
            if words[1]=="lnN" or words[1]=="shape" or words[1]=="gmN" :
                output_line = output_line.replace("\n", "")
                for category in categories :
                    for signal in signal_processes :
                        value = '-'
                        if words[0] in cashed_uncerts[category][signal].keys() :
                            value = cashed_uncerts[category][signal][words[0]]
                        output_line = output_line + "\t {VALUE}".format(VALUE=value)
                output_line = output_line + "\n"       
            ## add new scaled uncertainty histograms
            if words[1]=="shape" and words[0] in cashed_uncerts[category][signal].keys() : #and str(options.mass) in words[0]:
                for category in categories :
                    for signal in signal_processes :
                        #if words[0] in cashed_uncerts[category][signal].keys() :
                        if options.mssm:
                            datacard_creator.scale_histogram(full_rootfile, category, "{SIGNAL}{MASS}_".format(SIGNAL=signal, MASS=options.mass) + words[0], options.scale, "Up")
                            datacard_creator.scale_histogram(full_rootfile, category, "{SIGNAL}{MASS}_".format(SIGNAL=signal, MASS=options.mass) + words[0], options.scale, "Down")
                        else :
                            datacard_creator.scale_histogram(full_rootfile, category, "{SIGNAL}{MASS}_".format(SIGNAL=signal, MASS=options.mass) + words[0], options.scale, "Up")
                            datacard_creator.scale_histogram(full_rootfile, category, "{SIGNAL}{MASS}_".format(SIGNAL=signal, MASS=options.mass) + words[0], options.scale, "Down")
            if options.verbose :
                print output_line   
            output_file.write(output_line)
        
        ##close files
        input_file.close()
        output_file.close()
        if options.mssm :
            os.system("rm -r {INPUT}".format(INPUT=args[0]+"/mssm/{DIR}/".format(DIR=dir) +input_name))
            os.system("mv {OUTPUT} {NEW}".format(OUTPUT=args[0]+"/mssm/{DIR}/".format(DIR=dir) +input_name.replace(".txt", "_Higgs.txt"), NEW=args[0]+"/mssm/{DIR}/".format(DIR=dir) +input_name))
        else :
            os.system("rm -r {INPUT}".format(INPUT=args[0]+"/sm/{DIR}/".format(DIR=dir) +input_name))
            os.system("mv {OUTPUT} {NEW}".format(OUTPUT=args[0]+"/sm/{DIR}/".format(DIR=dir) +input_name.replace(".txt", "_Higgs.txt"), NEW=args[0]+"/sm/{DIR}/".format(DIR=dir) +input_name))
    print dir, " done"
