#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to fix the BR problems of the lowmH and tauphobic scenario. ARG corresponds to the file that is to be sculpted. Per default a new file with postfix *_sculpted will be createpick up the mA/tanb datacards from Hplus and Htt, combine them, transfer them to a workspace and put them into a common datacard structure.")
parser.add_option("--path-htt", dest="path_htt", default= "", type="string",
                  help="Path to htt datacards. [Default: \"\"]")
parser.add_option("--path-hplus", dest="path_hplus", default="", type="string",
                  help="Path to hplus datacards. [Default: \"\"]")
parser.add_option("--label", dest="label", default="", type="string",
                  help="Path to htt datacards. [Default: \"\"]")
# check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) != 0 :
    parser.print_usage()
    exit(1)

import os
import glob
import re

#build limit structure
if os.path.exists("LIMITS-MSSMCombination{LABEL}".format(LABEL="" if options.label=="" else "-"+options.label)) :
    os.system("rm -r LIMITS-MSSMCombination{LABEL}".format(LABEL="" if options.label=="" else "-"+options.label))
os.system("mkdir LIMITS-MSSMCombination{LABEL}".format(LABEL="" if options.label=="" else "-"+options.label))
os.system("cp -r {HTT}/common LIMITS-MSSMCombination{LABEL}/".format(HTT=options.path_htt, LABEL="" if options.label=="" else "-"+options.label))

for mass in (90, 100, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000) :
    os.system("mkdir LIMITS-MSSMCombination{LABEL}/{MASS}".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
    if os.path.exists("{HTT}/{MASS}/debug".format(HTT=options.path_htt, MASS=str(mass))) :
        for file in glob.glob("{HTT}/{MASS}/debug/*0.txt".format(HTT=options.path_htt, MASS=str(mass))) :
            tanbs=file.rstrip(".txt").split("_")
            tanb=tanbs[1]
            os.system("cp {FILE} LIMITS-MSSMCombination{LABEL}/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="htt_"+str(tanb)+".txt"))
            if mass > 150 : #area without hplus
                os.system("text2workspace.py -m {MASS} LIMITS-MSSMCombination{LABEL}/{MASS}/htt_{TANB}.txt -o LIMITS-MSSMCombination{LABEL}/{MASS}/batch_{TANB}.root".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
            elif float(tanb) < 1 or float(tanb) >= 10 :
                os.system("text2workspace.py -m {MASS} LIMITS-MSSMCombination{LABEL}/{MASS}/htt_{TANB}.txt -o LIMITS-MSSMCombination{LABEL}/{MASS}/batch_{TANB}.root".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
            print "htt mass", mass, "tanb", tanb
        for file in glob.glob("{HPLUS}/{MASS}/debug/*0.txt".format(HPLUS=options.path_hplus, MASS=str(mass))) :
            if mass < 150 : #only interesting and allowed area 
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                if float(tanb) >= 1 and float(tanb) < 10 :
                    os.system("cp {FILE} LIMITS-MSSMCombination{LABEL}/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="hplus_"+str(tanb)+".txt"))
                    os.system("cp {HPLUS}/{MASS}/combine_histograms_hplushadronic_light.root_{MASS}_{TANB} LIMITS-MSSMCombination{LABEL}/{MASS}".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb).replace("00", "0")))
                    os.system("cp {HPLUS}/{MASS}/combine_histograms_hplushadronic_light.root LIMITS-MSSMCombination{LABEL}/{MASS}".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
                    os.system("combineCards.py -S LIMITS-MSSMCombination{LABEL}/{MASS}/hplus_{TANB}.txt LIMITS-MSSMCombination{LABEL}/{MASS}/htt_{TANB}.txt > LIMITS-MSSMCombination{LABEL}/{MASS}/tmp_{TANB}.txt".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
                    os.system("text2workspace.py -m {MASS} LIMITS-MSSMCombination{LABEL}/{MASS}/tmp_{TANB}.txt -o LIMITS-MSSMCombination{LABEL}/{MASS}/batch_{TANB}.root".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
                    print "hplus mass", mass, "tanb", tanb
                              
                                                                                        

        

    
    
    
