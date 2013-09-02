#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="Script to sculpt all templates in a root input file for limit calculation between the values given by options --min and --max. ARG corresponds to the file that is to be sculpted. Per default a new file with postfix *_sculpted will be created. By option you can decide to update the existing file.")
parser.add_option("--min", dest="min", default= "0", type="string",
                  help="Minimum to start zeroing bins. [Default: 0]")
parser.add_option("--max", dest="max", default="50", type="string",
                  help="Maximum to stop zeroing bins. [Default: 50]")
parser.add_option("--categories", dest="categories", default="", type="string",
                  help="Add categories here, if you want to restrict the sculpting of templates to a certaint group of event categories. Category names can be given as python regular expressions. The regular expressions should be embraced by quotation marks and separated by whitespace. If empty, no restriction is applied. [Default: '']")
parser.add_option("--update-file", dest="update_file", default=False, action="store_true",
                  help="Use this option if you want to update the existing file and not create a new file. [Default: False]")

# check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re
import ROOT

## turn options.categories into a list
categories = options.categories.split(' ')
for idx in range(len(categories)) : categories[idx] = categories[idx].rstrip(',')

def modify_hists(dir, output, path='') :
    for key in dir.GetListOfKeys() :
        name=key.GetName()
        if key.GetClassName().startswith('TDirectory') :
            print "decending to directory:", name
            output.cd(); output.mkdir(name)
            modify_hists(dir.Get(name), output, path+name+'/')
        else :
            if isinstance(dir.Get(name), ROOT.TH1) :
                hist = dir.Get(name).Clone(name)
                for i in range(hist.GetNbinsX()) :
                    if float(options.min) <= hist.GetBinLowEdge(i) and hist.GetBinLowEdge(i)<float(options.max) :
                        sculpt = False
                        if categories :
                            for cat in categories :
                                if re.search(cat, name):
                                    sculpt = True
                        else :
                            sculpt = True
                        if sculpt :
                            hist.SetBinContent(i, 0); hist.SetBinError(i, 0)
                output.cd(); output.cd(path)
                hist.Write(hist.GetName(), ROOT.TObject.kOverwrite)

input  = ROOT.TFile(args[0]); output = ROOT.TFile(args[0]+'_sculpted', 'UPDATE')
modify_hists(input, output)
output.Close(); input.Close()
if options.update_file :
    os.system("mv {SOURCE} {TARGET}".format(SOURCE=args[0]+'_sculpted', TARGET=args[0]))
