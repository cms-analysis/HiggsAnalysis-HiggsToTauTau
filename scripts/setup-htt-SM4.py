#!/usr/bin/env python
import os
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Simple script to setup the limit calculation for htt in the 4 fermion model (SM4).")
parser.add_option("-n", "--name", dest="name", default="new-datacards", type="string", help="Name of the working directory. [Default: new-datacards]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

## main working directory
base_directory = os.getcwd()+'/'+options.name
## setup all SM4 datacards
os.system("local2cvs.py --name {NAME} --SM4".format(NAME=options.name))

for channel in ['emu', 'etau', 'mutau'] :
    ## add uncertainties
    os.chdir(base_directory+"/{CHANNEL}".format(CHANNEL=channel))
    datacards= []
    ## collect what is there
    basket = os.listdir(os.getcwd())
    ## skip empty directories
    if len(basket)<1 :
        continue
    for piece in basket :
        if piece.endswith('.txt') :
            datacards.append(piece)
    ## loop all datacards in the given directory
    for datacard in datacards :
        ## determine mass from datacard name
        mass = datacard[datacard.rfind('-')+1:datacard.rfind('.')]
        ## list of indexes that contain signal processes
        processes = []
        ## determine signal processes from datacard
        input_file = open(datacard,'r')
        for input_line in input_file :
            words = input_line.split()
            ## determine which processes in the datacard are actual signal processes
            if words[0] == "process" :
                for word in words :
                    if word.isdigit() or word.lstrip("-").isdigit() :
                        processes.append(word)
        ## close input file
        input_file.close()
        ## append uncertainties to datacard 
        output_file = open(datacard,'a')
        for uncert in ["gamma_Hff", "gamma_HVV", "gamma_Hgluglu"] :
            output_line = uncert+"   ln    "
            for proc in processes : 
                if int(proc) <=0 :
                    print "root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/uncerts2SM4.C+\({MASS}\) | grep {UNCERT}".format(
                        CMSSW_BASE=os.environ['CMSSW_BASE'], MASS=mass, UNCERT=uncert)
                    output_line += os.popen("root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/uncerts2SM4.C+\({MASS}\) | grep {UNCERT}".format(
                        CMSSW_BASE=os.environ['CMSSW_BASE'], MASS=mass, UNCERT=uncert)).read().split()[1]
                else :
                    output_line += "-"
                output_line += "    "
            output_file.write(output_line+'\n')
        ##close otuput file
        output_file.close()
print "done"
