#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...",
                      description="Script to setup the directory structure for the calculation of limits or significances with the CMS tools land or combine. ARG1, ARG2, ARG3, ... correspond to an arbitrary number of integers as input arguments corresponding to the mass points planned for the limit/significance calculation. If ARG1, ARG2, ARG3, ... are not a digit the datacard creation will be treated without any specific mass dependence. The tool will create a directory and a set of sub-directories corresponding to each element in ARGs. It will then copy all necessary root input files to these sub-directories and produce a consistent set of datacards (making use of the script create-datacard.py). The script relies on the machienery of automatic datacard creation detailed in the setup directory of this package. The name of the output directory and the list of necessary input files can be steered as optional parameters.")
parser.add_option("-n", "--name", dest="name", default="submit", type="string", help="Directory name for job submission. [Default: submit]")
parser.add_option("-c", "--decay-channel", dest="channel", default="new", type="choice", help="Ditau decay channel. [Default: new]", choices=["new", "em", "et","mt"])
parser.add_option("-e", "--event-category", dest="category", default="",type="string", help="Event category. [Default: \"\"]")
parser.add_option("-o", "--out", dest="out", default="model.txt", type="string", help="Name of the datacard (can be extended by the mass value for convenience when creating more than one datacard, see option --extend). [Default: model.txt]")
parser.add_option("--drop-channels", dest="drop",default="", type="string", help="Scale the given channels to 0. in the datacards. (This action will be applied to all channels that match the given string patterns, which may be on as a whitespace or ',' separated list). [Default: \"\"]")
parser.add_option("--extend", dest="extend", default=False, action="store_true", help="Extend datacard name by mass value [Default: False]")
parser.add_option("--verbose", dest="v", default=0, type="int", help="Verbosity level [Default: 0]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import re
import os

## create an unambiguous list out of a string of drop-channels
drop_channel_list = re.sub(r'\s', '', options.drop).split(',')

## admin of available masses per channel 
channel_to_mass = {}

## add mass point to the list of available masses per channel
def add_mass(channel, mass) :
    if not channel in channel_to_mass :
        channel_to_mass[channel] = "%s :  " % channel
    channel_to_mass[channel]+= "  %s  " % mass 

## create submit directory
if not os.path.exists(options.name):
    if options.v>0 :
        print "> creating directory %s" % options.name
    os.system("mkdir %s" % options.name)
os.chdir("%s/%s" % (os.getcwd(), options.name))

## add common directory for common input files
if not os.path.exists("common") :            
    os.system("mkdir common")
## open masses.vals. Append if it exists already, create otherwise
if os.path.exists("{pwd}/common/masses.vals".format(pwd=os.getcwd())) :
    masses = open("{pwd}/common/masses.vals".format(pwd=os.getcwd()), 'a')
else :
    masses = open("{pwd}/common/masses.vals".format(pwd=os.getcwd()), 'w')

## create subdirectories for each mass point and copy all necessary input files there
for mass in args:
    #if os.path.exists(mass):
    #    os.system("rm -r %s" % mass)
    if options.v>0 : 
        print "> create directory %s" % mass
    os.system("datacard-project.py -c %s -e %s %s" % (options.channel, options.category,  mass))
    os.chdir("%s/%s" % (os.getcwd(), mass))
    ## grap the root input file
    inputFile = ""
    basket = os.listdir(os.getcwd())
    for piece in basket :
        if piece.endswith('.root') :
            if piece.startswith(options.channel) or piece.startswith("htt_"+options.channel):
                inputFile = piece
    if inputFile :
        outputFile = options.out
        if options.extend :
            outputFile = "%s%s" % (outputFile, mass)
        if not mass.isdigit() :
            for channel in drop_channel_list :
                if not channel == "" : 
                    os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C+\(true,0.,\"{file}\",\"{pattern}\"\)".format(
                        CMSSW_BASE=os.environ['CMSSW_BASE'],
                        file=inputFile,
                        pattern=channel)
                              )
            os.system("create-datacard.py -i %s -o %s 0" % (inputFile, outputFile))
        else :
            for channel in drop_channel_list :
                if not channel == "" : 
                    os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C+\(true,0.,\"{file}\",\"{pattern}\"\)".format(
                        CMSSW_BASE=os.environ['CMSSW_BASE'],
                        file=inputFile,
                        pattern=channel)
                              )
            os.system("create-datacard.py -i %s -o %s %s" % (inputFile, outputFile, mass))
        add_mass(outputFile[:outputFile.find(".txt")], mass)
        os.system("rm *.conf *.vals")
    else :
        print "Error: did not find any input file"
    os.chdir("%s/.." % os.getcwd())

## write channel-mass strings to masses.vals
for channel in channel_to_mass :
    masses.write(channel_to_mass[channel]+"\n")
masses.close()

print "> done"
