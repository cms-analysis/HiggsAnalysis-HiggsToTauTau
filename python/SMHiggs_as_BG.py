#!/usr/bin/env python

from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options]",
                      description="Main script to inject a 125 GeV SM Higgs to the backgrounds.")
parser.add_option("-i", "--input", dest="input", default="", type="string",
                  help="Input path to the aux directory. [Default: \"\"]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Run in verbose mode")
(options, args) = parser.parse_args()

import re
import os
import math
import sys
import shutil
import ROOT
import linecache

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
        rate=0.0
        help = directory +"/"+hist
        hist=self.load_hist(file, help)
        rate=hist.Integral()
        return rate


## if len(args) < 1 :
##        parser.print_help()
##        exit(1)

## setup datacard creator
datacard_creator = MakeDatacard()

directoryList = os.listdir(options.input+"/sm")
print directoryList
for dir in directoryList :
    datacards = os.listdir(options.input+"/sm/{DIR}".format(DIR=dir))
    for datacard in datacards :
        ## skip first pass of 'bin'
        first_pass_on_bin = True
        ## does datacard includes Signal
        includesSignal = False
        ## only add once shape
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
        ## first file parsin
        input_file = open(options.input+"/sm/{DIR}/".format(DIR=dir) +input_name,'r')
        output_file = open(options.input+"/sm/{DIR}/".format(DIR=dir) +input_name.replace(".txt", "_Higgs.txt"), 'w')
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
                        full_rootfile=options.input+"/sm/{DIR}/".format(DIR=dir)+word
                        rootfile=word.replace("../common/", "")
                output_line = output_line +"""
shapes ggH_SM * ../common/{ROOTFILE} $CHANNEL/ggH125 $CHANNEL/ggH125_$SYSTEMATIC \n
shapes qqH_SM * ../common/{ROOTFILE} $CHANNEL/qqH125 $CHANNEL/qqH125_$SYSTEMATIC \n
shapes VH_SM * ../common/{ROOTFILE} $CHANNEL/VH125 $CHANNEL/VH125_$SYSTEMATIC
""".format(ROOTFILE=rootfile)
                add_shapes= False
            ## determine the list of all single channels (in standardized format, multiple occurences possible)
            if words[0] == "bin" :
                if not first_pass_on_bin :
                    bin_name=words[1]
                    output_line = output_line.replace("\n", "")
                    output_line = output_line + '\t' + bin_name + '\t' + bin_name + '\t' + bin_name + '\n'
                first_pass_on_bin = False
            if words[0] == "process" and words[4].isdigit() :
                if not words[1].isdigit() :
                    includesSignal = True
                output_line = output_line.replace("\n", "")
                output_line = output_line + "\t \t 97" + "\t \t 98" + "\t \t 99 \n" # geht auch schoener
            if words[0] == "process" and words[4].isdigit()==False :
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
        os.system("rm -r {INPUT}".format(INPUT=options.input+"/sm/{DIR}/".format(DIR=dir) +input_name))
        os.system("mv {OUTPUT} {NEW}".format(OUTPUT=options.input+"/sm/{DIR}/".format(DIR=dir) +input_name.replace(".txt", "_Higgs.txt"), NEW=options.input+"/sm/{DIR}/".format(DIR=dir) +input_name))
    print dir, " done"
