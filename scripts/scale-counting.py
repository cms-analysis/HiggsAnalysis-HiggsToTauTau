#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

parser = OptionParser(usage="usage: %prog [options] ARGs",
                      description="Script to rescale all yields for cut and count datacards (according to a luminosity projection)")
parser.add_option("-s", "--scale", dest="scale", default=1.,  type="float",   help="Scale to be applied to all yields. [Default: 1.]")
parser.add_option("-i", "--input", dest="input", default='test', type="string", help="Name of the input directoriy in which to expect the datacards. [Default: 'test']")
parser.add_option("-n", "--name", dest="name", default='datacard_{MASS}.txt', type="string", help="Name of the input datacard. [Default: 'datacard_{MASS}.txt']")
(options, args) = parser.parse_args()

def rescale(input_name, scale=1.) :
    """

    """
    output_rates = []
    input_file   = open(input_name,'r')
    output_file  = open("tmp.txt", 'w')
    for input_line in input_file :
       words = input_line.split()
       output_line = input_line
       if len(words) < 1: continue
       ## determine which processes are actually signal. The way to determine signal
       ## processes is by the process id smaller equal 0.
       if words[0] == "rate" :
           for (idx, word) in enumerate(words) :
               if idx==0 :
                   continue
               output_rates.append(str(scale*float(word)))
           output_line = "rate          "+"    ".join(output_rates)+"\n"
       output_file.write(output_line)
    input_file.close()
    output_file.close()

import os
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

## base directory introduced to allow use of absolute file paths
base_directory = os.getcwd()

for mass in parseArgs(args) :
    massstr = "%.0f" % mass
    os.chdir(base_directory+'/'+options.input+'/'+massstr)
    input_card = options.name.replace("{MASS}", massstr)
    rescale(input_card, options.scale)
    print "mv tmp.txt %s" % options.name.replace("{MASS}", massstr)
    os.system("mv tmp.txt %s" % options.name.replace("{MASS}", massstr))
