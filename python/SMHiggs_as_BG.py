#!/usr/bin/env python

from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to inject a 125 GeV SM Higgs as background. ARG corresponds to the pull path of the auxiliaries directory to which you want to apply this change. Note that this causes a change of the inputs datacards.")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Run in verbose mode.")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if not len(args) == 1 :
    parser.print_usage()
    exit(1)    
    
import os
import ROOT

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

    def rate_from_hist(self, file, directory, hist) :
        """
        Return rate from histogram in output histfile.
        """
        file = ROOT.TFile(file,"READ")
        rate=0.
        help = directory +"/"+hist
        hist=self.load_hist(file, help)
        rate=hist.Integral()
        return rate

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
                output_line = output_line +"""shapes ggH_SM * {ROOTFILE} $CHANNEL/ggH125 $CHANNEL/ggH125_$SYSTEMATIC 
shapes qqH_SM * {ROOTFILE} $CHANNEL/qqH125 $CHANNEL/qqH125_$SYSTEMATIC 
shapes VH_SM * {ROOTFILE} $CHANNEL/VH125 $CHANNEL/VH125_$SYSTEMATIC
""".format(ROOTFILE=rootfile)
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
                output_line = output_line + "\t \t ggH_SM" + "\t \t qqH_SM" + "\t \t VH_SM \n"
            if words[0] == "rate" :
                VH_rate=datacard_creator.rate_from_hist(full_rootfile, bin_name, "VH125")
                qqH_rate=datacard_creator.rate_from_hist(full_rootfile, bin_name, "qqH125")
                ggH_rate=datacard_creator.rate_from_hist(full_rootfile, bin_name, "ggH125")
                output_line = output_line.replace("\n", "")
                output_line = output_line + '\t \t' + str(ggH_rate) + "\t \t" + str(qqH_rate) + "\t \t" + str(VH_rate) + "\n"
            if len(words) > 1 :
                if words[1]=="lnN" or words[1]=="shape" or words[1]=="gnN" :
                    if includesSignal :
                        output_line = output_line.replace("\n", "")
                        output_line = output_line + "\t" + words[ggH_idx+1] + "\t" + words[qqH_idx+1] + "\t" + words[VH_idx+1] + "\n"
                    else :
                        output_line = output_line.replace("\n", "")
                        output_line = output_line + "- \t - \t - \n"
            if options.verbose :
                print output_line
            output_file.write(output_line)
        ##close files
        input_file.close()
        output_file.close()
        os.system("rm -r {INPUT}".format(INPUT=args[0]+"/sm/{DIR}/".format(DIR=dir) +input_name))
        os.system("mv {OUTPUT} {NEW}".format(OUTPUT=args[0]+"/sm/{DIR}/".format(DIR=dir) +input_name.replace(".txt", "_Higgs.txt"), NEW=args[0]+"/sm/{DIR}/".format(DIR=dir) +input_name))
    print dir, " done"
